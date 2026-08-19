%dw 2.0
output application/java
---
{
  fromDate: attributes.queryParams.fromDate,
  toDate: attributes.queryParams.toDate,
  limit: attributes.queryParams.limit default "10000",
  offset: attributes.queryParams.offset default "0",
  Database: p('process.api.database'),
  Supplier: p('process.api.supplier')
}
