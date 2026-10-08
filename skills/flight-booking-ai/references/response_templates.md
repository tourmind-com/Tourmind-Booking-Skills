# Canonical response templates

These English templates are the canonical structures for user-facing responses. Translate all user-facing headings, labels, guidance, and prose into the language of the user's current request unless another language was explicitly requested. Preserve Markdown structure, variables, proper names, URLs, currencies, identifiers, returned facts, and confirmation semantics. Do not output the English source alongside the translation unless the user requests bilingual output.

Populate only facts supported by the active request and authoritative API response. Keep a template field empty when its template permits missing data; never invent values. Never include a Token.

## Post-install guidance

Show this once after installation or on the first activation when installation guidance was not already shown. Replace the example date with a valid future date.

```markdown
### Flight Booking AI is ready

You can ask me like this:

> Find an Economy flight from Shanghai to Beijing on {future_date} for 3 adults, 1 child, and 0 infants.

Airport lookup and flight search are available without a Token. A Token is required for verification, booking, order queries, and payment:

- Personal users: sign in at https://auth.journione.ai to obtain a `uk_` Token.
- Business users: obtain an `sk_` Token at https://tourmind.com/user/skill-token. If you do not have a business account, register at https://tourmind.com/admin/skillSignup.

Send me the appropriate Token and I will configure it without displaying it back to you.
```

When authorization is already configured, replace the authorization block with:

```markdown
Authorization is configured. I will not display or repeat the stored Token.
```

## Authorization required

Use before any protected operation when no usable credential is configured. If the user type is known, show only the matching path; otherwise show both.

```markdown
Authorization is required before I can {protected_operation}.

- Personal users: sign in at https://auth.journione.ai to obtain a `uk_` Token.
- Business users: obtain an `sk_` Token at https://tourmind.com/user/skill-token. If you do not have a business account, register at https://tourmind.com/admin/skillSignup.

Send me the appropriate Token and I will configure it without displaying it back to you. No order has been created by this request.
```

## Update available

```markdown
### Flight Booking AI update available

Installed version: {current_version}
Latest version: {latest_version}

{release_change_summary}

Updating is recommended to obtain TourMind's latest flight-search, verification, booking, and payment behavior because older endpoints or operating rules may no longer remain available after a service update.

I can download the update from the official sources listed at {release_source_url}. Would you like me to update the installed Skill? I will not change it without your confirmation.
```

## Flight-offer results

Use for the initial result set and later pages. Keep the seven columns in this exact order. Repeat one aligned line per segment using `<br>`. Prefix every segment line with its translated journey label.

```markdown
| Offer | Flight | Departure–arrival (airport local time) | Departure terminal | Cabin | Checked baggage | Total |
| --- | --- | --- | --- | --- | --- | --- |
| {offer_number} | {journey_label}: {airline_name} ({flight_number}) | {journey_label}: {departure_time} {departure_airport_code} {departure_airport_name} → {arrival_time} {arrival_airport_code} {arrival_airport_name} | {journey_label}: {departure_terminal} | {journey_label}: {cabin_name} | {checked_baggage_summary} | {currency} {total_price} |
```

Use `Outbound` and `Return` for round-trip journey labels and `Trip 1`, `Trip 2`, and so on for multi-city labels before translation. For a one-way direct itinerary, a journey-label prefix may be omitted. Leave unsupported or unresolved cell content empty without inserting a placeholder.

When no offers are returned, use:

```markdown
No flight offers were returned for the confirmed search criteria. I have not changed the criteria or searched again. Tell me if you would like to adjust the request or approve another search.
```

## Offer verification result

```markdown
### Offer verification

| Item | Result |
| --- | --- |
| Price changed | {yes_or_no} |
| Verified total | **{currency} {verified_total_price}** |

This verification does not create a booking. If you want to continue, I will collect and review the required passenger and contact details before asking for booking confirmation.
```

## Unsupported passenger composition

