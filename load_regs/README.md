## Load FEC's regulations
When there are new regulations available in [GPO website](https://www.govinfo.gov/bulkdata/CFR/) (e.g. due to modifications in the parser, new Federal Register notices, etc.), that data must be sent to the regulations `/api` endpoint before it will be visible to users on the [website](https://www.fec.gov/regulations).

If any new regulation parts have been added, add those parts to the list located in load_regs/fec_reg_parts.txt.

### Parse FEC's regulations locally
Follow Wiki [Parsing regulations locally](https://github.com/fecgov/fec-eregs/wiki/Parsing-regulations-locally)

### Create new eregs database service
```
$ cf unbind-service eregs fec-eregs-db-rdn
$ cf rename-service fec-eregs-db-rdn fec-eregs-db-rdn-<YEAR>
$ cf create-service aws-rds micro-psql fec-eregs-db-rdn
$ cf bind-service eregs fec-eregs-db-rdn
$ cf restage eregs (or rebuild fec-eregs on circleci)
```

### Generate local eregs-database dump file
Note: Verify the location of db client command(pg_dump and pg_restore) on your local before generating database dump file
(e.g. `/usr/local/opt/postgresql@11/bin` or `/Library/PostgreSQL/11/bin/`)

```
/Library/PostgreSQL/11/bin/pg_dump -F c --no-acl --no-owner -f /<path to the dumpfile>/<dump_file_name>.dump postgres://<username>:<password>@localhost:<port>/<dbname>
```

### Restore eregs-database dump file to database service on space
```
#Setup SSH connection and get eregs database service credentials
cf connect-to-service -no-client eregs fec-eregs-db-rdn
```

```
/Library/PostgreSQL/11/bin/pg_restore --dbname postgres://<username>:<password>@localhost:<port>/<hostname> --no-acl --no-owner /<path to the dumpfile>/<dump_file_name>.dump
```

### Load regulations to Elasticsearch
```
cf run-task api --command "python manage.py load_regulations" -m 2G --name load_all_regulations
```
open api log terminal to verify regulations load successfully.
```
cf logs api |grep "<task_name>"
```

### Delete old eregs db service
```
#Get service key
cf sk fec-eregs-db-rdn-<YEAR>
cf delete-service-key fec-eregs-db-rdn-<YEAR> <service_key>
cf delete-service fec-eregs-db-rdn-<YEAR>
```

