# arun

System API work lives on branch `new/system` (`sys-solutech-api-v2`).

This change adds two MySQL GET endpoints on the system API.

## 1. GET `/api/Sales` (endpoint C)

Reads `bi_salesmaster` (A) left joined to `bi_customer_visits` (B) on `a.VisitID = b.visitid`.

| Query param | Required | Notes |
|---|---|---|
| `fromDate` | yes | `YYYY-MM-DD`, applied to `a.Created_AT` from `00:00:00` |
| `toDate` | yes | `YYYY-MM-DD`, applied to `a.Created_AT` to `00:00:00` (same bound as the sample SQL) |
| `PageNumber` | no | default `1`, page size `100` |
| `Database` | yes | MySQL schema, e.g. `sat_nobleoutlook` |
| `Product_ID` | no | list: `1,2,3` or repeated `Product_ID=` |

Example:

```
GET /api/Sales?fromDate=2026-08-13&toDate=2026-08-14&PageNumber=1&Database=sat_nobleoutlook&Product_ID=8,73
```

## 2. GET `/api/Product` (endpoint D)

Reads `bi_products` filtered by `supplier`.

| Query param | Required | Notes |
|---|---|---|
| `PageNumber` | no | default `1`, page size `100` |
| `Database` | yes | MySQL schema, e.g. `sat_nobleoutlook` |
| `Supplier` | yes | exact match on `bi_products.supplier` |

Example:

```
GET /api/Product?PageNumber=1&Database=sat_nobleoutlook&Supplier=BIC%20EAST%20AFRCA%20LIMITED
```
