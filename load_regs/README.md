## FEC's regulations
When there are new regulations available in [GPO website](https://www.govinfo.gov/bulkdata/CFR/) (e.g. due to modifications in the parser, new Federal Register notices, etc.), that data must be sent to the regulations `/api` endpoint before it will be visible to users on the [website](https://www.fec.gov/regulations).

If any new regulation parts have been added, add those parts to the list located in load_regs/fec_reg_parts.txt.

## Install cf-service-connect plugin on MAC 
After CLI upgrade, run the following command to install cf-service-connect plugin. 

```
cf install-plugin https://github.com/cloud-gov/cf-service-connect/releases/download/v1.1.3/cf-service-connect_darwin_amd64
```

### Load FEC's regulations on cloud.gov space

1.  Parse FEC's regulations locally
Follow Wiki [Parse regulations on local](https://github.com/fecgov/fec-eregs/wiki/Parse-regulations-on-local)

2. Generate local eregs database dump file
Note: Verify the location of db client command(pg_dump and pg_restore) on local before generating database dump file
(e.g. `/opt/homebrew/opt/postgresql@13/bin/` or /usr/local/opt/postgresql@13/bin`)

```
/opt/homebrew/opt/postgresql@13/bin/pg_dump -F c --no-acl --no-owner -f /<path to the dumpfile>/<dump_file_name>.dump postgres://<username>:<password>@localhost:<port>/<dbname>
```
    or
```
/usr/local/opt/postgresql@13/bin/pg_dump -F c --no-acl --no-owner -f /<path to the dumpfile>/<dump_file_name>.dump postgres://<username>:<password>@localhost:<port>/<dbname>
```

3. Create new eregs database service

```
$ cf unbind-service eregs fec-eregs-db-rdn
$ cf rename-service fec-eregs-db-rdn fec-eregs-db-rdn-<YEAR>
$ cf create-service aws-rds micro-psql fec-eregs-db-rdn
```

4. Setup SSH connection and get eregs database service credentials
```
$ cf connect-to-service -no-client eregs fec-eregs-db-rdn
```

5. Restore eregs database dump file to database service on space
```
/opt/homebrew/opt/postgresql@13/bin/pg_restore --dbname postgres://<username>:<password>@localhost:<port>/<hostname> --no-acl --no-owner /<path to the dumpfile>/<dump_file_name>.dump
```
    or 

```
/usr/local/opt/postgresql@13/bin/pg_restore --dbname postgres://<username>:<password>@localhost:<port>/<hostname> --no-acl --no-owner /<path to the dumpfile>/<dump_file_name>.dump
```

6. Bind eregs app to the database service on space 
```
$ cf bind-service eregs fec-eregs-db-rdn
```

7. Restage eregs app 
```
$ cf restage eregs (or rebuild fec-eregs on circleci)
```

8. Reload regulations to elasticsearch service (to be able to perform a keyword search on Regulations page)
```
cf run-task api --command "python cli.py initialize_legal_data ao_index" -m 4G --name initialize_legal_data_ao
```

9. Open api log terminal to verify regulations load successfully.
```
cf logs api |grep "<task_name>"
```

12. Delete old eregs db service
```
# Get service key
cf sk fec-eregs-db-rdn-<YEAR>
cf delete-service-key fec-eregs-db-rdn-<YEAR> <service_key>
cf delete-service fec-eregs-db-rdn-<YEAR>
```

