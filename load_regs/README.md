## Loading FEC's regulations
When there is new data available (e.g. due to modifications in the parser, new
Federal Register notices, etc.), that data must be sent to the `/api` endpoint
before it will be visible to users.

If any new regulation parts have been added, add those parts to the list located in
load_regs/fec_reg_parts.txt.

### Create temp eregs db service
```
$ cf unbind-service eregs fec-eregs-db-rdn
$ cf service-keys fec-eregs-db-rdn
$ cf rename-service fec-eregs-db-rdn fec-eregs-db-rdn-2020
$ cf create-service aws-rds micro-psql fec-eregs-db-rdn
$ cf bind-service eregs fec-eregs-db-rdn
$ cf restage eregs (or rebuild fec-eregs on circleci)
```

### Parsing FEC's regulations locally
Following Wiki https://github.com/fecgov/fec-eregs/wiki/Parsing-regulations-locally

### Dump local database file
Generate database dump file from your local eregs db

```
/Library/PostgreSQL/11/bin/pg_dump -F c --no-acl --no-owner -f /<path to the dumpfile>/<dump_file_name>.dump postgres://<username>:<password>@localhost:<port>/<dbname>
```

Ex:
```
/Library/PostgreSQL/11/bin/pg_dump -F c --no-acl --no-owner -f /Users/xxxx/eregs_local_parser_08132021.dump postgres://abcd:1234@localhost:1111/eregs
```

### Restore db dump file to database service on space
```
#Connect to service
cf connect-to-service -no-client eregs fec-eregs-db-rdn
cf create-service aws-rds micro-psql fec-eregs-db-rdn
```

```
/Library/PostgreSQL/11/bin/pg_restore --dbname postgres://<username>:<password>@localhost:<port>/<hostname> --no-acl --no-owner /<path to the dumpfile>/<dump_file_name>.dump
```

Ex:
```
/Library/PostgreSQL/11/bin/pg_restore --dbname postgres://abcd:1234@localhost:1111/eregs --no-acl --no-owner /<path to the dumpfile>/eregs_local_parser_08132021.dump
```

### Load regulations to Elasticsearch
cf run-task api --command "python manage.py load_regulations" -m 2G --name load_all_regulations


### Delete old eregs db service
```
#Service Key
cf sk fec-eregs-db-rdn-2020
```
```
cf delete-service-key fec-eregs-db-rdn-2020 <service_key>
cf delete-service fec-eregs-db-rdn-2020
```

