%dw 2.0
output application/json
var rows = payload.data default payload default []
---
{
	data: rows map ((row) -> {
		StoreID: row.SHOPID default "",
		StoreName: row.CUSTOMERNAME default "",
		StoreCategory: row.CUSTOMERCATEGORY default "",
		Channel: row.CHANNEL default "",
		StoreClassification: row.CHANNEL default "",
		WarehouseID: "???",
		Longitude: row.LONGITUDE default "",
		Latitude: row.LATITUDE default "",
		City: row.LOCATIONNAME default "",
		Region: row.REGIONNAME default "",
		County: "",
		StoreStatus: row.STATUS default "",
		StoreCreationDate: if (row.DATECREATED == null) "" else ((row.DATECREATED as DateTime as String {format: "dd/MM/yyyy"}) default ""),
		StoreSize: ""
	}),
	(next: payload.next) if (payload.next != null)
}
