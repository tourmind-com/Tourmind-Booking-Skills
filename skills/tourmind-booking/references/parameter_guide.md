# TourMind hotel API and field reference

Use this reference for HTTP requests and returned fields. For price comparison see [Search and pricing](search_and_pricing.md#compare). For confirmation, payment and creation recovery see [Booking and payment](booking_and_payment.md#payment) and [Creation recovery](booking_and_payment.md#recovery).

[Transport](#shared-request-rules) · [Locale table](#returned-result-page-url-language) · [Endpoint contracts](#endpoint-contracts) · [Display fields](#display-field-mappings) · [Errors](#errors)

<a id="shared-request-rules"></a>
## Transport and credentials

`POST` JSON (`Content-Type: application/json`) to `https://api.tourmind.com`. All routes below are relative to this host. A successful business response normally carries `ok=true` and `data`. Failures carry `ok=false`, `error` and, for specific cases, `error_code` or `reason`. Inspect the body even for HTTP 200. Only `check_skill_update` takes `current_version`.

| Credential | Route and body |
|---|---|
| Absent | Public `/skill/toc/` for search, details, rates, availability and booking review. Omit credentials and skip automatic coupons. Sign in for an explicit coupon lookup and all order operations. |
| `uk_` | Personal `/skill/toc/`. Send the current `user_key` on every `search_hotels` call. For other endpoints, follow the credential rule for that operation. Public location/detail reads and the version check do not require it. |
| `sk_` | Business `/skill/tob/`. Send `token` on **every** endpoint. |
| Other prefix | Stop before calling. Require a valid personal or business credential. |

Read the credential according to the entry Skill; `{baseDir}/skill_token.txt` holds at most one. Never mix or cross-send credential fields or expose their values. Use the same channel/account for rates, availability and coupons, and the creation channel for every order operation. Send `hotel_id` and `region_id` as strings; pass opaque codes verbatim. Translate user-facing descriptions, preserving identifiers, numbers, currencies and timestamps. Optional fields can differ by channel.

<a id="date-and-occupancy-rules"></a>
## Stay and occupancy fields

| Field | Type and meaning |
|---|---|
| `check_in_date`, `check_out_date` | `YYYY-MM-DD` strings. Checkout must be later than check-in. Resolve relative dates in the user's timezone; if the year is absent use the next future occurrence and disclose it. |
| `adults`, `room_count` | Integers. Adults **per room**, default 1 if omitted; room count defaults to 1. Keep any stated counts. Disclose defaults. |
| `children`, `children_ages` | Children per room (integer, default 0) and their ages (integer array, default `[]`). Exactly one age 0–17 per child. |

Each room repeats the same configuration. For multiple rooms and only a party total, obtain the per-room breakdown. Mixed occupancy and `room_occupancies` are unsupported. For live rates resolve location and both dates first.

<a id="search-currency-and-result-display-currency"></a>
### Currency and price bounds

Use ISO 4217 codes (for example `CNY`, `USD`, `EUR`, `GBP`, `JPY`). Only send `lowest_price`/`highest_price` for pre-coupon searches. These are CNY totals for the entire stay and all rooms; each bound is optional independently. A per-room nightly bound converts to `source_bound × live_CNY_rate × night_count × room_count`. For an explicit trip total use `source_total × live_CNY_rate`. Example: September 1–4, one room, CNY 300–400 per room per night → bounds 900–1,200; two rooms → 1,800–2,400. For coupon-inclusive budgets omit **both** fields and apply the budget after verification. See [comparison](search_and_pricing.md#compare).

The default display currency is CNY for a Chinese request and USD otherwise. An explicitly requested display currency takes precedence. For conversion use one current rate for nightly and total amounts, label estimates and state source, rate and retrieval time. If a necessary CNY budget conversion is unavailable, ask for a CNY budget or permission to omit that filter. Keep original checked amounts and currency for confirmation and API calls.

<a id="returned-result-page-url-language"></a>
<a id="result-page-url-language"></a>
## Result-page URL language

| Response language | URL locale |
|---|---|
| Chinese | `zh-CN` |
| English | `en-US` |
| Japanese | `ja` |
| Korean | `ko` |
| Spanish | `es` |
| Arabic | `ar` |
| All other languages | `en-US` |

Use the current or explicitly requested response language. For `search_hotels.data.web_url`, `query_room_rates.data.web_url`, and each successful `batch_query_room_rates.data.results[].data.web_url`, replace **only** the locale path segment in `/zh-CN/skills/access`. Preserve scheme, host, remaining path, query string and ordering, fragment and access ticket. Leave an unexpected path unchanged. Omit a missing link. `web_url_expires_at` is the expiry; `web_url_one_time=false` permits repeat viewing before expiry. These links grant read-only access to hotel lists/details/quotes, not verification, `/book/*`, booking, payment or account operations.

<a id="endpoint-contracts"></a>
## Endpoints

Each heading below names an HTTP operation. Use the path for the active channel.

[check_skill_update](#check_skill_update) · [search_location](#search_location) · [search_hotels](#search_hotels) · [get_hotel_detail](#get_hotel_detail) · [query_room_rates](#query_room_rates) · [batch_query_room_rates](#batch_query_room_rates) · [check_room_availability](#check_room_availability) · [query_available_coupons](#query_available_coupons) · [create_booking](#create_booking) · [query_booking](#query_booking) · [cancel_booking](#cancel_booking) · [pay_order](#pay_order)

<a id="check_skill_update"></a>
### `check_skill_update`

`POST /skill/toc/check_skill_update` · `POST /skill/tob/check_skill_update`

Read-only and idempotent. Required `current_version` is the exact semantic version in `SKILL.md` frontmatter `metadata.version`. ToC sends **only** this field, even if signed in. ToB also sends `token`. In a new chat and after 24 hours of inactivity check once; failure is advisory.

When returned, the top-level `skill_update` object requires `available` and `display_to_user` (booleans), `latest_version` (semantic version string), and, when both flags are true, `message` and `release_source_url`. When no update is available both flags are false. Do not look for these fields inside `data`. A malformed version returns `ok=false` and an invalid-version error. Follow the entry Skill for showing notices and installing updates.

<a id="location-and-poi-resolution"></a>
<a id="region-first-routing"></a>
<a id="nearby-mode"></a>
<a id="exact-point-and-broad-poi-fallback"></a>
<a id="search_location"></a>
### `search_location`

`POST /skill/toc/search_location` · `POST /skill/tob/search_location`

Required `keyword` (string): city, district, POI, landmark or hotel phrase. Public ToC sends no credential; ToB adds `token`. Region/POI selection belongs to the [search workflow](search_and_pricing.md).

| Response | Fields and interpretation |
|---|---|
| `data.regions[]` | `region_id`, `name`, `name_cn`, `full_name`, `full_name_cn`, `region_type`, `country`, `latitude`, `longitude`, optional `hotel_count`. |
| `data.hotels[]` | Hotel identifier and name, address, region and country fields. Static matches do not prove availability. |
| `data.place` | First Google Places result: `place_id`, `name`, `formatted_address`, `latitude`, `longitude`, `types`, `source`, `recommended_radius_km`, `search_scope`. Check name/address/context. |

For nearby requests use `place.latitude`, `place.longitude` and the exact requested radius; when unspecified, use `place.recommended_radius_km` (currently 3 km).

<a id="search_hotels"></a>
### `search_hotels`

`POST /skill/toc/search_hotels` · `POST /skill/tob/search_hotels`

For every ToC `search_hotels` request (keyword, region or nearby), send the current `user_key` when signed in, even when the user declines coupons. Omit credentials when signed out. ToB requires `token`. Select **one** location mode: `region_id` for a region, all of `latitude`, `longitude`, `radius_km` for a nearby search, or `keyword` for hotel-name discovery. The latter returns static candidates without live prices. For priced searches supply `location_name` with the resolved region or place name used for the result page.

Region/nearby requests take `check_in_date`, `check_out_date`, `adults` and optional `room_count`, `children`, `children_ages`, `lowest_price`, `highest_price`. The last two are pre-coupon CNY totals. The backend probes candidate hotels with the requested stay and per-room occupancy and returns up to 20. Read `data.total`, `data.hotels[]`, and, if present, `data.search_scope` and the result-page fields. Response fields can include `hotel_id`, `hotel_name`, `hotel_name_cn`, `address`, `address_cn`, `hotel_image`, `star_rating`, `min_price`, `currency_code` and nearby `distance_km`. `min_price` is a candidate signal, not a confirmed bookable price for the selected product/stay.

<a id="get_hotel_detail"></a>
### `get_hotel_detail`

`POST /skill/toc/get_hotel_detail` · `POST /skill/tob/get_hotel_detail`

Required string `hotel_id`; public ToC sends no credential, ToB adds `token`. Optional `language` controls image lookup, not the result-page locale. `data.hotel` supplies identity (`hotel_id`, `name`, `name_cn`), location (`address`, `address_cn`, coordinates and region/country), `telephone`, `star_rating`, `hotel_image`, `hotel_images`, `image_groups`, `amenities`, descriptions, policies and `fees`. `data.rooms[]` contains static definitions: `room_id`, names, `area_range`, `occupancy`, bed information and optional `basic_room_image`; these are not inventory.

<a id="query_room_rates"></a>
### `query_room_rates`

`POST /skill/toc/query_room_rates` · `POST /skill/tob/query_room_rates`

Required `hotel_id` (string), `check_in_date`, `check_out_date`, `adults`. Optional `room_count`, `children`, `children_ages`. Public ToC omits credentials; authenticated ToC uses `user_key`; ToB requires `token`. Each item in `data.room_types[]` supplies room names, bed description, optional `basic_room_image` and `products[]`. A product is a particular room/occupancy/meal/cancellation offer.

| Product field | Meaning |
|---|---|
| `max_occupancy`, `max_children`, `meal_type`, `meal_count` | See capacity and meal tables below. |
| `cancellation_policy` | `type`, `free_cancel_deadline`, `effective_non_refundable`; retain the returned timezone offset. |
| `rate.rate_code` | Opaque product quote identifier for availability checking. |
| `rate.currency`, `rate.total_price`, `rate.per_night_price` | Transaction currency; pre-coupon room charge for all rooms/all nights; average per room per night. Amounts are in currency major units. |
| `rate.payment_type`, `rate.is_on_request` | Payment type and supplier-confirmation flag. `is_on_request=true` is not immediately confirmed inventory. |
| `rate.stripe_payment_fee` | Quote-level `fee_rate`, `fee_amount`, fee-inclusive `payable_amount`, `currency` (and `notice` when provided). Applies to this quote's amount, not a later discounted charge. |

Optional `data.web_url` is for this hotel's returned rooms; use its own expiry and one-time flag. Do not substitute a hotel-list URL. HTTP 200 with `data.room_types=[]` and `data.reason=no_matching_live_room` is a successful empty result.

The sibling metadata for this link is `data.web_url_expires_at` and `data.web_url_one_time`; keep it attached to the same hotel.

<a id="adult-and-child-capacity"></a>
#### Adult and child capacity

`maxOccupancy` / `max_occupancy` is the **adult limit per room**; `maxChildren` / `max_children` is the **additional child limit per room**, if returned. Compare the two separately. For 2 adults and 1 child aged 6 in each of 2 rooms, use `adults=2`, `children=1`, `children_ages=[6]`, `room_count=2`. A product with limits 2 and 1 fits this capacity, subject to child-age terms and final verification. Zero child capacity allows no additional children; an absent field is unknown. Do not add adults and children when testing the adult limit. `allotment` is inventory, not guest capacity.

<a id="meal-type-mapping"></a>
#### Meal type mapping

Read both number and numeric-string values of `meal_type` / `mealType` from single rates, batch items and availability results. Use the booked occupancy for type 2, not maximum room capacity. `meal_count` / `mealCount` supplements known codes and a zero cannot override them. If type is missing/unknown and quantity is positive, report the quantity without guessing the meal; otherwise report type unspecified.

| Code | Constant | Meaning |
|---|---|---|
| 1 | `MealType_No_Breakfast` | Room only / no breakfast |
| 2 | `MealType_Free_Breakfast` | Breakfast included for booked guests |
| 3 | `MealType_ONE_Breakfast` | 1 breakfast |
| 4 | `MealType_TWO_Breakfast` | 2 breakfasts |
| 5 | `MealType_THREE_Breakfast` | 3 breakfasts |
| 6 | `MEALTYPE_FOUR_BREAKFAST` | 4 breakfasts |
| 7 | `MEALTYPE_FIVES_BREAKFAST` | 5 breakfasts |
| 8 | `MEALTYPE_SIX_BREAKFAST` | 6 breakfasts |
| 9 | `MEALTYPE_SEVEN_BREAKFAST` | 7 breakfasts |
| 10 | `MEALTYPE_EIGHT_BREAKFAST` | 8 breakfasts |
| 11 | `MealType_Lunch` | Lunch only |
| 12 | `MealType_Dinner` | Dinner only |
| 13 | `MealType_LunchAndDinner` | Lunch and dinner |
| 14 | `MealType_HalfBoard` | Half board: breakfast and one main meal |
| 15 | `MealType_FullBoard` | Full board: breakfast, lunch and dinner |
| 16 | `MealType_AllInclusive` | All inclusive |
| 17 | `MealType_SelfCatering` | Buffet in this Skill's mapping; meal time and kitchen are unspecified |
| 18 | `MealType_BreakfastAndLunch` | Breakfast and lunch |
| 19 | `MealType_BreakfastAndDinner` | Breakfast and dinner |

<a id="batch_query_room_rates"></a>
### `batch_query_room_rates`

`POST /skill/toc/batch_query_room_rates` · `POST /skill/tob/batch_query_room_rates`

Same stay fields and credential rules as `query_room_rates`; replace `hotel_id` with required `hotel_ids`, an array of 1–20 strings. Each request uses one shared stay and per-room configuration. The server uses four workers and preserves input order. The client may run up to three batches concurrently.

`data.results[]` contains `hotel_id`, `ok`, then `data` on success or `reason`/`error` on failure. Each successful item has the single-rate response shape, including its own optional hotel-detail link. `data.summary` contains `total`, `matched` (hotels with products), `empty` (successful no-match), and `failed`. A completed batch can contain any combination of these; retain each outcome without replacing failed/empty items with individual calls.

<a id="check_room_availability"></a>
### `check_room_availability`

`POST /skill/toc/check_room_availability` · `POST /skill/tob/check_room_availability`

Send `hotel_id`, `rate_code` from the selected live product, the same dates and per-room occupancy. On ToC, omit credentials when signed out and send the current account's `user_key` on every signed-in availability check, including when the user declines coupons. On ToB, send the current business `token`. For a selected product or an explicit verification request, declining coupons only skips the coupon lookup.

Read the selected `data.room_types[].rateInfos[]` row: `rateCode`, `totalPrice` and `currencyCode` are the checked values; the code and price can change. This call verifies but does not reserve inventory. Use the returned cancellation details. In legacy `cancelPolicyInfos`, `refundable: true` means cancellable/refundable, `startDateTime` is the free-cancellation deadline, and `amount` is the fee **after** it.

<a id="query_available_coupons"></a>
### `query_available_coupons`

`POST /skill/toc/query_available_coupons` · `POST /skill/tob/query_available_coupons`

Protected. Use `user_key` (ToC) or `token` (ToB). Trusted OAuth integrations take identity from their existing authorization without a `user_key`; the HTTP Skill does not add an OAuth route. Send only the following booking context from the same authenticated account, channel and verified quote:

| Required fields | Meaning |
|---|---|
| `hotel_id`, `rate_code` | Selected hotel ID as a string and the latest checked code. |
| `check_in_date`, `check_out_date` | Verified dates, both `YYYY-MM-DD`. |
| `currency`, `total_price` | Checked `rateInfos[].currencyCode` and pre-coupon charge for **all rooms and nights**, in major units. The service checks the authenticated settlement currency. |

| Success field under `data` | Meaning |
|---|---|
| `coupons` | Array of eligible coupons. `[]` is a successful no-coupon result. |
| `coupons[].coupon_code` | String to pass to booking if this coupon is selected. |
| `coupons[].discount_amount` | Number. Expected actual discount for this quote, in major units. |
| `coupons[].payable_amount` | Number. Post-coupon **room charge only**, in major units; excludes payment fees. This is the confirmed `expected_payable_amount` for booking. |
| `coupons[].currency` | ISO 4217 string. Currency of these amounts. Match it to the checked quote; the coupon template can have another currency. An empty list supplies no currency; retain the checked currency. Resolve mismatches before use. |
| `coupons[].remaining_quantity` | Integer. Only Skill campaigns use shared quota minus reserved/redeemed uses. An ordinary eligible coupon can return zero; do not drop it. The response does not give coupon type or a personal coupon balance. |
| `message` | String. Usage guidance. |

Preview may issue a campaign coupon once per account/configuration, but does not reserve quota or bind the order. No `available`, `unavailableReasonCode` or unavailable promotional coupons from `/support`. `request_id` belongs to creation, not preview.

<a id="create_booking"></a>
<a id="coupon-aware-booking-creation"></a>
### `create_booking`

`POST /skill/toc/create_booking` · `POST /skill/tob/create_booking`

Protected. Supply `user_key` (ToC) or `token` (ToB). The first four rows below are mandatory for this Skill. The last two describe the optional coupon path; when binding a coupon, supply all three coupon-attempt fields.

| Request | Type and source |
|---|---|
| `hotel_id`, `rate_code` | Strings. Selected hotel and opaque code from the latest availability check. |
| `check_in_date`, `check_out_date`, `adults`, `room_count`, `children`, `children_ages` | Confirmed dates and per-room occupancy. For no children send 0 and `[]`. |
| `guest_name`, `contact_email` | Full legal name (Chinese or Latin script) and a user-provided contact email. Both are mandatory for this Skill even where the server tolerates an absent email. Check one `@`, nonempty local/domain parts and a dot in the domain; format alone does not verify deliverability. |
| `currency`, `total_price` | Currency and strictly positive **pre-coupon** room charge from the latest check, in major units. |
| `coupon_code`, `expected_payable_amount` | For a selected coupon, send the returned code and confirmed post-coupon room charge excluding fees. Omit coupon fields for a no-coupon booking. |
| `request_id` | String, 1–64 bytes, required when using a coupon. Reuse the same ID and exact business parameters for the same attempt. |

Example: CNY 128 before coupons, CNY 20 off → `total_price=128`, `expected_payable_amount=108`. A confirmed amount is distinct from a missing argument. The server rechecks eligibility, quota and actual discount; a rejected preview is not permission to book at the original price. For ambiguous results and retry limits use [creation recovery](booking_and_payment.md#recovery).

| Success field under `data` | Meaning |
|---|---|
| `agent_ref_id` | TourMind order reference for query, payment and cancellation. Retain its creation channel. |
| `total_price`, `discount_amount`, `payable_amount`, `currency` | Original room charge, actual order discount, post-coupon room charge **excluding payment fees**, and their currency (major units). |
| `request_id`, `request_state` | Creation attempt and its processing state. Success is `SUCCEEDED`. |
| `status`, `message`, `replayed` | Creation `status=confirmed` acknowledges creation only. `message` supplies next steps. `replayed=true` means the existing order was returned; first success omits the flag. |

Read `data.agent_ref_id` from the creation response; use that exact string for subsequent order operations.

<a id="query_booking"></a>
### `query_booking`

`POST /skill/toc/query_booking` · `POST /skill/tob/query_booking`

Required string `agent_ref_id` and credentials for the order-creation channel (`user_key` or `token`). Read the current account's order rather than assuming a previously discussed order is meant.

| Success field under `data` | Meaning |
|---|---|
| `agent_ref_id`, `status`, `status_cn` | Order number, current status code, Chinese status description. |
| `hotel_id`, `hotel_name`, `room_type`, `check_in`, `check_out`, `room_count` | Booked hotel, room, dates and number of rooms. |
| `contact_name`, `hotel_confirmation_no`, `order_date` | Order contact, hotel confirmation number if provided, and order creation time. An empty confirmation number is not evidence of hotel confirmation. |
| `total_price`, `discount_amount`, `payable_amount`, `currency` | Full room charge, current bound/redeemed discount, post-coupon room charge **excluding fees**, and order currency; outer amounts use major units. |
| `coupon_usage` | Current binding object, or `null` when none. Not a history list. |

| `coupon_usage` field | Type and meaning |
|---|---|
| `id` | Integer binding-record ID. |
| `coupon_id`, `redeem_code_id` | Integer or null: coupon configuration ID and the user's coupon-entitlement record ID. |
| `channel_order_num`, `channel_id` | Order number (string) and channel (integer). |
| `agent_code`, `user_name`, `skill_source` | Owning account, username and source identifier (strings). |
| `discount_amount`, `currency_code` | Integer in **minor units** and currency. For CNY, 2,000 minor units = CNY 20.00. Do not subtract it again. |
| `status` | Integer. `0` = no coupon, `1` = reserved, `2` = redeemed. Released `status=3` is excluded from the current record. |
| `expires_at`, `consumed_at`, `released_at` | Nullable timestamp strings for expiry, redemption, release. Preserve the returned offset. Expiry alone does not establish release. |
| `release_reason`, `created_at`, `updated_at` | Release reason, creation time and update time (strings). |

| Order `status` | Meaning |
|---|---|
| `UNPAID` | Created and awaiting payment. |
| `PENDING` | Paid, awaiting hotel confirmation; do not pay again. |
| `CONFIRMED` | Hotel confirmed. |
| `CANCELLED` | Cancelled. |
| `CONFIRM_FAILED` | Hotel confirmation failed, distinct from a creation error. |

<a id="cancel_booking"></a>
### `cancel_booking`

`POST /skill/toc/cancel_booking` · `POST /skill/tob/cancel_booking`

Required `agent_ref_id` and the creation-channel credential. Confirm the exact order and cancellation terms before invoking. The response provides `agent_ref_id`, `status`, `status_cn`, `total_amount`, `cancel_fee`, `currency`, `message` and may include `refund_amount` and `payment_method` where applicable. A refund amount does not demonstrate receipt of funds. A charged Stripe processing fee is non-refundable even during the hotel's free-cancellation period.

<a id="pay_order"></a>
### `pay_order`

`POST /skill/toc/pay_order` · `POST /skill/tob/pay_order`

Request: `agent_ref_id`, exact `payment_method`, and the creation-channel credential. The payment service uses the order's bound discount snapshot. **No coupon input**, confirmation flag or custom return URL is required: never resend `coupon_code`, `discount_amount` or `expected_payable_amount`. User confirmation takes place in the conversation. For the method and fee review see [payment](booking_and_payment.md#payment).

| Successful `data` field | Meaning (all monetary values in currency major units) |
|---|---|
| `order_amount` | Original full room charge before discount or payment fees. |
| `discount_amount` | Discount applied to this order. Zero for no coupon. |
| `payable_amount` | Final amount for **this payment method**, after discount, including any applicable payment fee. For Stripe it matches `stripe_payment_fee.payable_amount`. |
| `currency`, `agent_ref_id`, `payment_method`, `message` | Order/payment currency, order number, selected method and payment instructions. The result does not include a coupon list or `coupon_usage`; look up binding details with `query_booking`. |

| `payment_method` | Currency/client | Branch-specific fields |
|---|---|---|
| `Stripe` | Available method for non-CNY orders, including USD; also an offered method for CNY under this Skill. | `pay_url`, `request_id`, `third_party_order_no`, `stripe_payment_fee` (`fee_rate`, `fee_amount`, `payable_amount`, `currency`, `notice`). The separate 3.5% fee uses the **post-coupon** room charge. |
| WeChat Pay (`微信支付`), Alipay (`支付宝`) | CNY only. | `pay_url`, `expires_at`, `one_time=true`. With no separate fee the amount equals the post-coupon room charge. |
| Alipay AI Pay (`支付宝AI付`) | CNY only, with native Qwen cashier support. | `prepay_id`, `expires_at`, `request_id`, `third_party_order_no` and empty `pay_url`. Use the native cashier, not a clickable link. |

Example in USD: an original room charge of 100.00 with 20.00 off gives a room-only `query_booking.data.payable_amount` of 80.00. A successful Stripe payment-link response reports `order_amount=100`, `discount_amount=20`, `stripe_payment_fee.fee_amount=2.80` and fee-inclusive `payable_amount=82.80`. Without the coupon the fee is 3.50 and the total 103.50. Use the values actually returned. A link or prepayment ID does not prove success; check the order.

Use `check_room_availability.data.room_types[].rateInfos[].currencyCode` for the coupon request, then `query_booking.data.currency` to select the payment method after creation. WeChat Pay and Alipay use the exact Chinese API values in the table. If an older response omits amount fields, do not infer a zero discount. Reconcile the latest order and the available payment breakdown before sharing the link; stop if the payable amount or currency cannot be verified.

<a id="display-field-mappings"></a>
<a id="hotel-list"></a>
<a id="room-details"></a>
<a id="cancellation-tax-and-payment-semantics"></a>
## Display field mappings

For the rendered layouts use [response templates](response_templates.md#hotel-list). The sources below apply to each specific hotel/product.

| Item | Source and fallback |
|---|---|
| Candidate count, distance | `search_hotels.data.total` or returned array length; `search_hotels.data.hotels[].distance_km` in nearby mode. |
| Name, class, address | Search name/star corroborated by details; use `get_hotel_detail.data.hotel.address_cn` then `address`. |
| Hotel hero | `hotel.hotel_image` → `image_groups` item labeled `Primary image`, preferring a valid `1000px` or largest `href` → first valid `hotel_images` item → no-image message. No unrelated substitute or separate raw image URL. |
| Detail page | Selected hotel's `query_room_rates.data.web_url` or successful batch item's own `data.web_url`, below that hotel's image. The hotel-list link belongs to the overall results. |
| Room image | Exact live `room_type.basic_room_image` → confidently matched static `rooms[].basic_room_image` → generic room gallery explicitly labeled as not this specific room → no-image message. |
| Room name and details | Chinese reply: `name_cn` then `name`; otherwise `name` then `name_cn`. Empty/`Others` is “Other / room assigned at check-in.” Show bed, separate adult/child capacity, meals, nightly/total price, cancellation and `is_on_request` for the same product. |
| Price, cancellation, match reason | Actual live product and checked coupon when applicable. `cancellation_policy.type=non_refundable` or `effective_non_refundable=true` indicates nonrefundable. `type=free_cancel_before_deadline` requires the exact deadline with its timezone. Match reasons use verified fields only. |
| Check-in/out, taxes, fees | `hotel.checkin.begin_time`, `hotel.checkout.time`; unknown times are “Not provided by the hotel.” The final room quote includes tax. Read `hotel.fees.mandatory` separately for city, tourist, resort or other at-property charges. Preserve the stated amount and basis; do not add ambiguous prose to the room total. Without an explicit fee, report that no additional mandatory fee information was returned, not that charges are impossible. |

<a id="booking-and-order-rules"></a>
<a id="candidate-verification-and-ranking"></a>
For hotel selection, exclusions, ranking and expansion see [comparison rules](search_and_pricing.md#compare). For the guest information, booking review, order channel, payment approval and cancellation sequence see the [booking workflow](booking_and_payment.md).

<a id="errors-and-performance"></a>
<a id="errors"></a>
## Errors and empty results

| Response or condition | Meaning and action |
|---|---|
| HTTP 401 / `unauthorized` | Invalid credential. Clear the active credential as directed by the entry Skill, stop authenticated work and reauthenticate for its prefix. Do not automatically downgrade or probe the opposite channel. |
| ToB HTTP 403, `error_code=HOTEL_BUSINESS_PERMISSION_REQUIRED` | Valid business token, missing hotel-business access. Keep the token, stop and direct the user to their administrator or TourMind support. Changing tokens or retrying does not grant access. |
| Missing credential | Public ToC search, rates, availability and review can continue. Sign-in is required for an explicitly requested coupon check or any order operation. |
| Nonempty invalid credential or unknown prefix | Stop before any endpoint call. Request a valid complete credential beginning `uk_` or `sk_`; never send the invalid credential or silently downgrade to public ToC. |
| Channel changed after rate selection | Discard the old channel’s rate codes, prices, availability, cancellation terms and payment context. Fetch rates and verify them on the new channel, review and reconfirm the new terms. Existing orders stay with their creation channel. |
| Empty candidates or no live products | State which case occurred and the exact constraints. A budget-free diagnostic is optional; do not silently change user constraints. |
| `no_matching_live_room` | Successful empty room-rate result, not a failure. Suggest other dates or occupancy. |
| `hotel_not_found` | Hotel missing or unavailable. |
| `upstream_timeout` | Upstream live pricing timed out. |
| `upstream_error` | Upstream service failure. |
| `hotel_detail_unavailable` | Required hotel details are temporarily unavailable. |
| `invalid_request` | Correct malformed/invalid request before retrying. May describe an entire request rather than one batch item. |
| Selected rate fails availability checking | Handle 401/`unauthorized` and ToB 403/`HOTEL_BUSINESS_PERMISSION_REQUIRED` immediately using [access recovery](access_and_updates.md#auth-errors). For a safely retryable transient failure, recheck the same rate once. Report any unresolved error. |
| Ordinary coupon lookup fails for one quote | Label its verified price as pre-coupon, coupon lookup unavailable. Keep it separate from verified after-coupon rankings and budget matches and continue with the other quotes. |
| Coupon no longer eligible / quota exhausted / payable changed | Refresh coupons and reconfirm price/terms. No silent fallback to a full-price booking. |
| `FAILED_NO_ORDER`, `PROCESSING`, `UNKNOWN`, conflicting `request_id` | Creation outcomes can appear in error text. HTTP errors, `ok=false`, MCP `isError=true`, `booking failed`, `CONFIRM_FAILED` or “not found” alone do not prove no order. Use [creation recovery](booking_and_payment.md#recovery). |

Rate-query `reason` codes apply to single calls and to each `batch_query_room_rates.data.results[]` item separately. Preserve successful siblings and never present a timeout as sold out. Run booking, cancellation and payment sequentially.
