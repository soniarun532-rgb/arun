%dw 2.0
output application/java
---
{
  fromDate: attributes.queryParams.fromDate,
  toDate: attributes.queryParams.toDate,
  PageNumber: attributes.queryParams.PageNumber default "1",
  database: p('process.api.database'),
  supplier: p('process.api.supplier')
}
