%dw 2.0
output application/java
---
{
	fromDate: attributes.queryParams.fromDate,
	toDate: attributes.queryParams.toDate,
	database: p("api.database"),
	supplier: p("api.supplier"),
	pageNumber: ((attributes.queryParams.pageNumber default 0) as Number) as String
}