```markdown
The actual group is {adults} adults, {children} children, and {infants} infants. This flight-booking flow permits at most one infant per actual accompanying adult and does not permit an infant to travel without an accompanying adult, so I cannot search or book this composition through the current flow. I will not add, remove, or relabel passengers.

Would you like to contact TourMind flight customer service to check whether the selected airline supports another arrangement? Eligibility cannot be promised until the airline's age and accompaniment policy is confirmed.
```

## Passenger-composition requotation

```markdown
The earlier quotation was based on {quoted_adults} adults, {quoted_children} children, and {quoted_infants} infants. The actual group is {actual_adults} adults, {actual_children} children, and {actual_infants} infants, so the earlier quotation and verification session are no longer valid.

If you confirm the actual passenger composition, I can run a new live search using those counts. No order has been created by this request.
```

## Passenger and contact collection

Repeat the passenger subsection for every passenger and replace `{passenger_number}` and `{passenger_type}`.

```markdown
To create a booking, I need the complete information shown on each passenger's travel document. Names must match the document exactly or boarding may be affected. Please provide all of the following in one message.

### Passenger {passenger_number} — {passenger_type}

- First name (given name):
- Last name (surname):
- Date of birth (`YYYY-MM-DD`):
- Sex:
- Nationality country code:
- Document type:
- Document number:
- Document expiry date (`YYYY-MM-DD`):
- Document issuing country/region code:
- Associated adult passenger number, for an infant only:

### Contact

- Name:
- Phone number, preferably including country/region code:
- Email:
```

## Shared review tables

Use these tables inside both booking and payment confirmations. Repeat the itinerary row for every segment and the passenger block for every passenger.

```markdown
### Itinerary

| Journey | Flight | Departure–arrival (airport local time) | Departure terminal | Cabin | Checked baggage |
| --- | --- | --- | --- | --- | --- |
| {journey_label} | {airline_name} ({flight_number}) | {departure_time} {departure_airport} → {arrival_time} {arrival_airport} | {departure_terminal} | {cabin_name} | {checked_baggage} |

### Passenger {index} — {type_label}

| Review item | Complete information |
| --- | --- |
| First name (given name) | {first_name} |
| Last name (surname) | {last_name} |
| Date of birth | {birthday} |
| Sex | {sex} |
| Nationality country code | {nationality} |
| Document type | {card_type} |
| Document number | {card_no} |
| Document expiry date | {card_expired} |
| Document issuing country/region code | {card_issue_place} |
| Associated adult, for an infant only | {associated_adult_passenger_number_and_name} |

### Contact

| Review item | Complete information |
| --- | --- |
| Name | {contact.name} |
| Phone | {contact.phone} |
| Email | {contact.email} |
```

## Booking confirmation

Render the shared review tables first, followed by:

```markdown
### Booking review

| Review item | Information |
| --- | --- |
| Passengers | {adults} adults, {children} children, {infants} infants |
| Price verification | {price_change_notice_from_price_changed} |
| Booking total | **{currency} {verified_total_price}** |

Please check that each First name and Last name appears in the correct field and matches the travel document exactly. Also check the itinerary, amount, passenger documents, and contact details. I will create the booking only after you explicitly confirm that all information above is correct.
```

## Payment-method labels

