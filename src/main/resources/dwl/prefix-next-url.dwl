%dw 2.0
output application/json
var expBase = p("papi.exp.datashare.base.url") default p("exp.base.url") default ""
var papiPath = vars.adapterPublicPath default ""
fun toExpNext(n) = do {
	var s = n as String default ""
	var q = if (s contains "?") ((s splitBy "?")[1] default "") else ""
	---
	expBase ++ papiPath ++ (if (q != "") ("?" ++ q) else "")
}
---
payload update {
	case .next if (payload.next != null) -> toExpNext(payload.next)
}
