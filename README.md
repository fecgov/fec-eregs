[![CircleCI](https://circleci.com/gh/fecgov/fec-eregs.svg?style=svg)](https://circleci.com/gh/fecgov/fec-eregs)

## FEC's eRegs

The Federal Election Commission's web-based application that makes regulations easier to find, read and understand.

Glue project which combines [regulations-site](https://github.com/eregs/regulations-site), [regulations-core](https://github.com/eregs/regulations-core) and
styles/templates specific to FEC. Packaged as a cloud.gov app.

## Site Location
https://www.fec.gov/regulations

**package.json**
[![Known Vulnerabilities](https://snyk.io/test/github/fecgov/fec-eregs/badge.svg)](https://snyk.io/test/github/fecgov/fec-eregs?targetFile=package.json)
**requirements.txt**
[![Known Vulnerabilities](https://snyk.io/test/github/fecgov/fec-eregs/badge.svg)](https://snyk.io/test/github/fecgov/fec-eregs?targetFile=requirements.txt)

## Architecture

![General Architecture (described below)](https://github.com/fecgov/fec-eregs/blob/develop/load_regs/eregs_general_architecture.png)

This repository is a cloud.gov app which stitches together two large Django
libraries with cloud.gov datastores and some FEC-specific styles and
templates. The first library, `regulations-core`, defines an API for reading
and writing regulation and associated data. `fec-eregs` mounts this
application at the `/api` endpoint (details about the "write" API will be
discussed later). The second library, `regulations-site`, defines the UI. When
rendering templates, `regulations-site` will first look in `fec-eregs` to see
if the templates have been overridden. These views pull their data from the
API; this means that `fec-eregs` makes HTTP calls to itself to retrieve data
(when it's not already cached).

## Environments

We're currently deploying to multiple environments, a `dev`, `stage`, and a `prod`
instance. All environments are deployed automatically based on [git
flow](https://danielkummer.github.io/git-flow-cheatsheet/).


Environment | App URL                              | Proxy | Website URL | Description
----------- | ---                              | ----- | ----- | -----------
`dev`       | https://fec-dev-eregs.app.cloud.gov/regulations/ | https://fec-dev-proxy.app.cloud.gov/regulations/ | https://dev.fec.gov/regulations/ | Ad-hoc testing, deploys the latest changes from `develop`.
`stage`     | https://fec-stage-eregs.app.cloud.gov/regulations/ | https://fec-stage-proxy.app.cloud.gov/regulations/ | https://stage.fec.gov/regulations/ | Staging site, deployed from branches matching `release/*`.
`prod`      | https://fec-prod-eregs.app.cloud.gov/regulations/ | https://www.fec.gov/regulations/ | https://www.fec.gov/regulations/ | Production site, deployed from any tagged commit.


## Front End Development
The static files are located at: `fec_eregs/static/fec_eregs/`.<br>
Base SCSS files are copied from fec-cms (previously fec-style), but be mindful of custom stylesheets to make it work with this eregs instance.<br>
Running `npm run build` will compile both the JS and SCSS files (generating `/static/fec_eregs/css/main.css`).<br>

It's also important to keep in mind that the `compile_frontend` management command will compile the base regulations styles located at `fec_eregs/static/regulations/*`.

## Local Development
This application requires Python 3.9.X

Use pip and npm to download the required libraries:

```bash
$ pip install -r requirements.txt
# remove the node_modules from your local environment
$ rm -rf node_modules/
$ npm install
```

Then initialize the database, build the front-end, and run the server:

```bash
$ npm run build
$ python manage.py migrate
$ python manage.py compile_frontend
$ python manage.py runserver
```

Create local_settings.py and point to <cf_space> regulations API. Replace <cf_space> with dev/stage or prod in the following url.
```bash
$ echo "API_BASE = 'https://fec-<cf_space>-eregs.app.cloud.gov/regulations/api/'" >> local_settings.py
```

## Deploying Code

If the code within `fec-eregs`, `regulations-core`, or `regulations-site` has
been updated, you will want to deploy the updated code to cloud.gov.

```bash
$ pip install -r requirements.txt   # updates the -core/-site repositories
$ npm run build
$ python manage.py compile_frontend   # builds the frontend
$ cf target -s ${cf_space}
$ cf push --strategy rolling eregs -f manifest.${cf_space}.yml
```

## Load FEC's regulations

1. Follow the wiki to [parse regulations on local](https://github.com/fecgov/fec-eregs/wiki/Parse-regulations-on-local).
2. Follow this instructions to [parse regulations on cloud.gov space](https://github.com/fecgov/fec-eregs/tree/develop/load_regs#load-fecs-regulations-on-cloudgov-space).


### Ports

For the time being, this application, which cobbles together
[regulations-core](https://github.com/eregs/regulations-core) and
[regulations-site](https://github.com/eregs/regulations-site), makes HTTP calls
to itself. The server therefore needs to know which port it is set up to
listen on.

We default to 8000, as that's the standard for django's `runserver`, but if
you need to run on a different port, either export an environmental variable
or create a local_settings.py as follows:

```bash
$ export PORT=1234
```

OR

 Update the port# in local_settings.py
```bash
  "API_BASE = 'http://localhost:1234/api/'" 
```