Use the canonical [payment-method mapping](parameter_guide.md#payment-method-mapping) for every user-visible payment-method selection, confirmation, creation result, and query result. The only public labels are Stripe, WeChat Pay, Alipay, and Online Banking. API values are request/response implementation details and must never appear in user-visible output.

Translate the generic label `Online Banking` naturally when appropriate, while preserving the product names Stripe, WeChat Pay, and Alipay. If a response contains an unrecognized string or number, do not show, transliterate, or guess from it. Omit the payment-method row and use the fixed fallback `The service did not return a recognized payment method.` translated into the response language.

## Payment before ticketing

Use for an existing-order next-step or ticket-issuance question only after the latest successful order query passes the payable-order gate. Show the normal order-query result, then this notice and the applicable payment-method selection or current payment review. Translate naturally into the customer's language.

```markdown
Your order {order_no} has been created. The order amount is {currency} {total_price}. Please complete payment first; you can then check the ticketing progress.

{payment_deadline_notice}
```

If a valid future deadline was returned, set `{payment_deadline_notice}` to `Please complete payment before {payment_deadline}.` Otherwise, when it was absent, use `The order did not return a payment deadline. Please complete payment as soon as possible.` Do not use this notice for an expired or unparseable deadline, already-paid/ticketed evidence, another order status, or a failed query. Never promise an issuance time or treat this guidance as consent to create a payment. If payment was already initiated, follow the existing payment-query reconciliation and returned-link rules instead of creating another payment.

## Payment-method selection

Use only after the latest order query passes the payable-order gate.

```markdown
### Choose a payment method

| Item | Information |
| --- | --- |
| Order number | {order_no} |
| Order currency | {currency} |
| Available payment methods | {available_public_payment_method_labels} |

If you choose Stripe, Stripe will charge an additional processing fee of 3.5% of the order amount. This processing fee is non-refundable if you later request a refund or cancel the order; after initiating payment, I will show the fee and total payable returned by the API.

Please select one of the available payment methods. The selected method will be included in the complete payment review before any payment link is created.
```

For `CNY`, `{available_public_payment_method_labels}` is `Stripe, WeChat Pay, Alipay, Online Banking`. For every other valid currency, it is `Stripe`; add `WeChat Pay, Alipay, and Online Banking are available only for CNY orders.` Translate that explanatory sentence into the response language.

Keep the complete Stripe reminder directly below the payment-method table and before the selection instruction, including when presenting payment methods after booking creation. Translate it without omitting the rate, non-refundable rule, or post-initiation fee/total display. Do not attach the fee to another method. If the API later omits the fee breakdown, use the payment-result fallback below rather than inventing an API-returned fee.

## Payment unavailable

```markdown
### Payment unavailable

| Item | Result |
| --- | --- |
| Order number | {order_no} |
| Current order status | {status} |
| Payment deadline | {payment_deadline_if_returned} |

No payment link was created. {payment_unavailable_reason}

{payment_unavailable_next_step}
```

Use exactly one translated reason appropriate to the authoritative query:

- Paid/ticketing/ticketed evidence: `This order is already paid or has moved beyond the payable stage, so I will not create another payment link.`
- Cancelled or creation failed: `This order cannot be paid in its current state.`
- Any other nonpayable or unfamiliar status: `The current status does not establish that this order is payable, so I will not create a payment link or assume that payment can be retried.`
- Deadline reached: `The returned payment deadline has been reached, so this order is no longer eligible for a new payment link.`
- Deadline cannot be interpreted reliably: `The returned payment deadline cannot be verified safely, so I will not create a payment link.`

For `{payment_unavailable_next_step}`, offer a later order query when a state may still change, a payment query when payment outcome needs reconciliation, or the [customer-service template](#customer-service) when the state cannot be resolved through the supported queries. If no deadline was returned, leave its cell empty; do not use the payment-review fallback here.

## Payment confirmation

Render the shared review tables with all data available for this order, followed by:

```markdown
### Payment review

| Review item | Information |
| --- | --- |
| Order number | {order_no} |
| Order status | {status} |
| Itinerary relationship | {route_dates_and_direct_or_transfer_summary} |
| Passengers | {adults} adults, {children} children, {infants} infants |
| Payment method | {selected_payment_method_label} |
| Flight order total | **{currency} {total_price}** |
| Payment deadline | **{payment_deadline_or_fallback}** |

{payment_deadline_reminder}

Please check the itinerary, passenger information, payment method, amount, and deadline. I will create the payment link only after you explicitly confirm that all information above is correct.
```

When a deadline is returned, set `{payment_deadline_or_fallback}` to that value and `{payment_deadline_reminder}` to `Complete payment before **{payment_deadline}**.` When absent, use `No payment deadline was returned; please pay as soon as possible.` for the fallback and leave the reminder empty.

When and only when Stripe is selected, insert this block after `{payment_deadline_reminder}` and before the final `Please check...` confirmation sentence in the payment-review output:

```markdown
### Stripe fee acknowledgement

| Item | Information |
| --- | --- |
| Flight order total | **{currency} {total_price}** |
| Stripe processing fee (3.5%) | **{currency} {processing_fee}** |
| Total payable including Stripe fee | **{currency} {payable_total}** |

{fee_amount_source_notice}

Stripe—not the airline or TourMind—adds this payment-processing fee. Once charged, the Stripe processing fee is non-refundable, even if the flight order or fare later qualifies for cancellation or a refund.

Please explicitly confirm the Stripe processing fee of **{currency} {processing_fee}**, the total payable of **{currency} {payable_total}**, and that this processing fee is non-refundable even if you later request a refund or cancel the order.
```

Populate `{processing_fee}` and `{payable_total}` using the [fee calculation rules](parameter_guide.md#fee-calculation-before-payment-confirmation): decimal half-up rounding of `total_price * 0.035` to two places, then add the rounded fee to `total_price`. Show all three monetary values with exactly two decimal places. Set `{fee_amount_source_notice}` to `The fee and total payable above are calculated from the current order amount; after payment initiation, I will show the amounts returned by the service.` When the service has already returned an authoritative fee/payable breakdown for this order and method, use it instead and set the notice to `The fee and total payable above were returned by the service.` This Stripe acknowledgement is part of the complete payment review; the customer must confirm both.

## Booking creation result

Render the final itinerary using the flight-offer structure, followed by:

```markdown
### Booking created

| Item | Result |
| --- | --- |
| Order number | {order_no} |
| Order status | {status} |
| Price changed | {yes_or_no} |
| Total | **{currency} {total_price}** |

The status above is exactly what the service returned. It does not by itself prove payment or ticket issuance.
```

## Order query result

Render the returned itinerary summary first, followed by:

```markdown
### Order details

| Item | Result |
| --- | --- |
| Order number | {order_no} |
| Status | {status} |
| Passengers | {adults} adults, {children} children, {infants} infants |
| Total | **{currency} {total_price}** |
| Payment deadline | {payment_deadline} |

The status above is exactly what the service returned. No payment or ticketing outcome is inferred from another field.
```

If the deadline is absent, leave that cell empty. For questions about ticket issuance or next steps on a payable order, continue with [payment before ticketing](#payment-before-ticketing) rather than ending with only the status table or a support referral.

## Payment creation result

```markdown
### Payment link created

| Item | Result |
| --- | --- |
| Order number | {order_no} |
| Payment status | {status} |
| Payment method | {payment_method_label} |
| Total payable returned by the service | **{currency} {amount}** |

Payment link: {payment_url}

The payment link is a payment destination; it does not prove that payment succeeded or that a ticket was issued.
```

If no URL is returned, replace the payment-link line with `The response did not return a payment link.`

Map the returned method through [payment-method labels](#payment-method-labels). If it is unrecognized, omit the payment-method row and append the fixed unrecognized-method fallback defined there.

For Stripe, insert a `Stripe processing fee` row immediately before the total-payable row. Use the explicitly returned fee in the returned currency with two decimal places, or the fixed fallback `The API did not return a separate fee breakdown.` Never label a local calculation as an API-returned fee. `{amount}` is the authoritative payable total; never add a fee to it. For payments created with the current flight fee logic it already includes the Stripe fee; do not infer a fee for historical records. If a returned total or explicit fee differs from the confirmed review, show the difference and obtain confirmation before directing the customer to pay; do not create another payment.

## Payment query result

```markdown
### Payment status

| Item | Result |
| --- | --- |
| Order number | {order_no} |
| Payment status | {status} |
| Payment method | {payment_method_label} |
| Total payable returned by the service | **{currency} {amount}** |

The status above is exactly what the service returned. It is the only basis for reporting the payment outcome and does not by itself prove ticket issuance.
```

Map the returned method through [payment-method labels](#payment-method-labels). If it is unrecognized, omit the payment-method row and append the fixed unrecognized-method fallback defined there.

For Stripe, insert a `Stripe processing fee` row immediately before the total-payable row. Use the explicitly returned fee in the returned currency with two decimal places, or the fixed fallback `The API did not return a separate fee breakdown.` Never label a local calculation as an API-returned fee. `{amount}` is the authoritative payable total; never add a fee to it. For payments created with the current flight fee logic it already includes the Stripe fee; do not infer a fee for historical records. If a returned total or explicit fee differs from the confirmed review, show the difference and obtain confirmation before directing the customer to pay; do not create another payment.

## Authentication recovery

Use the acquisition path matching the rejected credential. If its channel is unknown, include both paths.

```markdown
Authentication was rejected, so {operation_outcome}. I cleared the rejected Token and will not retry the operation automatically. {authorization_path} Send me the replacement Token and I will configure it without displaying it. I will continue only after you explicitly request or approve the next operation and its normal checks are complete. {order_state}
```

Use one authorization path:

- Personal: `Sign in at https://auth.journione.ai to obtain a new personal Token.`
- Business: `Obtain a new business Token at https://tourmind.com/user/skill-token. If you do not have a business account, register at https://tourmind.com/admin/skillSignup.`
- Unknown: include both personal and business paths from the authorization-required template.

Set `{operation_outcome}` to `{protected_operation} did not complete` for a read-only/preflight operation or when authoritative evidence confirms that creation did not occur. If a booking or payment creation request may have been dispatched and its outcome is not authoritative, set it to `{protected_operation} could not be confirmed`. Set `{order_state}` from evidence, for example `No booking request was sent, so this request did not create an order.` Never claim that no order exists after an ambiguous booking response. Supplying a replacement Token does not by itself authorize replaying a failed search, booking, or payment operation.

## Token-change quotation refresh

Use after a successful refresh caused by a new or changed `sk_` token since search plus a request to verify, or by a verification business `code == 20105`. No extra search approval is needed. Render the normal flight-offer results table from the latest response and include this notice, translated into the user's language:

```markdown
Because the token changed, I have retrieved updated quotations. Please choose a quotation from the new results so I can verify it.
```

Wait for a new selection before verification, even when the original flight uniquely matches or its price is unchanged. Do not report that verification succeeded. Do not expose internal agent codes, backend routing, token fragments, raw error codes, or diagnostics. If the refresh fails, explain that updated quotations could not be retrieved. If it succeeds with no offers, explain that the refreshed search found none and use the normal no-offers response. Neither case permits fallback to old offers or an automatic repeat search. Preserve any known order or uncertain creation state.

## Failure and reconciliation

Verification failure before booking:

For the first verification `code == 20105`, use the token-change quotation refresh template above. If that one-cycle recovery fails, report the failed refresh without starting another automatic search.

```markdown
This offer could not be confirmed and has been removed from the selectable offers. No booking request was sent. If you approve, I can run a new live search using the confirmed itinerary.
```

Ambiguous booking result without a confirmed order number:

```markdown
Booking creation could not be confirmed. The service did not return a confirmed order number, so it is currently unknown whether an order was created. Contact TourMind flight customer service to reconcile the attempt before trying to book again and avoid a duplicate order.
```

Ambiguous payment result for a known order:

```markdown
Order number: {order_no}. The payment operation could not be confirmed, so the payment status is currently unknown. I will query the payment status before any further payment-creation attempt.
```

## Unsupported operation

Use this for requests to perform an unsupported action. A question about next steps or ticketing progress on an existing order must first follow the order-query and [payment-before-ticketing guidance](#payment-before-ticketing); do not classify it as unsupported merely because it mentions tickets.

```markdown
This Skill cannot perform {requested_operation}. Baggage purchases, seat selection, cancellation, changes, refund initiation, manual payment, and ticketing require assistance from TourMind flight customer service.

TourMind flight customer service is available 24/7. Email: flightcs1@tourmind.com
```

## Customer service

```markdown
TourMind flight customer service is available 24/7. Email: flightcs1@tourmind.com
```

## Refund and change

```markdown
Tickets cannot be refunded or changed after payment. Contact TourMind flight customer service for details. TourMind flight customer service is available 24/7. Email: flightcs1@tourmind.com
```
