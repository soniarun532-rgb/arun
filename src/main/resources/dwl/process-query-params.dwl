%dw 2.0
output application/java
---
{
	fromDate: attributes.queryParams.fromDate,
	toDate: attributes.queryParams.toDate,
	database: p("exp.sat.solutech.mysql.database") default p("api.database") default p("process.api.database"),
	supplier: p("exp.sat.solutech.mysql.supplier") default p("api.supplier") default p("process.api.supplier"),
	pageNumber: ((attributes.queryParams.pageNumber default 0) as Number) as String
}
