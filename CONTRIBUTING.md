This document describes how the 18F Legal team has agreed to work together
with regard to Git, GitHub and facilitating changes to the repositories they
administer.

This document describes guidelines, not rules. This means they are not
mandatory. It is expected that everyone will use their best judgment when
deciding when and how to apply these guidelines.

## Workflow

The most common workflow is:

1. A change is initiated and discussed via Zenhub. Zenhub cards are
   prioritized on a per-sprint basis.  To view the Zenhub board, install the [zenhub plugin](https://www.zenhub.io/).  Once done, a tab in Github called "Boards" should appear.
1. Team members are assigned cards during sprint planning.
1. When a team member begins working on a feature, they move the related Zenhub
   card to the "In progress" column. Team members should have no more than 2-3
   "In progress" stories at a time.
1. A Pull Request (PR) is created on Github. The related Zenhub card is
   referenced in the PR description.
1. The PR is reviewed by someone other than the committer.
1. Once PR feedback has been addressed and/or incorporated, the reviewer merges
   the pull request.

## Coding standards

* Use [PEP8](https://www.python.org/dev/peps/pep-0008/) as the coding standard
  for Python.
* Use Sphinx-style docstrings for function and method documentation, including
  signatures, unless they're very short. See
  http://www.sphinx-doc.org/en/stable/domains.html#signatures for details.
* The team aims to have 100% test coverage and will not accept changes that put
  test coverage under 90%.
* Follow the boy scout rule: "Always leave the code cleaner than you
  found it."

## Code review guidelines

* Don't merge your own code.
* Don't merge things until you are confident you could maintain it as-written.
* Commit / PR message should explains what's going on at a high level.
* Aim to have no more than 500 changes per PR. If a change is getting large, do
  your best to break it into multiple PRs.
* If you come upon a bug while doing something else, you can fix it as part of
  your current work.
* If a feature or bug has a separate Zenhub card, it should have its own PR.
* Reviewers expect code to be submitted with test coverage.
* Travis CI runs the test suite and a PEP8 linter on GitHub PRs. PRs should only
  be merged when Travis is green.

## Squashing / rebasing commits

Individual contributors may choose to rebase and [squash
commits](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History#Squashing-Commits)
to clean up git history on a fork that is being PR'd. It is not expected or
required for contributors to change their git history.

## When should a PR be created?

This team opens PRs for all commits, even typos.

## When reviewing a PR, should the change be tested locally?

Yes

## Team processes

* Manually QA your own work before you submit a PR.
* Don't merge your own pull request. Find a friend to review your code and
  merge your pull request.
* Standard code review should be kept to reading, not actually running the
  code. If a feature requires local acceptance, that information is included in
  the Zenhub card along with who should be included in local acceptance process.

When creating a new pull request:

* If the pull request is still a work-in-progress and should not be merged, say
  so in the description.
* Anyone is welcome to informally review a PR and comment on it at any time, no
  matter who is assigned.

## Public domain

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.
