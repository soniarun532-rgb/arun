%dw 2.0
output application/java
---
{
  fromDate: attributes.queryParams.fromDate,
  toDate: attributes.queryParams.toDate,
  PageNumber: attributes.queryParams.PageNumber default "1",
  Database: p('process.api.database'),
  Supplier: p('process.api.supplier')
}
