%dw 2.0
output application/java
---
{
  fromDate: attributes.queryParams.fromDate,
  toDate: attributes.queryParams.toDate,
  limit: attributes.queryParams.limit default "10000",
  offset: attributes.queryParams.offset default "0",
  database: p('process.api.database'),
  supplier: p('process.api.supplier')
}
