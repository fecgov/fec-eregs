import os
import json
import git
import cfenv
import sys

from invoke import task

env = cfenv.AppEnv()


def _detect_prod(repo, branch):
    """Deploy to production if master is checked out and tagged."""
    if branch != 'master':
        return False
    try:
        # Equivalent to `git describe --tags --exact-match`
        repo.git().describe('--tags', '--exact-match')
        return True
    except git.exc.GitCommandError:
        return False


def _resolve_rule(repo, branch):
    """Get space associated with first matching rule."""
    for space, rule in DEPLOY_RULES:
        if rule(repo, branch):
            return space
    return None


def _detect_branch(repo):
    try:
        return repo.active_branch.name
    except TypeError:
        return None


def _detect_space(repo, branch=None, yes=False):
    """Detect space from active git branch.

    :param str branch: Optional branch name override
    :param bool yes: Skip confirmation
    :returns: Space name if space is detected and confirmed, else `None`
    """
    space = _resolve_rule(repo, branch)
    if space is None:
        print('No space detected')
        return None
    print('Detected space {space}'.format(**locals()))
    if not yes:
        run = input(  # nosec
            'Deploy to space {space} (enter "yes" to deploy)? > '.format(**locals())
        )
        if run.lower() not in ['y', 'yes']:
            return None
    return space


DEPLOY_RULES = (
    ('prod', _detect_prod),
    ('stage', lambda _, branch: branch.startswith('release')),
    ('dev', lambda _, branch: branch == 'develop'),
)


@task
def deploy(ctx, space=None, branch=None, login=None, yes=False):
    """Deploy app to Cloud Foundry.

    Log in using credentials stored in
    `FEC_CF_USERNAME` and `FEC_CF_PASSWORD`; push to either `space` or the space
    detected from the name and tags of the current branch. Note: Must pass `space`
    or `branch` if repo is in detached HEAD mode, e.g. when running on Travis.
    """
    # Detect space
    repo = git.Repo('.')
    branch = branch or _detect_branch(repo)
    space = space or _detect_space(repo, branch, yes)
    if space is None:
        return

    if login == 'True':
        # Set api
        api = 'https://api.fr.cloud.gov'
        ctx.run('cf api {0}'.format(api), echo=True)
        # Authorize
        login_command = 'cf auth "$FEC_CF_USERNAME_{0}" "$FEC_CF_PASSWORD_{0}"'.format(space.upper())
        ctx.run(login_command, echo=True)

    # Target space
    ctx.run('cf target -o fec-beta-fec -s {0}'.format(space), echo=True)

    # Set deploy variables
    with open('.cfmeta', 'w') as fp:
        json.dump({'user': os.getenv('USER'), 'branch': branch}, fp)

    # Deploy eregs
    existing_deploy = ctx.run('cf app eregs', echo=True, warn=True)
    print("\n")
    cmd = 'push --strategy rolling' if existing_deploy.ok else 'push'
    new_deploy = ctx.run('cf {0} eregs -f manifest_{1}.yml'.format(cmd, space),
        echo=True,
        warn=True
    )

    if not new_deploy.ok:
        print("Build failed!")
        # Check if there are active deployments
        app_guid = ctx.run('cf app eregs --guid', hide=True, warn=True)
        app_guid_formatted = app_guid.stdout.strip()
        status = ctx.run('cf curl "/v3/deployments?app_guids={}&status_values=ACTIVE"'.format(app_guid_formatted), hide=True, warn=True)
        active_deployments = json.loads(status.stdout).get("pagination").get("total_results")
        # Try to roll back
        if active_deployments > 0:
            print("Attempting to roll back any deployment in progress...")
            # Show the in-between state
            ctx.run('cf app eregs', echo=True, warn=True)
            cancel_deploy = ctx.run('cf cancel-deployment eregs', echo=True, warn=True)
            if cancel_deploy.ok:
                print("Successfully cancelled deploy.")
            else:
                print("Unable to cancel deploy.")
        print("Check logs for more detail.")
        return sys.exit(1)

    print("\nA new version of your application 'eregs' has been successfully pushed!")
    ctx.run('cf apps', echo=True, warn=True)

    # Needed for CircleCI
    return sys.exit(0)
