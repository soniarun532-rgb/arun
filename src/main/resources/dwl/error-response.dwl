%dw 2.0
output application/json
---
{
  error: {
    code: vars.errorCode default "INTERNAL_SERVER_ERROR",
    message: vars.errorMessage default (error.description default "An unexpected error occurred while processing the request"),
    correlationId: vars.correlationId default uuid(),
    timestamp: now() as String { format: "yyyy-MM-dd'T'HH:mm:ss.SSSXXX" }
  }
}
