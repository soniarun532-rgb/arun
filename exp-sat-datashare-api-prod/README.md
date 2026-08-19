# exp-sat-datashare-prod-api

SAT Datashare Experience API. It accepts `fromDate`, `toDate`, and `PageNumber`, then calls the Solutech process API and adds `Database` and `Supplier` from configuration.

Process API: `https://prc-solutech-api-v1-5nct48.2ky31l-1.deu-c1.eu1.cloudhub.io`

## Endpoints

- `GET /api/v1/Invoice`
- `GET /api/v1/Order`
- `GET /api/v1/Product`
- `GET /api/v1/Route`
- `GET /api/v1/SalesRep`
- `GET /api/v1/Store`
- `GET /api/v1/Inventory`
- `GET /api/v1/Warehouse`

Query parameters sent to the process API:

| Name | Source |
|---|---|
| fromDate | inbound query param |
| toDate | inbound query param |
| PageNumber | inbound query param (default `1`) |
| Database | `process.api.database` in env properties |
| Supplier | `process.api.supplier` in env properties |

## Runtime

```
-M-Dmule.env=dev
-M-Dsecure.key=<your-aes-key>
```

Prod:

```
-M-Dmule.env=prod
-M-Dsecure.key=<your-aes-key>
```

Properties:

- `src/main/resources/properties/config-common.yaml` (shared host, base path, timeouts)
- `src/main/resources/properties/config-dev.yaml` (Database, Supplier, port)
- `src/main/resources/properties/config-prod.yaml` (Database, Supplier, port, prod timeout)
- `src/main/resources/properties/secure-dev.yaml`
- `src/main/resources/properties/secure-prod.yaml`

Mule files:

- `src/main/mule/global.xml`
- `src/main/mule/global-error-handler.xml`
- `src/main/mule/main.xml`
- `src/main/mule/call-prc-solutech-api-sub-flow.xml`

Replace `REPLACE_*_CLIENT_ID` / `REPLACE_*_CLIENT_SECRET` in the secure files. To encrypt a value:

```
java -jar secure-properties-tool.jar string encrypt AES CBC <secure.key> "<value>"
```

Wrap the result as `![encrypted-value]` in the secure YAML.

Set CloudHub / Runtime Manager properties:

- `mule.env` = `dev` or `prod`
- `secure.key` = encryption key (mark as sensitive)
- optionally override `process.api.database` and `process.api.supplier`
