%dw 2.0
output application/java
var endpoint = vars.endpoint default ""
var skipDates = [
	"Adapter_Product",
	"Adapter_Route",
	"Adapter_SalesRep",
	"Adapter_Stock",
	"Adapter_Warehouse"
] contains endpoint
var base = {
	database: p("exp.sat.solutech.mysql.database"),
	supplier: p("exp.sat.solutech.mysql.supplier"),
	pageNumber: ((attributes.queryParams.pageNumber default 0) as Number) as String
}
---
if (skipDates)
	base
else
	base ++ {
		fromDate: attributes.queryParams.fromDate,
		toDate: attributes.queryParams.toDate
	}
