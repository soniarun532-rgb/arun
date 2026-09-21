%dw 2.0
output application/java
import fromBase64 from dw::core::Binaries
import try from dw::Runtime

fun padB64(s) =
	s ++ ("=" * ((4 - (sizeOf(s) mod 4)) mod 4))

fun asText(v) =
	if (v == null)
		""
	else if (v is Array)
		trim((v[0] default "") as String)
	else
		trim((v as String) default "")

fun firstNonEmpty(values) =
	((values default []) filter ((v) -> asText(v) != ""))[0] default ""

fun headerByName(headers, wanted) = do {
	var wantedL = lower(wanted)
	var pairs = headers pluck ((v, k) -> { name: (k as String) default "", value: v })
	var hit = (pairs filter (lower($.name) == wantedL))[0]
	---
	asText(hit.value default "")
}

fun jwtPayload(authHeader) = do {
	var raw = asText(authHeader)
	var token = trim(if (lower(raw) startsWith "bearer ") raw[7 to -1] else raw)
	var part = (token splitBy ".")[1] default ""
	var normalized = (part replace "-" with "+") replace "_" with "/"
	var attempt =
		if (part == "")
			{ success: false }
		else
			try(() -> read((fromBase64(padB64(normalized)) as String {encoding: "UTF-8"}), "application/json"))
	---
	if (attempt.success default false)
		attempt.result default {}
	else
		{}
}

var headers = attributes.headers default {}
var authn = vars.oidcAuthentication default {}
var authnProps = authn.properties default {}
var authnClaims = authnProps.claims default authn.claims default {}
var auth = headerByName(headers, "authorization")
var jwt = jwtPayload(auth)
var headerClient = firstNonEmpty([
	headerByName(headers, "client_id"),
	headerByName(headers, "clientId"),
	headerByName(headers, "x-client-id"),
	headerByName(headers, "azp"),
	headerByName(headers, "appid")
])
var jwtClient = firstNonEmpty([
	jwt.azp,
	jwt.appid,
	jwt.cid,
	jwt.client_id,
	authnClaims.azp,
	authnClaims.appid,
	authnClaims.client_id,
	authnProps.azp,
	authnProps.appid,
	authnProps.client_id,
	authnProps.clientId,
	authn.principal,
	authn.clientId
])
var clientId = lower(asText(firstNonEmpty([headerClient, jwtClient])))
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
var headerKeys = headers pluck ((v, k) -> (k as String) default "")
---
{
	matched: hit != null,
	country: if (hit != null) hit.country else "",
	database: if (hit != null) hit.database else "",
	supplier: if (hit != null) hit.supplier else "",
	hasClientId: clientId != "",
	hasAuthHeader: auth != "",
	headerKeys: headerKeys,
	jwtKeys: jwt pluck ((v, k) -> (k as String) default "")
}
