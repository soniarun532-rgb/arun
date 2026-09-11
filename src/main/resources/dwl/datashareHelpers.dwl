%dw 2.0

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
