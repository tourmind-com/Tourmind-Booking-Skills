# Flight HTTP Parameter Guide

This is the request and response contract for Flight Booking AI. It is derived from the current Go DTOs and service validation. Do not add supplier-only fields or send `AgentCode`; the server supplies its own agent code.

## Transport, authentication, and envelope

- **Base URL:** `https://airxapi.hlzinterface.cn`
- **Method and body:** every endpoint is `POST` with a JSON request body (`Content-Type: application/json`).
- **Protected-request header:** `X-Skill-Token: uk_...` for the personal channel or `X-Skill-Token: sk_...` for the business channel. Never put either token in the flight request JSON body or URL.
- **Success condition:** a response succeeds only when its envelope has `code == 0`. A nonzero `code` is a failure even if the HTTP status is 200.
- **Business-flight permission condition:** on the business channel, `code == 20105` means the `sk_` Token was accepted but the account has not enabled flight-booking access. Handle this exact code before generic authentication or nonzero-code rules.

```json
{"code":0,"message":"success","data":{}}
```

| Credential state | Flight channel | Protected-request behavior |
| --- | --- | --- |
| Missing or empty | None | Airport lookup remains public; stop all other operations and show both personal and business authorization choices. |
| Begins with `uk_` | Personal (ToC) | Send the complete token only in `X-Skill-Token`. |
| Begins with `sk_` | Business (ToB) | Send the complete token only in `X-Skill-Token`. |
| Any other value | Unrecognized | Send no protected request; ask for a complete `uk_` or `sk_` token. |

| Operation | Path | Authentication |
| --- | --- | --- |
| Airport lookup | `/skill/flight/v1/search_airports` | Public; do not send `X-Skill-Token`. |
| Flight search | `/skill/flight/v1/search_flights` | Protected; send `X-Skill-Token`. |
| Offer verification | `/skill/flight/v1/verify_offer` | Protected; send `X-Skill-Token`. |
| Booking creation | `/skill/flight/v1/create_booking` | Protected; send `X-Skill-Token`. |
| Payment creation | `/skill/flight/v1/create_payment` | Protected; send `X-Skill-Token`. |
| Payment query | `/skill/flight/v1/query_payment` | Protected; send `X-Skill-Token`. |
| Order query | `/skill/flight/v1/query_order` | Protected; send `X-Skill-Token`. |

The personal and business channels use the same flight Base URL and endpoint paths. The server verifies `X-Skill-Token`, selects the account channel from the token, and derives `AgentCode` and `CreatorUser` before processing a protected operation. Even for a `uk_` token, do not send `user_key`, `AgentCode`, or `CreatorUser` in the JSON request.

A search, quotation, verification session, booking confirmation, order, and payment context belongs to the credential channel that created it. Changing the active token, especially between `uk_` and `sk_`, invalidates pre-order quotations, sessions, and confirmations and requires a user-approved fresh search and verification. Existing order and payment operations must remain on the creation channel with a matching-prefix credential authorized to access the order; never probe both channels.

After an authentication failure, follow [authentication recovery](authentication.md): clear the rejected credential and reusable header, stop the affected operation, and do not retry it automatically. This endpoint list contains no independent public credential-validation endpoint; do not invent or call a server-internal verifier, and never use booking or payment creation to test a replacement token. A newly supplied token may be used only for the next protected operation the user explicitly requests or approves, after that operation's normal validations and confirmations. The official endpoint response is authoritative; another authentication rejection clears the replacement and restarts recovery.

