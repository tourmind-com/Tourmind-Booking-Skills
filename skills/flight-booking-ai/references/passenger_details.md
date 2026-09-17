# Passenger details and booking/payment confirmation

Read this reference as soon as passenger composition is known, before searching, collecting booking data, or presenting a booking/payment confirmation. Use the canonical structures in [response templates](response_templates.md); do not recreate fixed customer-facing text here.

## Passenger-composition gate

In this booking flow, each actual accompanying adult can carry at most one infant, and an infant cannot buy a ticket alone. Check `adults >= 1` and `infants <= adults` before flight search, verification, and booking, and recheck whenever counts or ages change. If infants are mentioned but accompanying adults are unknown, ask for the actual composition first; do not assume an adult. Booking associations must link each infant to a different actual adult in the same booking.

When the group is unsupported, use the [unsupported passenger composition template](response_templates.md#unsupported-passenger-composition), preserve every actual passenger, birthday, and age-based type, and stop the affected requests. Never add adults, omit infants, reduce infant counts, relabel an infant as a child, or split the group into orders to evade the requirement.

Ask whether the user wants to explore an alternative before pursuing it. Change the active group only when the user confirms a real change in travel plans. Such a change invalidates prior quotations and verification and requires approval for a new search. Do not present extra adults, infant seat purchases, child fares, or split orders as guaranteed solutions. Verify any proposed alternative against the relevant airline's current official policy or provider/customer-service confirmation for the itinerary. Record the source internally. Passing the numerical gate alone does not prove airline eligibility, seat availability, price, or bookability.

## Age and quotation consistency

Use date of birth and the itinerary's departure date to determine pricing type:

- Adult: 12 years or older.
- Child: 2 years to under 12 years.
- Infant: 14 days to under 2 years.

A baby under 14 days is outside the supported infant range; stop booking and refer the user to customer service. If a birthday crosses a type boundary during a multi-leg itinerary, obtain provider or customer-service confirmation before quoting or booking. Keep the actual birthday and pricing type.

If an accompanying passenger's airline eligibility is unresolved, pause booking even when the pricing type passes local validation. A pricing type does not establish eligibility to accompany an infant.

The normal search flow confirms all passenger counts before searching. If later passenger data differs from the quotation, invalidate the quotation, session, and confirmation. Use the [passenger-composition requotation template](response_templates.md#passenger-composition-requotation), confirm the actual composition, apply the composition gate, and obtain approval for a fresh search. Never reuse an adult price for a child or infant, change a type or birthday, fabricate an accompanying adult, or multiply an old price to construct a group quotation.

## Collect details in one message

Use the [passenger and contact collection template](response_templates.md#passenger-and-contact-collection). Do not ask again for valid information already supplied; request all remaining or invalid fields together.

For every passenger, require:

- `type`
- `first_name`
- `last_name`
- `birthday`
- `sex`
- `nationality`
- `card_type`
- `card_no`
- `card_expired`
- `card_issue_place`

Also require `contact.name`, `contact.phone`, and `contact.email`. These fields are required by this Skill even when the verified API reports `support_no_card=true`.

Map the travel-document given name to `first_name` and surname to `last_name`. Never infer a split from an ambiguous combined name or invent a transliteration. Normalize unambiguous localized sex, document-type, and country inputs to supported API values, but do not alter the underlying fact. Nationality and document-issuing country are independent fields. Do not require an optional contact address or a separate area code when the supplied phone number is usable. Each infant also requires its associated adult passenger.

## Booking confirmation

After all fields pass validation, use the [shared review tables](response_templates.md#shared-review-tables) followed by the [booking confirmation template](response_templates.md#booking-confirmation). Populate itinerary facts from the verified offer. Repeat one row per segment and one passenger table per passenger.

Show all required passenger, document, and contact values in full in this user-requested confirmation view. Never include a Token. Ordinary summaries, logs, and diagnostics remain redacted.

Any correction cancels the previous confirmation. Revalidate the data and show the complete updated review before requesting a new explicit confirmation. A passenger count or type change also requires a new search and verification.

## Payment confirmation

Use the immediately preceding successful `query_order` response as the authority for order number, status, itinerary, passenger names/types/counts, amount, currency, and payment deadline. Before offering payment methods or rendering a payment review, apply the payable-order rules in the [parameter guide](parameter_guide.md#payable-order-gate). Continue only for an eligible order. Otherwise use the [payment-unavailable template](response_templates.md#payment-unavailable) and stop payment creation.

Render the [shared review tables](response_templates.md#shared-review-tables) followed by the [payment confirmation template](response_templates.md#payment-confirmation). Show payment methods only through their documented public labels; API request values are never user-visible. When Stripe is selected, include the template's Stripe fee-acknowledgement block and require explicit acknowledgement of both the additional 3.5% processing fee and its non-refundable nature. Do not show or apply that fee for another method.

The order API omits document and contact data. Supplement them only from validated booking data already confirmed for this exact order in the current conversation. Never use another order's data, invent missing fields, or claim that omitted data was reverified by the query. If the query conflicts with known passenger data, stop payment creation and refer corrections to customer service.

For an existing order with no matching complete booking data in the conversation, show every returned passenger's full first name, last name, and type. Omit unavailable document/contact rows and explain once that the query did not return those details. Do not collect documents solely to fill the payment review.

Payment confirmation is separate from booking confirmation and payment-method selection. Any reviewed change requires the complete updated payment review and a new explicit confirmation. Switching to or from Stripe invalidates the prior confirmation. Passenger or contact corrections on an existing order require customer service; payment creation cannot update the booking.

After explicit payment confirmation, query the order again immediately before payment creation and reapply the complete payable-order gate. If that query fails or shows a nonpayable order, do not call payment creation. If any reviewed fact changed but the order remains payable, render the complete updated review and obtain a new explicit confirmation.
