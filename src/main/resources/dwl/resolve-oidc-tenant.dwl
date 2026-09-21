%dw 2.0
output application/java
import fromBase64 from dw::core::Binaries

fun padB64(s) =
	s ++ ("=" * ((4 - (sizeOf(s) mod 4)) mod 4))

fun jwtPayload(authHeader) = do {
	var raw = (authHeader default "") as String
	var token = trim(if (lower(raw) startsWith "bearer ") raw[7 to -1] else raw)
	var part = (token splitBy ".")[1] default ""
	var normalized = (part replace "-" with "+") replace "_" with "/"
	---
	if (part == "")
		{}
	else
		try(() -> read((fromBase64(padB64(normalized)) as String {encoding: "UTF-8"}), "application/json")) default {}
}

var headers = attributes.headers default {}
var auth = headers.authorization default headers.Authorization default ""
var jwt = jwtPayload(auth)
var clientId = lower(trim((
	headers.client_id default headers.clientId default headers['x-client-id']
	default jwt.azp default jwt.appid default jwt.cid default jwt.client_id
	default ""
) as String))
var tenantKeys = ((p("exp.sat.oidc.tenants") default "") as String)
	splitBy ","
	map ((k) -> trim(k))
	filter ((k) -> k != "")
var matches = tenantKeys map ((k) -> {
	country: k,
	clientId: lower(trim((p("exp.sat.oidc." ++ k ++ ".client-id") default "") as String)),
	database: trim((p("exp.sat.oidc." ++ k ++ ".database") default "") as String),
	supplier: trim((p("exp.sat.oidc." ++ k ++ ".supplier") default "") as String)
}) filter ((t) -> (t.clientId != "") and (t.clientId == clientId))
var hit = matches[0]
---
{
	matched: hit != null,
	country: if (hit != null) hit.country else "",
	database: if (hit != null) hit.database else "",
	supplier: if (hit != null) hit.supplier else "",
	hasClientId: clientId != ""
}
