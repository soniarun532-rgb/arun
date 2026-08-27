%dw 2.0
output application/java
---
{
  fromDate: attributes.queryParams.fromDate,
  toDate: attributes.queryParams.toDate,
  database: attributes.queryParams.database as String,
  supplier: (attributes.queryParams.supplier default attributes.queryParams.Supplier default "") as String,
  pageNumber: ((attributes.queryParams.pageNumber default 0) as Number) as String
}
