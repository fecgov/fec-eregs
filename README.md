[![Dependency Status](https://gemnasium.com/badges/github.com/18F/fec-eregs.svg)](https://gemnasium.com/github.com/18F/fec-eregs)

[![Build
Status](https://travis-ci.org/18F/fec-eregs.svg?branch=master)](https://travis-ci.org/18F/fec-eregs)

# FEC's eRegs

## Site Location
https://www.fec.gov/regulations

## Code Status:
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/816ef1e6041a46748fa984e6780cc913/badge.svg)](https://www.quantifiedcode.com/app/project/816ef1e6041a46748fa984e6780cc913)  [![Dependency Status](https://gemnasium.com/badges/github.com/18F/fec-eregs.svg)](https://gemnasium.com/github.com/18F/fec-eregs)

Glue project which combines regulations-site, regulations-core and
styles/templates specific to FEC. Packaged as a cloud.gov app.

## Local Development
Like regulations-site and regulations-core, this application requires Python 3.6

Use pip and npm to download the required libraries:

```bash
$ pip install -r requirements.txt
$ pip install -r requirements_dev.txt
$ npm install
```

Then initialize the database, build the front-end, and run the server:

```bash
$ npm run build
$ python manage.py migrate --fake-initial
$ python manage.py compile_frontend
$ python manage.py runserver
```

### Front End Development
The static files are located at: `fec_eregs/static/fec_eregs/`.<br>
Base SCSS files are copied from fec-cms (previously fec-style), but be mindful of custom stylesheets to make it work with this eregs instance.<br>
Running `npm run build` will compile both the JS and SCSS files (generating `/static/fec_eregs/css/main.css`).<br>

It's also important to keep in mind that the `compile_frontend` management command will compile the base regulations styles located at `fec_eregs/static/regulations/*`.


### Loading FEC's regulations

You will need access to FEC's org in cloud.gov for this.
Make sure you have run `pip install -r requirements_dev.txt`.

In the environment you with to update regulations, first run:
```bash
$ cf env eregs
```
It will print to console the environment variables for the current running instance of eregs.
Use that console output to copy / paste the appropriate parameters here:

```bash
$ export HTTP_AUTH_USER=[pasted from cf env output]
$ export HTTP_AUTH_PASSWORD=[pasted from cf env output]
```

If any new regulation parts have been added, add those parts to the list located in
load_regs/fec_reg_parts.txt.

If you are loading regs for a new year, you will need to reset the database. To do that, run:
```bash
$ cf unbind-service eregs fec-eregs-db
$ cf delete-service fec-eregs-db
$ cf create-service aws-rds shared-psql fec-eregs-db
$ cf restage eregs
```

Now you can load the regs with:

```bash
$ python load_regs/load_fec_regs.py dev $HTTP_AUTH_USER $HTTP_AUTH_PASSWORD
```
This process is pretty verbose in terms of console output, and takes about 10 minutes.
Once completed, you will need to reindex the new regulations in elasticsearch so that they
are available through the search engine. Do that with:

```bash
$ cf run-task api  "python manage.py index_regulations" -m 1G --name load-regs
```

And monitor progress with
```bash
cf logs api | grep load-regs
```

### Working with Parser

If you are also working on the parser, it'd be a good idea to test your
changes locally:

```bash
$ python manage.py runserver &    # start the server as a background process
$ cd path/to/regulations-parser
$ eregs pipeline 11 4 http://localhost:8000/api   # send the data
```

If you aren't working on the parser, you may want to just configure the
application to run against the live API:

```bash
$ echo "API_BASE = 'https://fec-prod-eregs.app.cloud.gov/regulations/api/'" >> local_settings.py
```

By default, the application uses a SQLite database named `eregs.db` as its database backend. To use a different database, configure a `default` database using https://docs.djangoproject.com/en/1.8/ref/settings/#databases in `local_settings.py` .

E.g., add the following lines to `local_settings.py`:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

### Ports

For the time being, this application, which cobbles together
[regulations-core](https://github.com/18F/regulations-core) and
[regulations-site](https://github.com/18F/regulations-site), makes HTTP calls
to itself. The server therefore needs to know which port it is set up to
listen on.

We default to 8000, as that's the standard for django's `runserver`, but if
you need to run on a different port, either export an environmental variable
or create a local_settings.py as follows:

```bash
$ export PORT=1234
```

OR

```bash
$ echo "API_BASE = 'http://localhost:1234/api/'" >> local_settings.py
```

## Architecture

![General Architecture (described below)](docs/architecture.png)

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

## Updating Data

![Deploying New Data Schematic (described below)](docs/updating-data.png)

When there is new data available (e.g. due to modifications in the parser, new
Federal Register notices, etc.), that data must be sent to the `/api` endpoint
before it will be visible to users. However, we don't want to allow the
general public to modify the regulatory data, so we need to authenticate.
Currently, this is implemented via HTTP Basic Auth and a very long user name
and password (effectively creating an API key). See the `HTTP_AUTH_USER` and
`HTTP_AUTH_PASSWORD` environment variables in cloud.gov for more.

Currently, sending data looks something like this (from `regulations-parser`)

```bash
$ eregs pipeline 11 4 https://{HTTP_AUTH_USER}:{HTTP_AUTH_PASSWORD}@{LIVE_OR_DEMO_HOSTNAME}/api
```

This updates the data, but does not update the search index and will not clear
various caches. It's generally best to `cf restage` the application at this
point, which clears the caches and rebuilds the search index. Note that this
will also pull down the latest versions of the libraries (see the next
section); as a result it's generally best to do a full deploy after updating
data.

## Deploying Code

If the code within `fec-eregs`, `regulations-core`, or `regulations-site` has
been updated, you will want to deploy the updated code to cloud.gov.


### Environments

We're currently deploying to multiple environments, a `dev`, `stage`, and a `prod`
instance. All environments are deployed automatically based on [git
flow](https://danielkummer.github.io/git-flow-cheatsheet/).

Environment | URL                              | Proxy | Description
----------- | ---                              | ----- | -----------
`dev`       | https://fec-dev-eregs.app.cloud.gov/   | https://fec-dev-proxy.app.cloud.gov/regulations/ | Ad-hoc testing, deploys the latest changes from `develop`.
`stage`     | https://fec-stage-eregs.app.cloud.gov/ | https://fec-stage-proxy.app.cloud.gov/regulations/ | Staging site, deployed from branches matching `release/*`.
`prod`      | https://fec-prod-eregs.app.cloud.gov/  | https://www.fec.gov/regulations/ | Production site, deployed from any tagged commit.


### Travis

These are the basic steps of what get runs on travis. To be sure, check the
[.travis.yml](https://github.com/18F/fec-eregs/blob/develop/.travis.yml) file.

```bash
$ pip install -r requirements.txt   # updates the -core/-site repositories
$ npm run build
$ python manage.py compile_frontend   # builds the frontend
$ cf target -s ${cf_space} && cf zero-downtime-deploy eregs -f manifest.${cf_space}.yml
```
