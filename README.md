# exp-sat-datashare-api

SAT Datashare Experience API. Latest implementation from [exp-sat-datashare-api](https://github.com/soniarun532-rgb/exp-sat-datashare-api).

It accepts `fromDate`, `toDate`, `limit`, and `offset`, calls the Solutech process API, and adds `database` and `supplier` from properties.

When another page exists, the response includes a `next` URL whose **host is always the experience API** (`eapi.host`). Downstream SAPI/PAPI hosts are not exposed.

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

Example next URL:

`https://exp-sat-datashare-sand-api-5nct48.2ky31l-2.deu-c1.eu1.cloudhub.io/api/v1/Invoice?fromDate=2026-08-01&toDate=2026-08-10&limit=10000&offset=10000`

## Runtime

Same property pattern as PAPI/SAPI: `${env}.properties` with a global `env` property (default `dev`).

```
-M-Denv=dev
```

Prod:

```
-M-Denv=prod
```

Properties:

- `src/main/resources/dev.properties`
- `src/main/resources/prod.properties`

Key properties:

- `eapi.host` — public experience host used in `next`
- `process.api.host` / `process.api.port` — process API
- `process.api.database` / `process.api.supplier`
