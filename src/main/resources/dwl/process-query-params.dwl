%dw 2.0
output application/java
---
{
	(fromDate: attributes.queryParams.fromDate) if ((attributes.queryParams.fromDate default "") as String != ""),
	(toDate: attributes.queryParams.toDate) if ((attributes.queryParams.toDate default "") as String != ""),
	database: p("exp.sat.solutech.mysql.database") default p("process.api.database") default p("api.database"),
	supplier: p("exp.sat.solutech.mysql.supplier") default p("process.api.supplier") default p("api.supplier"),
	pageNumber: ((attributes.queryParams.pageNumber default 0) as Number) as String
}
