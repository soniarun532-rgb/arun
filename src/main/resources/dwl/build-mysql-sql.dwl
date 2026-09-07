%dw 2.0
output text/plain

fun ident(v) =
	((v default "") as String) replace /[^A-Za-z0-9_]/ with ""

fun lit(v) =
	((v default "") as String) replace "'" with "''"

var db = ident(vars.databaseName default attributes.queryParams.database)
var supplier = lit(vars.supplier default attributes.queryParams.supplier default attributes.queryParams.Supplier)
var sales = p("sapi.mysql.sat.table.sales") default p("db.table.sales") default "bi_salesmaster"
var orders = p("sapi.mysql.sat.table.orders") default "bi_ordersmaster"
var visits = p("sapi.mysql.sat.table.visits") default p("db.table.visits") default "bi_customer_visits"
var products = p("sapi.mysql.sat.table.products") default p("db.table.products") default "bi_products"
var uomQty = p("sapi.mysql.sat.table.uom.quantities") default "bi_uom_quantities"
var uom = p("sapi.mysql.sat.table.uom") default "bi_uom"
var routes = p("sapi.mysql.sat.table.routes") default "bi_routes"
var userRoutes = p("sapi.mysql.sat.table.user.routes") default "bi_user_routes"
var users = p("sapi.mysql.sat.table.users") default "bi_users"
var userCategories = p("sapi.mysql.sat.table.user.categories") default "bi_user_categories"
var customers = p("sapi.mysql.sat.table.customers") default "bi_customer_master"
var stockMovement = p("sapi.mysql.sat.table.stock.movement") default "bi_stock_movement"
var pageSize = (vars.limit as Number) default ((p("sapi.mysql.sat.query.page.size") default p("db.limit") default 10000) as Number)
var pageNumber = (vars.pageNumber as Number) default (attributes.queryParams.pageNumber as Number default 0)
var fetchLimit = ((pageSize as Number) + 1) as String
var off = ((vars.offset as Number) default ((if (pageNumber < 0) 0 else pageNumber) * pageSize)) as String
var lim = " LIMIT " ++ fetchLimit ++ " OFFSET " ++ off
var fromTs = if (((vars.fromDate default "") as String) != "") (((vars.fromDate as String) ++ " 00:00:00")) else ""
var toTs = if (((vars.toDate default "") as String) != "") (((vars.toDate as String) ++ " 00:00:00")) else ""
var endpoint = (vars.endpoint default "") as String
var productSupplierExistsRoutes =
	"(Select distinct routeid from (" ++
	"select Distinct v.routeid, y.product_id from " ++ db ++ "." ++ sales ++ " as y inner join " ++ db ++ "." ++ visits ++ " as v on y.VisitID = v.visitid " ++
	"union all " ++
	"select Distinct v.routeid, y.product_id from " ++ db ++ "." ++ orders ++ " as y inner join " ++ db ++ "." ++ visits ++ " as v on y.Visit_ID = v.visitid" ++
	") as x inner join " ++ db ++ "." ++ products ++ " as z on x.product_id = z.id where z.supplier = '" ++ supplier ++ "')"
var productSupplierExistsUsers =
	"(Select distinct userid from (" ++
	"select Distinct userid, y.product_id from " ++ db ++ "." ++ sales ++ " as y " ++
	"union all " ++
	"select Distinct user_id as userid, y.product_id from " ++ db ++ "." ++ orders ++ " as y" ++
	") as x inner join " ++ db ++ "." ++ products ++ " as z on x.product_id = z.id where z.supplier = '" ++ supplier ++ "')"
var productSupplierExistsShops =
	"(Select distinct SHOPID from (" ++
	"select Distinct SHOPID, product_id from " ++ db ++ "." ++ sales ++ " as y " ++
	"union all " ++
	"select Distinct SHOP_ID as SHOPID, product_id from " ++ db ++ "." ++ orders ++ " as y" ++
	") as x inner join " ++ db ++ "." ++ products ++ " as z on x.product_id = z.id where z.supplier = '" ++ supplier ++ "')"

fun invoiceSql() =
	"Select a.*, b.routeid from " ++ db ++ "." ++ sales ++ " as a " ++
	"left join " ++ db ++ "." ++ visits ++ " as b on a.VisitID = b.visitid " ++
	"inner join " ++ db ++ "." ++ products ++ " as c on a.PRODUCT_ID = c.id and c.supplier = '" ++ supplier ++ "' " ++
	(if ((fromTs != "") and (toTs != ""))
		("where a.Created_AT between '" ++ fromTs ++ "' and '" ++ toTs ++ "' ")
	else "") ++
	"order by a.Entry_ID desc" ++ lim

