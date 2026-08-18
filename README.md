# arun

System API (`sys-solutech-api-v2`) GET endpoints from APIkit (`solutech-sapi-uat` 1.0.21):

- `GET /api/products` → `mysql-query-main`
- `GET /api/sales` → `mysql-query-main`

Reusable pieces: `mysql-query-main` (paging + SQL) and `mysql-query-subflow` (`db:select`). New GET endpoints set `vars.endpoint` (or `vars.sql` / `vars.sqlParams`) and flow-ref `mysql-query-main`.

## GET `/api/products` (D)

`SELECT id, product_name FROM {Database}.bi_products WHERE supplier = :Supplier`

| Param | Notes |
|---|---|
| `PageNumber` | default `1`, size `100` |
| `Database` | schema, e.g. `sat_nobleoutlook` |
| `Supplier` | e.g. `BIC EAST AFRCA LIMITED` |

```
GET /api/products?PageNumber=1&Database=sat_nobleoutlook&Supplier=BIC%20EAST%20AFRCA%20LIMITED
```

## GET `/api/sales` (C)

`bi_salesmaster` A left join `bi_customer_visits` B on `a.VisitID = b.visitid`, filtered by `Created_AT` only.

| Param | Notes |
|---|---|
| `fromDate` | `YYYY-MM-DD` → `00:00:00` |
| `toDate` | `YYYY-MM-DD` → `00:00:00` |
| `PageNumber` | default `1`, size `100` |
| `Database` | schema |

```
GET /api/sales?fromDate=2026-08-13&toDate=2026-08-14&PageNumber=1&Database=sat_nobleoutlook
```

Process API sequence: call products, call sales, then join `C.ProductID = D.id`.

Table names come from properties: `db.table.sales`, `db.table.visits`, `db.table.products`.
