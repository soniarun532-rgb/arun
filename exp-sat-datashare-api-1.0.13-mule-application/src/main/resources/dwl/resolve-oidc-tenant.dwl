%dw 2.0
output application/java
import substringAfter from dw::core::Strings
import fromBase64 from dw::core::Binaries

fun asText(v) =
	if (v == null)
		""
	else if (v is Array)
		trim((v[0] default "") as String)
	else
		trim((v as String) default "")

fun firstNonEmpty(values) =
	((values default []) filter ((v) -> asText(v) != ""))[0] default ""

fun jwtPayload(headers) = do {
	var raw = asText(headers["authorization"] default headers.authorization default "")
	var token = if (lower(raw) startsWith "bearer")
		trim(raw substringAfter " ")
	else
		raw
	var segments = token splitBy "."
	---
	if (sizeOf(segments) >= 2)
		read(fromBase64(segments[1]), "application/json")
	else
		{}
}

var headers = attributes.headers default {}
var jwt = jwtPayload(headers)
var clientId = lower(asText(firstNonEmpty([
	jwt.appid,
	jwt.azp,
	jwt.cid,
	jwt.client_id
])))
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
	hasClientId: clientId != "",
	hasAuthHeader: asText(headers["authorization"] default headers.authorization default "") != "",
	headerKeys: headers pluck ((v, k) -> (k as String) default ""),
	jwtKeys: jwt pluck ((v, k) -> (k as String) default "")
}
