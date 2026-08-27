%dw 2.0
output application/java
---
{
  fromDate: attributes.queryParams.fromDate,
  toDate: attributes.queryParams.toDate,
  database: p("process.api.database"),
  supplier: p("process.api.supplier"),
  pageNumber: ((attributes.queryParams.pageNumber default 0) as Number) as String
}
