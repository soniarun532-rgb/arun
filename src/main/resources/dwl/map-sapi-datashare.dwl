%dw 2.0
output application/json

fun v(row, keys) = do {
	var list = if (keys is Array) keys else [keys]
	---
	list reduce ((k, acc = null) ->
		if ((acc != null) and ((acc as String default "") != ""))
			acc
		else
			row[k] default row[upper(k)] default row[lower(k)]
	)
}

fun s(row, keys) = (v(row, keys) as String) default ""

fun numericProductId(code) = ((code default "") as String) replace /^[A-Za-z]+/ with ""

fun fmtDate(value) =
	if ((value == null) or (value == ""))
		""
	else
		((value as DateTime default value as LocalDateTime default value as Date default null) as String {format: "dd/MM/yyyy"}) default ((value as String) default "")

fun fmtTime(value) =
	if ((value == null) or (value == ""))
		""
	else
		((value as DateTime default value as LocalDateTime default null) as String {format: "HH:mm:ss"}) default ((value as String) default "")

fun toExpNext(n) = do {
	var expBase = trim((p("papi.exp.datashare.base.url") default p("exp.base.url") default "") as String) replace /\/$/ with ""
	var papiPath = (vars.adapterPublicPath default "") as String
	var raw = n as String default ""
	var q = if (raw contains "?") ((raw splitBy "?")[1] default "") else ""
	---
	if ((expBase == "") or (papiPath == ""))
		raw
	else
		expBase ++ papiPath ++ (if (q != "") ("?" ++ q) else "")
}

fun mapInvoice(sale) = {
	STOREID: s(sale, ["SHOPID", "SHOP_ID"]),
	Discount: v(sale, ["DISCOUNT"]) default "",
	SalesRepID: s(sale, ["USERID", "USER_ID"]),
	VATAmount: v(sale, ["TOTAL_VAT"]) default "",
	RouteID: s(sale, ["ROUTEID", "routeid"]),
	DistributorID: (p("papi.sat.solutech.distributor.id") default "") as String,
	ProductID: numericProductId(v(sale, ["PRODUCT_CODE", "PRODUCTCODE"])),
	WarehouseID: s(sale, ["SUPPLIER_ID"]),
	OrderNumber: s(sale, ["SALE_ORDER_ID"]),
	InvoiceNumber: s(sale, ["ENTRY_ID"]),
	InvoiceDate: fmtDate(v(sale, ["CREATED_AT", "Created_AT"])),
	InvoiceTime: fmtTime(v(sale, ["CREATED_AT", "Created_AT"])),
	InvoiceStatus: s(sale, ["PAYMENT_STATUS"]),
	UnitOfMeasure: s(sale, ["PACKAGING"]),
	Currency: (p("papi.sat.solutech.currency") default "KES") as String,
	QuantityInvoiced: v(sale, ["QUANTITY"]) default "",
	AmountInvoiced: v(sale, ["VALUE_SOLD"]) default "",
	TransType: s(sale, ["ENTRY_TYPE"])
}

fun mapOrder(row) = {
	StoreID: s(row, ["SHOP_ID", "SHOPID"]),
	SalesRepID: s(row, ["SALES_REP", "SALESREP"]),
	RouteID: s(row, ["routeid", "ROUTEID"]),
	ProductID: numericProductId(v(row, ["PRODUCT_code", "PRODUCT_CODE", "PRODUCTCODE"])),
	DistributorID: (p("papi.sat.solutech.distributor.id") default "") as String,
	WarehouseID: s(row, ["supplier_id", "SUPPLIER_ID"]),
	OrderNumber: s(row, ["ENTRY_ID"]),
	OrderDate: fmtDate(v(row, ["CHECKINTIME", "CHECK_IN_TIME"])),
	OrderStartTime: fmtTime(v(row, ["CHECKINTIME"])),
	OrderEndTime: fmtTime(v(row, ["CHECKOUTTIME"])),
	OrderStatus: v(row, ["DELIVERED"]) default "",
	UnitOfMeasure: s(row, ["PACKAGING"]),
	Currency: (p("papi.sat.solutech.currency") default "KES") as String,
	QuantityOrdered: v(row, ["QUANTITY"]) default "",
	AmountOrdered: v(row, ["TOTAL_VAT_INC"]) default "",
	Discount: v(row, ["DISCOUNT"]) default "",
	VATAmount: v(row, ["TOTAL_VAT"]) default ""
}

fun mapProduct(row) = {
	id: v(row, ["id", "ID"]) default "",
	ProductID: numericProductId(v(row, ["productcode", "PRODUCTCODE"])),
	product_category: v(row, ["product_category", "PRODUCT_CATEGORY"]) default "",
	product_name: v(row, ["product_name", "PRODUCT_NAME"]) default "",
	ProductSKU: v(row, ["product_desc", "PRODUCT_DESC"]) default "",
	product_status: v(row, ["product_status", "PRODUCT_STATUS"]) default "",
	short_code: v(row, ["short_code", "SHORT_CODE"]) default "",
	tax_code: v(row, ["tax_code", "TAX_CODE"]) default "",
	hs_code: v(row, ["hs_code", "HS_CODE"]) default "",
	focus_product: v(row, ["focus_product", "FOCUS_PRODUCT"]) default "",
	tonne_equivalent: v(row, ["tonne_equivalent", "TONNE_EQUIVALENT"]) default "",
	apply_discount: v(row, ["apply_discount", "APPLY_DISCOUNT"]) default "",
	disable_price_check: v(row, ["disable_price_check", "DISABLE_PRICE_CHECK"]) default "",
	product_type: v(row, ["product_type", "PRODUCT_TYPE"]) default "",
	supplier: v(row, ["supplier", "SUPPLIER"]) default "",
	alternative_group: v(row, ["alternative_group", "ALTERNATIVE_GROUP"]) default "",
	supplier_id: v(row, ["supplier_id", "SUPPLIER_ID"]) default "",
	UnitofMeasure: v(row, ["uomname", "UOMName", "UOMNAME"]) default ""
}

fun mapStock(row) = {
	ProductID: numericProductId(v(row, ["productcode", "PRODUCTCODE"])),
	UnitofMeasure: v(row, ["UOMName", "uomname", "UOMNAME"]) default "",
	WarehouseName: v(row, ["stockpoint_name", "STOCKPOINT_NAME"]) default "",
	DateCreated: fmtDate(v(row, ["date_created", "DATE_CREATED"])),
	Quantity: v(row, ["quantity", "QUANTITY"]) default "",
	TotalCost: v(row, ["total_cost", "TOTAL_COST"]) default ""
}

var adapter = (vars.adapterResource default "") as String
var rows = payload.data default []
var mapped =
	if (adapter == "invoice") rows map mapInvoice($)
	else if (adapter == "order") rows map mapOrder($)
	else if (adapter == "product") rows map mapProduct($)
	else if (adapter == "stock") rows map mapStock($)
	else rows
---
{
	data: mapped
} ++ (if (payload.next != null) { next: toExpNext(payload.next) } else {})
