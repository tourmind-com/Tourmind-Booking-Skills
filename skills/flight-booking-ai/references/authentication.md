# Authentication failure and recovery

Read this reference after an authentication rejection, but only after excluding the dedicated ToB business-permission condition. A business-channel response with `code == 20105` means the `sk_` Token was accepted but business flight-booking access is not enabled; keep the Token and follow the permission rule in `SKILL.md`, even if its HTTP status or message also resembles an authentication failure. For every other HTTP 401, `unauthorized`, or `invalid_token` result, authentication recovery takes precedence over transport retries and ordinary retry requests.

## Clear the rejected credential and stop

Immediately clear the rejected `{baseDir}/skill_token.txt` value and remove it from reusable request headers or client state. Stop the affected operation and do not retry it automatically. Do not print any credential while reading, clearing, or saving it.

Never reuse the rejected credential, send an empty or guessed header, silently switch channels, change the API host or endpoint, or search another installation, workspace, archive, backup, environment variable, shell history, previous message, or account for replacement credentials. A request to hurry, accept risk, change the itinerary, or “try once” does not authorize another call with the rejected token.

Public airport lookup remains available without a token. A public lookup or Skill update check does not prove flight authorization and does not resume the failed protected operation.

## Obtain and use a replacement token

Direct a personal-channel user to <https://auth.journione.ai> to obtain a new `uk_` token. Direct a business-channel user to <https://tourmind.com/user/skill-token> to obtain a new `sk_` token; if they do not have a business account, provide <https://tourmind.com/admin/skillSignup>. If the rejected credential's channel is unknown, present both choices without selecting one for the user.

When the user supplies a complete replacement beginning `uk_` or `sk_`, save it securely to `{baseDir}/skill_token.txt` without echoing it. The prefix selects the channel, but receiving or saving the token does not prove authorization and does not by itself authorize any endpoint call.

Do not invent a validation endpoint, call a server-internal verifier, or automatically issue a protected request solely because the replacement was saved. The replacement may be used for the next protected operation only when the user explicitly requests or approves that operation and its normal input validation, quotation freshness, channel, review, and confirmation requirements are satisfied. If the user explicitly asks to test the replacement, use only a documented read-only protected operation with complete valid inputs; never use `create_booking` or `create_payment` as a credential test.

Treat the official endpoint response as authoritative. First exclude the exact ToB `code == 20105` permission condition, which keeps the credential. If the response instead returns any other HTTP 401, `unauthorized`, or `invalid_token`, clear the replacement credential and restart this recovery flow. Otherwise, handle the response under its normal success, business-error, or transport-error rules without claiming more authorization than the response establishes.

## Resume the business workflow safely

Replacing a token invalidates pre-order quotations, verification sessions, passenger/contact confirmations, and payment context as required by `SKILL.md`. Obtain approval for a fresh search and repeat verification before any later booking. An existing order remains bound to its creation channel and requires a matching-prefix credential authorized to access it; never probe the other channel.

Never automatically replay `create_booking` or `create_payment` after authentication recovery. If an earlier creation result was ambiguous, reconcile it before considering another creation. Any later booking or payment creation must satisfy the complete current review and explicit-confirmation flow.

## Customer-facing response

Use the [authentication recovery template](response_templates.md#authentication-recovery). Select its operation outcome, authorization path, and order-state variables from actual evidence. If an existing order is known, retain its confirmed number and explain which follow-up action stopped. If an earlier creation is uncertain, retain that uncertainty. Do not show raw authentication errors or any token fragment.
