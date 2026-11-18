# Verify, book and manage a hotel order

<a id="book"></a>
## Verify the chosen room and create the booking

1. A room selection authorizes verification only. If a pasted selection has yet to be matched to one live product on the active channel, [match it first](search_and_pricing.md#copied-product). Ask the user to choose if several products fit. Call [`check_room_availability`](parameter_guide.md#check_room_availability) for the chosen product, dates, room count, adults, children and ages, using the current identity even when coupons are declined. Use the returned rate code, total, transaction currency, inventory and cancellation terms.
   - On HTTP 401 or `unauthorized`, or on ToB HTTP 403 with `HOTEL_BUSINESS_PERMISSION_REQUIRED`, stop immediately and follow [access recovery](access_and_updates.md#auth-errors). Only a safely retryable, transient verification failure permits one retry of the selected rate. Report any unresolved verification error and stop before booking.
2. If the user is signed in and has not declined coupons, refresh [applicable coupons](search_and_pricing.md#compare) against the final availability check on the same account/channel. Let the user choose a returned coupon or keep the original price.
3. Present the full [booking review](response_templates.md#booking-review) and obtain explicit confirmation of the verified booking terms. If a coupon is selected, include its identity, discount and post-coupon room charge excluding payment fees. Signed-out users may review and confirm the original price before signing in to place the order.
4. Before submission require the correct stored credential (`uk_` as `user_key` for ToC; `sk_` as `token` for ToB). Follow [channel switching](access_and_updates.md#switch-channel): refresh rates, availability and applicable coupons for any change of identity, channel or quote. Never transfer rate codes, policy, price, availability or payment context between channels. Obtain new confirmation if the channel changes, one signed-in account replaces another (even at the same price), a checked quote for an already confirmed coupon booking changes, or the stay, occupancy, currency, coupon, price or other terms change. A signed-out user signing in on the same ToC channel may keep their original confirmation only if the recheck leaves all confirmed terms unchanged. Reconcile any unresolved creation before starting a different attempt.
5. Collect the guest's full legal name as on the identification document, and a contact email confirmed for this booking. Chinese and Latin-script names are supported; do not promise a transliteration. The email is mandatory, even if the service accepts omission: one `@`, nonempty local/domain parts, and a dot in the domain are basic plausibility checks. Explain it receives booking-success, booking-failure and cancellation notifications. Do not invent an email, reuse an unconfirmed one, offer to skip it, or ask for a phone number.
6. Send [`create_booking`](parameter_guide.md#create_booking) with the latest checked **pre-coupon** `total_price`. If a coupon is chosen, generate a 1–64-byte `request_id` and retain it with the exact business parameters. Send the selected `coupon_code` and confirmed `expected_payable_amount` in transaction-currency major units, excluding payment fees. A numeric zero is distinct from an absent field. If no coupon is selected, omit the coupon arguments and retain the ordinary booking flow.

On success return `data.agent_ref_id` and the returned pre-coupon total, actual discount and post-coupon room charge. Retain the order reference, owning account and creation channel. A normal first success omits `replayed`; `replayed=true` returns the existing order. Creation `request_state=SUCCEEDED` or `status=confirmed` does not establish hotel confirmation or payment. [Query the order](#order) for its current state. If `UNPAID`, use the currency from that response to [offer payment methods](#payment) supported by this client and ask the user to choose. Obtain separate payment confirmation before calling `pay_order`. Booking, payment and cancellation are separate, explicitly authorized operations and must run sequentially.

<a id="recovery"></a>
## Recover a creation attempt

| Outcome | Action |
|---|---|
| Explicit `FAILED_NO_ORDER`, or authoritative reconciliation that the attempt cannot still create an order | End that attempt. Refresh rates/coupons as needed and use a fresh ID for a new attempt. Reconfirm changed terms or amount. At most **one automatic new attempt** is allowed with existing booking authorization. Stop and report a repeat failure. |
| `PROCESSING`, `UNKNOWN`, timeout, lost connection or ambiguous response | Retain the **original ID and every business parameter**. Allow at most **two automatic identical retries** with a brief delay. If unresolved, stop automatic creation. Query a known order reference; if none is known, ask TourMind support to reconcile the original attempt. |
| `SUCCEEDED`, `replayed=true` or known existing order | Continue with that order. Do not create another booking. |
| Same ID with different parameters | Inspect and reconcile the original request. Do not bypass the conflict with a fresh ID. |
| Coupon unavailable, quota exhausted or payable amount changed | Refresh eligibility and obtain confirmation for the new terms. Do not silently remove the coupon or submit the original undiscounted total as the payable amount. Classify the previous attempt's outcome above before choosing an ID. |

An HTTP failure, `ok=false`, MCP `isError=true`, the words “booking failed”, order status `CONFIRM_FAILED`, or a lookup which has not found an order is insufficient to establish `FAILED_NO_ORDER`. The explicit state may be in the error text. Without an original `request_id`, do not blindly repeat creation.

<a id="order"></a>
## Query and interpret the order

Use [`query_booking`](parameter_guide.md#query_booking) with the exact `agent_ref_id` and the owning account on the creation channel. For a newly supplied order number, fetch its details instead of reusing the previous order's data. If the credential does not match, stop and request the credential used for that order. Do not try both channels.

| Current order status | Meaning |
|---|---|
| `UNPAID` | Created and awaiting payment. |
| `PENDING` | Paid, awaiting hotel confirmation. Do not ask for another payment. |
| `CONFIRMED` | Confirmed by the hotel. |
| `CANCELLED` | Cancelled. |
| `CONFIRM_FAILED` | Hotel confirmation failed. This does not establish that no order exists. |

Use outer `data.discount_amount` and `data.payable_amount` for the current discount and post-coupon room charge, in major units and excluding payment fees. `coupon_usage` is the current binding, not a history; its nested `discount_amount` is in **minor units**. Do not subtract the discount again. An elapsed reservation-expiry timestamp alone proves neither release nor payment. Use `query_booking.data.currency` for the order's transaction currency.

<a id="payment"></a>
## Confirm payment and issue the payment entry

1. Use the current order lookup on the creation channel. If this exact order was just queried after creation, use that result to offer methods. Otherwise query the order first. Only proceed for an order awaiting payment. Obtain a separate confirmation of the payment method, order amount and currency. For CNY, offer Stripe, WeChat Pay and Alipay. Alipay AI Pay is CNY-only and requires a client with the native Qwen cashier. For any non-CNY order, including USD, offer Stripe only. Display language, search currency, coupon-template currency and the checkout page's adaptive display currency do not select a method.
2. If Stripe is considered, show the [payment review](response_templates.md#payment-review) **before** requesting a link: current post-coupon room charge, Stripe's separate **3.5%** processing fee and fee-inclusive total in the order currency. Only use a returned fee preview if its base matches this exact room charge; otherwise label the fee and total as estimates. This is a Stripe processing fee, separate from room charges and taxes. Once charged it is **non-refundable, even during the hotel's free-cancellation period**. Obtain explicit acknowledgement of the method, fee, total and non-refundability.
3. Call [`pay_order`](parameter_guide.md#pay_order) using the supported payment method and order reference. The service uses the bound coupon snapshot: do not send any coupon arguments, deduct the discount again, or invent confirmation arguments. WeChat Pay and Alipay return `pay_url`, `expires_at` and `one_time`; Stripe returns a link and fee fields; Alipay AI Pay returns `prepay_id` for the native cashier. There is no custom return URL.
4. Reconcile Stripe's returned amounts in the order currency. In `pay_order.data`, `order_amount` is the **pre-coupon** room total and `discount_amount` is the discount. Subtract the discount once: the result must match the post-coupon room charge in `query_booking.data.payable_amount`. Add `stripe_payment_fee.fee_amount` to that room charge: the result must match both `pay_order.data.payable_amount` and `stripe_payment_fee.payable_amount` when returned. These payment totals **include** the Stripe fee; the coupon preview and order-query payables **exclude** it. For example, USD 460.80 − 1.49 = 459.31 in room charges; 459.31 + 16.08 = 475.39 due. If a field is absent, do not assume a zero discount or invent a fee; use the order query and available payment breakdown to verify the amounts. If the figures or currencies cannot be reconciled, withhold the link and clarify with TourMind support as needed. If the reconciled fee or total differs from what the user confirmed, show the difference and obtain fresh confirmation **before** sharing the link. Otherwise share the payment entry and verified breakdown.
5. A link, prepayment ID or success message is not proof of payment. After the user completes checkout, query the booking. If payment times out or its state is unknown, query the order before taking any further action; do not automatically request another payment.

<a id="cancel"></a>
## Cancel an order

Use the cancellation terms returned for this order or the verified terms recorded when this exact order was booked. If neither is available, explain that the charge cannot yet be verified and obtain the order confirmation or ask TourMind support for the terms before requesting cancellation confirmation. Never use a new room quote or call `cancel_booking` to discover the charge.

Confirm the exact order number, account and creation channel and obtain the current order details. Explain the hotel's cancellation terms, including any deadline and original timezone offset. `non_refundable` or `effective_non_refundable=true` means non-refundable; `free_cancel_before_deadline` means free only through the returned deadline. For legacy availability `cancelPolicyInfos`, `refundable: true` means refundable/cancellable, `startDateTime` is the free deadline and `amount` is the fee after it.

For a Stripe-paid order, explain before cancellation that any room refund follows hotel policy and the charged Stripe fee is **not refunded**, even if room cancellation is free. Obtain explicit cancellation confirmation after the disclosure and before calling [`cancel_booking`](parameter_guide.md#cancel_booking). Report the returned cancellation status, currency, cancellation charge and refund when provided. Do not promise a refund amount, coupon release or payment reversal from an expiry timestamp.