Do not route a ToB response with business `code == 20105` into authentication recovery, even if its HTTP status or message contains authentication-like wording. Keep `{baseDir}/skill_token.txt` and the reusable header. Stop the permission-gated booking workflow, do not retry or switch channels, and use the [business-flight-permission template](response_templates.md#business-flight-booking-access-required). The user may still request flight-price searches. After they report that access was enabled, require an explicit request and start again with a new live search before verification or booking.

## Airport lookup

### `POST /skill/flight/v1/search_airports`

Request (`keyword` is required):

```json
{"keyword":"Shanghai"}
```

`data` is an airport result:

| Field | Type | Meaning |
| --- | --- | --- |
| `list` | array | Matched city records. |
| `total` | integer | Total matched city records. |

Each item in `list` has every field below:

| Field | Type | Meaning |
| --- | --- | --- |
| `city_code` | string | City code. |
| `city_cn` | string | Chinese city name. |
| `city_en` | string | English city name. |
| `country_cn` | string | Chinese country name. |
| `country_en` | string | English country name. |
| `country_code` | string | Country code. |
| `match_city` | boolean | Whether the lookup matched the city itself. |
| `airports` | array | Airport records in that city. |

Each item in `airports` has:

| Field | Type | Meaning |
| --- | --- | --- |
| `s_region_id` | string | Supplier region identifier returned for the airport. |
| `airport_code` | string | Airport code; use this value in a flight-search leg only when the user specifies this airport. |
| `airport_cn` | string | Chinese airport name. |
| `airport_en` | string | English airport name. |

For a flight-search leg, use the matched city's `city_code` when the user accepts any airport in that city. Use an airport's `airport_code` only when the user specifies that airport. `s_region_id` is supplier-facing lookup data, not a user-visible identifier.

## Flight search

### `POST /skill/flight/v1/search_flights`

Protected request example:

```http
X-Skill-Token: uk_or_sk_redacted
```

```json
{
  "trip_type":"round_trip",
  "flight_type":"direct",
  "cabin_class":"Y",
  "adults":1,
  "children":0,
  "infants":0,
  "legs":[
    {"departure":"SHA","arrival":"BJS","departure_date":"2026-09-10"},
    {"departure":"BJS","arrival":"SHA","departure_date":"2026-09-15"}
  ]
}
```

| Field | Required | Rules |
| --- | --- | --- |
| `trip_type` | Yes | `one_way`, `round_trip`, or `multi_city`. A one-way trip has exactly 1 leg, a round trip exactly 2, and multi-city at least 2. |
| `flight_type` | No | `all`, `direct`, or `transfer`; omitted or blank defaults to `all`. `direct` keeps offers whose every journey has zero transfers. `transfer` keeps offers with at least one journey whose transfer count is greater than zero. |
| `cabin_class` | No | `Y`, `C`, or `F`; omitted or blank defaults to `Y`. |
| `adults` | Yes | Integer at least 1. |
| `children` | No | Integer at least 0. |
| `infants` | No | Integer from 0 through `adults`. At most one infant per actual accompanying adult; no infant-only purchase. Reject unsupported compositions before calling the endpoint; never change real counts or age types to pass validation. |
| `legs` | Yes | Array whose length matches `trip_type`. |
| `legs[].departure` | Yes | Three-letter IATA code (ASCII letters); normalized to uppercase and must differ from `arrival`. |
| `legs[].arrival` | Yes | Three-letter IATA code (ASCII letters); normalized to uppercase and must differ from `departure`. |
| `legs[].departure_date` | Yes | Valid `YYYY-MM-DD`. Before calling flight search, require `today <= departure_date <= latest_date` in the user's timezone, where `latest_date` is today plus one calendar year. Both boundaries are inclusive: same-day flights are searchable. Compare calendar dates rather than midnight to the current time. Validate every leg and require nondecreasing dates; if any leg is invalid, stop the whole search and request correction without changing dates automatically. |

Date-boundary examples (assume the user's local date is `2026-09-09`; recompute the range at runtime):

| Requested date | Pre-search decision |
| --- | --- |
| `2026-09-08` | Reject as past; request a corrected date without calling flight search. |
| `2026-09-09` | Allow today, even when the current time is later than midnight. |
| `2027-09-09` | Allow the inclusive one-year boundary. |
| `2027-09-10` | Reject as beyond one year; request a corrected date without calling flight search. |
| Outbound `2026-09-10`, return `2026-09-09` | Reject the whole search because leg dates decrease, although each date individually lies within the range. |

`data` contains:

| Field | Type | Meaning |
| --- | --- | --- |
| `offers` | array of `FlightOffer` | Matching non-null offers sorted by `total_price` ascending, limited to the cheapest 50. Offers with equal prices preserve their upstream order. |
| `total` | integer | Total matching non-null offers before the 50-offer response limit. |

### `FlightOffer` response fields

`FlightOffer` is returned by search, verification, and booking. Decimal price values currently serialize as JSON **strings**, not JSON numbers.

| Field | Type | Meaning |
| --- | --- | --- |
| `offer_id` | string | Offer identifier used internally for verification; do not show it to the user. |
| `currency` | string | Offer currency. |
| `total_price` | string decimal | Total price. |
| `adults` | integer | Adult count priced in the offer. |
| `children` | integer | Child count priced in the offer. |
| `infants` | integer | Infant count priced in the offer. |
| `adult_fare` | string decimal | Adult base fare. |
| `adult_tax` | string decimal | Adult tax. |
| `child_fare` | string decimal | Child base fare. |
| `child_tax` | string decimal | Child tax. |
| `infant_fare` | string decimal | Infant base fare. |
| `infant_tax` | string decimal | Infant tax. |
| `journeys` | array of `FlightJourney` | Journey summaries. |
| `segments` | array of `FlightSegment` | Flight segments. |
| `baggage` | array of `FlightBaggage` | Baggage rules. |

Each `journeys` item contains:

| Field | Type | Meaning |
| --- | --- | --- |
| `index` | integer | Journey index. |
| `departure_city` | string | Departure city. |
| `departure_airport` | string | Departure airport. |
| `arrival_city` | string | Arrival city. |
| `arrival_airport` | string | Arrival airport. |
| `transfer_count` | integer | Number of transfers. |
| `duration_minutes` | integer | Journey duration in minutes. |

Each `segments` item contains:

| Field | Type | Meaning |
| --- | --- | --- |
| `index` | integer | Segment index. |
| `group` | integer | Journey/group index for the segment. |
| `airline` | string | Marketing airline. |
| `flight_no` | string | Marketing flight number. |
| `operating_airline` | string | Operating airline. |
| `operating_flight_no` | string | Operating flight number. |
| `cabin_class` | string | Display this segment's returned cabin in search results: `Y` → Economy, `C` → Business, `F` → First, translated into the response language. Do not substitute the requested cabin or another segment's cabin. |
| `cabin_code` | string | Cabin/booking code. |
| `available_seats` | integer | Available seat count. |
| `departure_city` | string | Departure city. |
| `departure_airport` | string | Departure airport. |
| `departure_terminal` | string | Departure terminal. |
| `departure_time` | string | Provider-supplied departure time; display with this segment’s flight number, arrival time, and cabin in every search-results presentation. |
| `arrival_city` | string | Arrival city. |
| `arrival_airport` | string | Arrival airport. |
| `arrival_terminal` | string | Arrival terminal. |
| `arrival_time` | string | Provider-supplied arrival time for the same segment. Display it alongside departure time; retain returned dates for overnight/cross-date travel and any returned timezone information. |
| `duration_minutes` | integer | Segment duration in minutes. |

Each `baggage` item contains:

| Field | Type | Meaning |
| --- | --- | --- |
| `segment_index` | integer | Segment index to which the rule applies. |
| `passenger_type` | string | `adult`, `child`, `infant`, or `unknown`. |
| `type` | string | `checked`, `carry_on`, `cabin`, or `unknown`. |
| `pieces` | integer | Included piece count. |
| `weight_kg` | integer | Included weight in kilograms. |
| `size` | string | Size allowance. |
| `description` | string | Provider rule text. |

## Offer verification

### `POST /skill/flight/v1/verify_offer`

Protected request:

```http
X-Skill-Token: uk_or_sk_redacted
```

```json
{"offer_id":"offer-1","adults":1,"children":0,"infants":0}
```

`offer_id` and `adults` are required. Counts use the same constraints as flight search: adults >= 1, children >= 0, infants >= 0, and infants <= adults.

Apply the [passenger-composition gate](passenger_details.md#passenger-composition-gate) before search, verification, and booking. A numerically valid request does not prove that airline age/accompaniment policy permits an alternative; obtain the user's preference before pursuing alternatives and verify the relevant policy before promising eligibility.

`data` fields:

| Field | Type | Meaning and required action |
| --- | --- | --- |
| `offer` | `FlightOffer` | The authoritative, currently verified itinerary and price details. |
| `session_id` | string | Authoritative session to use for one booking request. |
| `price_changed` | boolean | Whether price changed; surface it and obtain confirmation of the verified amount. |
| `rule_changed` | boolean | Ignored by this Skill. Do not display, interpret, branch on, or request confirmation based on this field; it does not change the booking workflow. |
| `support_no_card` | boolean | API capability to omit document/card fields. This Skill still requires complete travel-document details before booking. |

The returned `offer`, `total_price`, `currency`, and `session_id` are authoritative. Verification is not booking approval: present the verified result and obtain explicit final confirmation before creating a booking.

On a ToB verification response with business `code == 20105`, do not treat the Token as invalid and do not describe the offer as unavailable. The account may search price information, but it cannot proceed through verification to booking until business flight-booking access is enabled. Clear any verification or booking-confirmation state for the selected offer, keep the search result only as informational price output until its normal expiry, and follow the dedicated permission rule above.

## Booking creation

### `POST /skill/flight/v1/create_booking`

Protected request example (one adult passenger; `agent_order_no` is optional):

```http
X-Skill-Token: uk_or_sk_redacted
```

```json
{
  "session_id":"session-verified-1",
  "agent_order_no":"client-order-20260910-001",
  "passengers":[
    {
      "index":1,
      "type":"adult",
      "first_name":"Ming",
      "last_name":"Zhang",
      "birthday":"1990-01-15",
      "sex":"male",
      "nationality":"CN",
      "card_type":"PP",
      "card_no":"E12345678",
      "card_expired":"2030-01-15",
      "card_issue_place":"CN",
      "associated_index":0
    }
  ],
  "contact":{
    "name":"Ming Zhang",
    "phone":"+86 13800138000",
    "email":"ming.zhang@example.com",
    "address":"1 Example Road",
    "area_code":"86"
  }
}
```

Top-level fields:

| Field | Required | Rules |
| --- | --- | --- |
| `session_id` | Yes | Nonblank verified session ID. Use the authoritative value from verification. |
| `agent_order_no` | No | Optional client/agent order number. |
| `passengers` | Yes | Nonempty passenger array. Do not send an ancillary-items field. |
| `contact` | Yes | Contact object described below. |

Every passenger uses these fields:

| Field | Required | Rules |
| --- | --- | --- |
| `index` | Yes | Must be sequential: 1, 2, 3, … in array order. |
| `type` | Yes | `adult`, `child`, or `infant` (case-insensitive input). The Skill checks age on the travel date: adult >= 12 years; child >= 2 and < 12 years; infant >= 14 days and < 2 years. Must match actual passenger details and the searched/verified composition. |
| `first_name` | Yes | Nonblank after trimming. Travel-document given name; collect and confirm separately as `First name (given name)`. |
| `last_name` | Yes | Nonblank after trimming. Travel-document surname; collect and confirm separately as `Last name (surname)`. |
| `birthday` | Yes | Valid calendar date in `YYYY-MM-DD`; reconcile age and passenger type before booking. Never alter a birthday or relabel a child/infant to fit an adult quotation. |
| `sex` | Yes | `male` or `female` (case-insensitive input). |
| `nationality` | Yes | Two- or three-letter uppercase country code; input is normalized to uppercase. |
| `card_type` | Conditional | With the other three document fields, either all are blank or all are present. If present: `ID`, `PP`, `GA`, `TW`, `TB`, `HX`, `HY`, or `UN`. |
| `card_no` | Conditional | Required when any document/card field is supplied; otherwise blank with all of them. |
| `card_expired` | Conditional | Required with all document/card fields; valid `YYYY-MM-DD`. |
| `card_issue_place` | Conditional | Required with all document/card fields; two- or three-letter country code, normalized to uppercase. |
| `associated_index` | Yes | `0` for adults and children. For an infant, the index of an adult passenger. Each adult may be associated with at most one infant. |

The table's conditional document fields describe API validation. This Skill's booking flow requires all four document fields even when `support_no_card: true`. Apply [passenger details and confirmation](passenger_details.md) and use the canonical [passenger collection and review templates](response_templates.md). Warn that names must match the travel document or boarding may be affected, and show First name and Last name separately in the final confirmation tables with complete unmasked passenger, document, and contact details. If the actual composition differs from the quote, follow the requotation flow before booking. The request has no ancillary field: the server sends an empty ancillary list.

`contact` fields:

| Field | Required | Rules |
| --- | --- | --- |
| `name` | Yes | Nonblank after trimming. |
| `phone` | Yes | 5–32 characters; at least one digit; only digits, `+`, `-`, space, `(`, and `)`; at most one `+`, which may appear only at the start. |
| `email` | Yes | No whitespace/control characters; exactly one `@`; nonblank local part; domain contains a dot and does not begin or end with one. |
| `address` | No | Optional address. |
| `area_code` | No | Optional area code. |

`data` fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `order_no` | string | Created booking order number. |
| `status` | string | Current booking status; do not claim payment or ticketing beyond this value. |
| `currency` | string | Order currency. |
| `total_price` | string decimal | Authoritative order total; decimals serialize as JSON strings. |
| `price_changed` | boolean | Whether the price changed during creation. |
| `offer` | `FlightOffer` | Final returned offer. |

Emitted `status` values are: `pending_confirmation`, `booking_successful`, `payment_successful`, `ticketing`, `payment_failed`, `ticket_issued`, `ticketing_failed`, `cancelled`, `creation_failed`, and `unknown`.

## Third-party payment creation and query

### `POST /skill/flight/v1/create_payment`

This protected endpoint creates a third-party payment URL for a booked order. Query the order and pass the [payable-order gate](#payable-order-gate) before offering a payment method. Then apply the [payment confirmation data rules](passenger_details.md#payment-confirmation), present the canonical [payment confirmation template](response_templates.md#payment-confirmation) with full available passenger/document/contact values, and obtain a separate explicit confirmation. Immediately before calling this endpoint, query the order again, reapply the complete gate, and confirm that every reviewed fact is unchanged. When that final query is unchanged, proceed directly to the single creation call without another user-visible or deferred step. The caller never supplies an amount, currency, agent, operator, or payment return URL; the server derives or supplies those values.

```json
{
  "order_no":"TM202609030001",
  "payment_method":"stripe"
}
```

| Field | Required | Rules |
| --- | --- | --- |
| `order_no` | Yes | Nonblank after trimming. |
| `payment_method` | Yes | Request-only API value. Case-insensitive input is normalized to one of `stripe`, `yeepay_wechat`, `yeepay_alipay`, or `yeepay_bank`. Never show this value to the user. |

Do not ask the user for or send `return_url`; the service supplies the payment return URL.

#### Payment-method mapping

Payment methods use these canonical display mappings and order-currency constraints:

| Public user-visible label | Request-only API value | Queried order currency |
| --- | --- | --- |
| Stripe | `stripe` | Any valid returned currency. |
| WeChat Pay | `yeepay_wechat` | `CNY` only. |
| Alipay | `yeepay_alipay` | `CNY` only. |
| Online Banking | `yeepay_bank` | `CNY` only. |

The API value is used only in request construction and internal response mapping. Never display it, the payment-provider implementation name, or any numeric upstream code. Availability must be derived from the immediately preceding eligible `query_order` result. If its currency is not exactly `CNY`, present only Stripe. Use the canonical [payment-method selection template](response_templates.md#payment-method-selection).

Stripe adds a separate payment-processing fee equal to 3.5% of the flight order total. The fee applies only to Stripe and is not airfare, tax, an airline charge, or a TourMind booking surcharge. Once charged, it is non-refundable even if the flight order or fare later qualifies for cancellation or a refund. Disclose the rate and non-refundable rule and obtain explicit acknowledgement before `create_payment`.

#### Fee calculation before payment confirmation

For Stripe, use `total_price` and `currency` from the latest eligible `query_order` response. Calculate with decimal arithmetic: `processing_fee = round_half_up(total_price * 0.035, 2)` and `payable_total = total_price + processing_fee`. Round the fee first, then add it to the order total; display all amounts in the order currency with exactly two decimal places. This matches the flight service's `paymentServiceFee` calculation. For example, an order of `12.34` has a fee of `0.43` and a payable total of `12.77`; an order of `1.00` has a fee of `0.04` and a payable total of `1.04` (half-cent rounds up).

Before `create_payment`, show the order total, 3.5% rate, numeric fee, numeric payable total, and non-refundable-fee notice in the complete payment review. Identify locally calculated values as the pre-payment calculation, not as values already returned by the payment API. Obtain explicit confirmation of the fee amount, payable total, and non-refundable nature. If an authoritative fee/payable breakdown for the same order and selected method is already returned, show those values instead. Recalculate and renew confirmation whenever the order amount, currency, or method changes. Other methods do not incur this Stripe fee.

The request contract remains only `order_no` plus `payment_method`; never send a locally calculated order amount, fee, payable amount, or return URL. The payment service applies the fee. After creation or query, use the service-returned `amount` as the payable total and any explicit returned fee breakdown as authoritative; never add 3.5% again. If the returned total or explicit fee differs from the confirmed review, highlight the difference and obtain confirmation of the returned amounts before directing the customer to pay; do not create another payment to resolve the discrepancy.

### `POST /skill/flight/v1/query_payment`

This protected endpoint returns the latest third-party payment state and is the reconciliation path after an ambiguous payment-creation result.

```json
{"order_no":"TM202609030001"}
```

`order_no` is required and must be nonblank after trimming. The server resolves the authenticated agent; never send `AgentCode` or `CreatorUser`.

### Payment response contract

Both payment endpoints return this `data` object on `code == 0`:

```json
{
  "order_no":"TM202609030001",
  "payment_method":"stripe",
  "amount":"1025.72",
  "pay_service_fee":"34.65",
  "order_amount":"990.07",
  "currency":"CNY",
  "status":"created",
  "payment_url":"https://example.com/pay"
}
```

| Field | Type | Meaning |
| --- | --- | --- |
| `order_no` | string | Payment order number. |
| `payment_method` | string | Internal API value. Map it to Stripe, WeChat Pay, Alipay, or Online Banking before any user-visible output. If it is unrecognized, do not expose or guess from the raw value. |
| `amount` | string decimal | Total payable amount returned by the service, rendered with two decimal places. For a Stripe payment created with the current flight fee logic, this already includes the rounded 3.5% fee. Report it exactly; never add the fee again or use it as the fee calculation base. |
| `pay_service_fee` | string decimal | Payment service fee, rendered with two decimal places, including `"0.00"` for a zero fee. |
| `order_amount` | string decimal | Total order principal excluding the payment service fee, rendered with two decimal places. |
| `currency` | string | Three-letter uppercase currency. |
| `status` | string | Current payment status; report exactly as returned. |
| `payment_url` | string, optional | Payment destination when supplied. Status `created` requires it; explicitly recognized transitional or terminal states may omit it. Its presence never proves payment success or ticket issuance. |

The example is a Stripe payment for an order total of `990.07`, with a rounded fee of `34.65` and a returned payable total of `1025.72`. The current payment response schema has no separate fee field. If an explicit fee breakdown is returned, display it; otherwise use the payment-result template's missing-breakdown notice. Do not invent a fee field or describe the pre-payment calculation as an API-returned fee. Historical payments may predate the fee logic: report their stored amounts without adding a fee retroactively.

Payment statuses are `init`, `created`, `paid_success`, `pay_failed`, `refund_success`, `refund_failed`, `closed`, `error`, `refund_in_process`, `timeout`, or `unknown`. This API reports refund-related source states but does not initiate refunds.

## Order query

### `POST /skill/flight/v1/query_order`

This protected endpoint returns an AI-safe view of an order the authenticated agent is allowed to query.

```json
{"order_no":"TM202609030001"}
```

`order_no` is required and must be nonblank after trimming. The server resolves the authenticated agent; never send `AgentCode` or `CreatorUser`.

`data` has these fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `order_no` | string | Order number. |
| `agent_order_no` | string | Caller/agent order reference when returned. |
| `status` | string | Order status; report exactly as returned. |
| `total_price` | string decimal | Exact total price. |
| `currency` | string | Three-letter uppercase currency. |
| `adults` / `children` / `infants` | integer | Passenger counts. |
| `payment_deadline` | string, optional | Payment deadline when supplied. |
| `paid_at` | string, optional | Payment timestamp when supplied. |
| `ticketed_at` | string, optional | Ticketing timestamp when supplied. |
| `passengers` | array | Safe passenger summary described below. |
| `journeys` | array | Journey summaries described below. |
| `segments` | array | Flight segments described below. |
| `tickets` | array | Returned ticket references described below. |

Order status values are `pending_confirmation`, `booking_successful`, `payment_successful`, `ticketing`, `payment_failed`, `ticket_issued`, `ticketing_failed`, `cancelled`, `creation_failed`, and `unknown`.

### Payable-order gate

Payment eligibility is an allowlist, not a denylist. A successful, current `query_order` response is payable only when all of these conditions hold:

- `status` is exactly `booking_successful`.
- `paid_at` and `ticketed_at` are absent.
- `tickets` is empty.
- If `payment_deadline` is returned, it can be interpreted reliably and is strictly later than the current time. An absent deadline alone does not make the order ineligible.

Every other listed status is nonpayable. Do not infer that `payment_failed`, `ticketing_failed`, `pending_confirmation`, or `unknown` permits another attempt. A populated `paid_at`, `ticketed_at`, or ticket reference makes the order nonpayable even if the status is inconsistent. A returned deadline that has passed, equals the current time, or cannot be interpreted reliably also makes it nonpayable.

Before presenting payment methods or a payment review, apply this gate to the immediately preceding query. If it fails, use the canonical [payment-unavailable template](response_templates.md#payment-unavailable) and do not call `create_payment`.

After the user explicitly confirms the complete payment review, call `query_order` again immediately before `create_payment` and reapply the gate. If this final query fails, do not create payment. If any reviewed status, amount, currency, itinerary, passenger data, or deadline changed, invalidate the confirmation. For a changed order that remains payable, show the complete updated review and obtain another explicit confirmation; for a nonpayable order, use the payment-unavailable template.

This final client-side query narrows but cannot eliminate a state change between `query_order` and `create_payment`. The payment service must enforce the same payable-order gate atomically when it processes creation and reject an order that has become nonpayable. Do not treat the client's preflight as evidence that the endpoint performed that server-side check.

Each `passengers` item has `index` (integer), `type` (`adult`, `child`, `infant`, or `unknown`), `first_name` (string), and `last_name` (string). Each `journeys` item has `index`, `departure_city`, `departure_airport`, `arrival_city`, `arrival_airport`, `transfer_count`, and `duration_minutes`.

Each `segments` item has `index`, `group`, `airline`, `flight_no`, `operating_airline`, `operating_flight_no`, `cabin_class`, `cabin_code`, `departure_city`, `departure_airport`, `departure_terminal`, `departure_time`, `arrival_city`, `arrival_airport`, `arrival_terminal`, `arrival_time`, and `duration_minutes`. Each `tickets` item has `passenger_index`, `segment_index`, `ticket_no`, `pnr`, and `airline_pnr`.

Nullable timestamps are omitted when absent. Empty collections are returned as `[]`, never `null`. The response intentionally excludes document data, birthdays, nationality, phone numbers, email addresses, addresses, remarks, supplier/internal identifiers, cost fields, ancillary data, and refund metadata.

## Error actions and redaction

### Failed-quotation recovery

A nonzero response `code` is a failed request, including when HTTP status is 200. Handle ToB business `code == 20105` as the dedicated permission condition before the generic recovery below. Never display its raw message or other API/transport exceptions to the customer. Explain the affected booking stage in friendly language, retain the known order/payment state, and select the recovery below.

Except for the dedicated ToB `code == 20105` permission condition, remove any affected failed offer from selectable quotation state, its quotation-number-to-`offer_id` mapping, associated verified session, and booking confirmation. For a failed search, clear the current quotation set. Keep order numbers, payment state, and sanitized reconciliation evidence even when a quotation is removed. Do not offer the failed quotation again or ask the customer to pick another quotation from the old results table as recovery. A fresh successful search replaces the old table and its mappings with newly numbered offers.

| Failure stage | Recovery |
| --- | --- |
| ToB business `code == 20105` | Keep the `sk_` Token and reusable header. Stop the permission-gated booking workflow, clear verification/booking-confirmation state for the selected offer, and use the business-flight-permission template. Do not enter authentication recovery, request a replacement Token, retry, or switch channels. User-requested price searches may continue; after access is enabled, require an explicit request and a new live search before verification or booking. |
| Airport lookup or flight search | Explain that the lookup/search did not complete. Correct known invalid inputs; invite the user to retry lookup or run a fresh search after criteria are valid. Never fall back to an older results table. |
| Offer verification | Delete the failed quotation, session, and confirmation; politely explain that it cannot currently be confirmed and invite a fresh search using the confirmed criteria. Do not ask for another selection from old quotations. |
| Booking creation, with authoritative confirmation that no order was created | Delete the failed quotation/session/confirmation. Explain that booking did not complete and offer a new search; after the user authorizes it, search live, verify a newly selected quotation, and obtain a new complete booking review confirmation. |
| Booking creation that may have reached the service, without authoritative confirmation of outcome | Invalidate the quotation for reuse, retain reconciliation evidence, and first reconcile using a known real order number or customer service. A nonzero code alone does not prove no order exists. Do not direct the customer into a replacement booking while the earlier outcome is unknown. |
| Order query, payment creation, or payment query for an existing order | Preserve the real order. Explain that order/payment handling did not complete or is unconfirmed; query/reconcile or refer to customer service as appropriate. Do not turn payment/query failure into a new booking or flight search. |
| Authentication failure at any stage | Clear the rejected credential and reusable header, stop the affected operation, and show the matching official replacement-token guidance. Do not retry automatically. A replacement may be used only for a later user-requested or approved operation after normal preconditions are satisfied; any affected failed quotation remains removed. |

A nonzero business code does not authorize automatic retry or automatic fresh search. Obtain a user instruction for the new search, revalidate criteria and dates, and show only its new results. For a verification failure other than ToB `code == 20105` before any booking attempt, use the [verification failure template](response_templates.md#failure-and-reconciliation). Select the order-state statement from actual evidence for other stages. Distinguish local input validation, which must be corrected before sending, from an API rejection, which also invalidates affected quotations.

| Condition | Required action |
| --- | --- |
| `code == 0` | Continue only with the returned `data`; for verification, still obtain explicit booking confirmation. |
| ToB business `code == 20105` | Handle before every HTTP-status or error-text rule. Keep the accepted `sk_` Token and reusable header, stop the permission-gated booking workflow, and use the [business-flight-permission template](response_templates.md#business-flight-booking-access-required). Do not clear or replace the Token, retry, or switch channels. |
| Nonzero business `code` (including HTTP 200) | Remove affected failed quotations and follow the stage-specific recovery above; invite a fresh search when appropriate instead of reselection from the old table. Retain order/payment uncertainty, and never expose the original message or retry automatically. |
| HTTP 401, `unauthorized`, or `invalid_token`, after excluding ToB `code == 20105` | Clear the rejected credential and reusable header, stop the affected operation, and follow [authentication recovery](authentication.md). Never retry the rejected token, search for another credential, switch channels silently, or automatically replay the operation after a replacement is saved. |
| Transient transport error or HTTP 5xx during airport lookup, search, or verification, without a nonzero business response or authentication failure | Retry the identical request once only. |
| Ambiguous booking result (for example, timeout or HTTP 5xx after the request may have been sent) | Stop creation. If a real order number is known, use `query_order` to reconcile; otherwise state that no order number was returned and creation is unknown, and provide customer service. Do not repeat booking until absence of an order is confirmed, a user-authorized fresh search and verification have completed, and the user approves the new complete booking review. |
| Missing or unsupported payment method | Do not call payment creation. Present the methods allowed for the queried order currency and request a supported selection. |
| Ambiguous payment creation (for example, transport error or timeout after dispatch) | Never retry an ambiguous payment creation. Report uncertainty and use `query_payment` to reconcile before any further user-authorized decision. |
| Order or payment query needs retry | Retry only when the user explicitly requests it and a usable channel-matching credential is configured. Do not add an implicit retry policy. |
| Invalid parameters | Explain which input needs correction. Revalidate corrected data and renew any required booking/payment confirmation before submission. If an earlier creation may have been dispatched, reconcile it first; corrected input is not permission to duplicate creation. |

Customer-facing failure messages must state the operation that did not complete or could not be confirmed, the order-number state, and the next recovery action. Select the state from evidence:

- **No creation request sent:** say this operation has not created an order; request the missing data, renewed authorization, or other specific recovery step. An existing order remains unchanged by this failed read-only/preflight operation.
- **Order number confirmed:** show the actual known `order_no` and explain which later operation failed or remains unconfirmed; query that order/payment to recover. A known order does not prove payment success.
- **Creation request sent, no reliable result:** use the [ambiguous booking template](response_templates.md#failure-and-reconciliation). Do not claim no order exists merely because the response lacks a number. A local `agent_order_no` does not establish creation.
- **Authoritative reconciliation confirms no order was created:** explain that no order was generated and remove the failed quotation/session. Resolve the cause, obtain approval for a fresh search, verify a new quotation, and obtain a fresh complete booking confirmation before a new creation attempt.

For payment creation/query failures, distinguish the existing booking from the payment state and use the [ambiguous payment template](response_templates.md#failure-and-reconciliation). If that query also fails, report that the payment state remains unknown and refer to customer service; do not retry creation. Use templates only when their predicates are supported by actual results.

For support, use the [customer-service template](response_templates.md#customer-service).

Never paste raw API/system error strings, exception names, stack traces, SQL, request headers, or internal supplier payloads into customer replies, even inside a code block. Preserve original error details, endpoint, time, and available diagnostic identifiers only in internal troubleshooting records after removing tokens and personal data. Do not discard diagnostic evidence just to make the customer message friendly; do not attach the internal records to the customer reply.

Redact the Skill token, document/card numbers, phone numbers, and email addresses in logs, errors, examples, and ordinary user-visible summaries. The exceptions are the booking and payment confirmation tables shown to the customer immediately before creation: display available passenger names, document fields, and contact details in full so the customer can verify them. Follow the [canonical review templates](response_templates.md#shared-review-tables) and [passenger data-source rules](passenger_details.md); missing query fields must not be fabricated or filled from an unrelated order. Never expose the Skill token in any summary, URL, or JSON body, and never send `AgentCode` or `CreatorUser` from the client.