fun orderSql() =
	"Select a.*, b.routeid, b.CHECKINTIME, b.CHECKOUTTIME from " ++ db ++ "." ++ orders ++ " as a " ++
	"inner join " ++ db ++ "." ++ products ++ " as c on a.PRODUCT_ID = c.id and c.supplier = '" ++ supplier ++ "' " ++
	"left join " ++ db ++ "." ++ visits ++ " as b on a.VISIT_ID = b.visitid " ++
	(if ((fromTs != "") and (toTs != ""))
		("where b.CHECKINTIME between '" ++ fromTs ++ "' and '" ++ toTs ++ "' ")
	else "") ++
	"order by a.ENTRY_ID desc" ++ lim

fun productSql() =
	"Select a.*, c.uomname from " ++ db ++ "." ++ products ++ " as a " ++
	"left join " ++ db ++ "." ++ uomQty ++ " as b on a.id = b.product_id " ++
	"left join " ++ db ++ "." ++ uom ++ " as c on b.packaging_id = c.id " ++
	"where a.supplier = '" ++ supplier ++ "' " ++
	"order by a.id" ++ lim

fun routeSql() =
	"Select a.*, b.userid, b.visit_frequency, b.visit_week, b.visit_day, b.status, d.saler_category " ++
	"from " ++ db ++ "." ++ routes ++ " as a " ++
	"left join " ++ db ++ "." ++ userRoutes ++ " as b on a.route_id = b.route_id " ++
	"left join " ++ db ++ "." ++ users ++ " as c on b.userid = c.id " ++
	"left join " ++ db ++ "." ++ userCategories ++ " as d on c.rep_category = d.usercategory " ++
	"where exists (Select 1 from " ++ productSupplierExistsRoutes ++ " as w where w.routeid = a.route_id) " ++
	"order by a.route_id" ++ lim

fun salesRepSql() =
	"Select a.*, b.saler_category from " ++ db ++ "." ++ users ++ " as a " ++
	"left join " ++ db ++ "." ++ userCategories ++ " as b on a.rep_category = b.usercategory " ++
	"where exists (Select 1 from " ++ productSupplierExistsUsers ++ " as w where w.userid = a.id) " ++
	"order by a.id" ++ lim

fun customerSql() =
	"Select a.* from " ++ db ++ "." ++ customers ++ " as a " ++
	"where a.Customer_Type = 'Customer' " ++
	"and exists (Select 1 from " ++ productSupplierExistsShops ++ " as w where w.SHOPID = a.SHOPID) " ++
	"order by a.SHOPID" ++ lim

fun stockSql() =
	"Select a.productcode, d.UOMName, b.stockpoint_name, MAX(b.date_created) as date_created, SUM(b.quantity) as quantity, SUM(b.total_cost) as total_cost " ++
	"from " ++ db ++ "." ++ products ++ " as a " ++
	"inner join " ++ db ++ "." ++ stockMovement ++ " as b on a.id = b.product_id " ++
	"left join " ++ db ++ "." ++ uomQty ++ " as c on b.product_id = c.product_id " ++
	"left join " ++ db ++ "." ++ uom ++ " as d on c.packaging_id = d.id " ++
	"where a.supplier = '" ++ supplier ++ "' " ++
	"group by a.id, d.UOMName, b.stockpoint_name " ++
	"order by a.id, d.UOMName, b.stockpoint_name" ++ lim

fun warehouseSql() =
	"Select c.* from " ++ db ++ "." ++ customers ++ " as c " ++
	"where c.CUSTOMER_TYPE = 'Supplier' " ++
	"order by c.SHOPID" ++ lim

var known =
	(endpoint == "invoice") or (endpoint == "order") or (endpoint == "product") or
	(endpoint == "route") or (endpoint == "sales-rep") or (endpoint == "salesrep") or
	(endpoint == "customer") or (endpoint == "store") or
	(endpoint == "stock") or (endpoint == "inventory") or
	(endpoint == "warehouse")

---
if ((not known) or (db == ""))
	""
else if (endpoint == "invoice") invoiceSql()
else if (endpoint == "order") orderSql()
else if (endpoint == "product") productSql()
else if (endpoint == "route") routeSql()
else if ((endpoint == "sales-rep") or (endpoint == "salesrep")) salesRepSql()
else if ((endpoint == "customer") or (endpoint == "store")) customerSql()
else if ((endpoint == "stock") or (endpoint == "inventory")) stockSql()
else if (endpoint == "warehouse") warehouseSql()
else ""
