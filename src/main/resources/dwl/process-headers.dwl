%dw 2.0
output application/java
---
{
  client_id: p('secure::process.api.clientId'),
  client_secret: p('secure::process.api.clientSecret'),
  "X-Correlation-Id": vars.correlationId,
  Accept: "application/json"
}
