# User-facing response templates

Translate all user-facing text into the current request language unless the user asks for another. Preserve returned facts, variable names, IDs, Markdown structure, URL tickets, and actual API field/enum values. Use only one language unless bilingual output is requested. Quote raw API errors verbatim and explain them in the user’s language.

Whenever a hotel list, room detail, booking review or cancellation message shows a free-cancellation deadline, show the exact returned date and time with its original timezone offset. Do not drop or silently convert the timezone.

<a id="first-run"></a>

## First-run welcome

Resolve the [shared credential](access_and_updates.md#credentials) first. Show the complete welcome and all three examples once, immediately after installation and before the first hotel task. Translate the text without summarizing, shortening, or turning it into a feature list. Preserve product names and URLs. If either supported location yields a usable token, replace only the final authorization paragraph with:

> Authorization is configured. I will not display or repeat the stored Token.

````markdown
### TourMind Booking Skill is ready

You can start using it now.

You can ask me like this:

```text
I am visiting Paris next month for four nights with one other person. I would like to stay near the Louvre or the Opera, with a budget of about EUR 200 per night. Help me find a few well-located hotels.
```

```text
I am taking my family to Tokyo this summer and would like to stay near Shinjuku. I prefer somewhere quiet, with breakfast and free cancellation. Pick a few hotels and explain who each one suits.
```

```text
I am planning a honeymoon in Bali and want to stay in Nusa Dua, preferably by the beach with a pool and under USD 300 per night. Show me some suitable resorts.
```

For access to the best channel prices and price-markup and commission capabilities, apply for a business account at [TourMind registration](https://tourmind.com/admin/skillSignup). Registered users or users who already have a TourMind account can visit [Create a private token](https://tourmind.com/user/skill-token), create a TourMind private token, and send it to me to connect the business channel.
````

<a id="sign-in"></a>

## Sign-in guidance

Show both choices after [credential resolution](access_and_updates.md#credentials) finds no usable token and the user requests coupons, proceeds to create a booking, or requests an order operation. This also applies without the sibling flight Skill. Do not interrupt public browsing, availability or the pre-coupon review with this message. For a rejected known credential, show the matching branch as specified under [authorization errors](access_and_updates.md#auth-errors).

> Before checking your available coupons, continuing with a booking, or managing an order, please tell me whether you are a personal user or a business user:
>
> - Personal user: open [Journione sign-in](https://auth.journione.ai), sign in by verifying your email, then copy the token beginning `uk_` from the right side of the page and send it to me. If you have trouble registering or signing in, I can open the link in my built-in browser and help you complete the process.
> - Business user: first sign in to your TourMind account, then visit [Create a private token](https://tourmind.com/user/skill-token), create a TourMind private token beginning `sk_`, and send it to me.

<a id="hotel-list"></a>

## Hotel list

Use this English template as the canonical structure for every multi-hotel result. Default to five selected hotels. Translate all user-facing labels, guidance, and prose into the user's language while preserving the Markdown structure, variables, numbers, URLs, and returned facts. Do not include a duplicate English version unless the user requests bilingual output.

```markdown
Found {candidate_count} candidate hotels and verified live room products for {verified_scope}; below are the {selected_count} selected based on “{ranking_dimensions}”.

Search area: {region_or_poi_and_radius_resolution_note}
Stay: {check_in_date} to {check_out_date}, {night_count} nights
Guests: {total_adults} adults, {total_children} children, {room_count} rooms ({occupancy_distribution})
Price basis: Per room per night and total for all rooms and nights.
Display currency: {display_currency}

👉 More hotels: [View detailed hotel results]({web_url}). Open a hotel, click “Copy” beside the desired room, and send it to me to book.

### 1. {hotel_name}

![{hotel_name} hero image]({hotel_image_render_target})

[View hotel details]({hotel_web_url})

| Distance | Star rating | Lowest matching room product | Meal | Per night | Stay total | Cancellation | Inventory status |
|---:|---:|---|---|---:|---:|---|---|
| {distance} | {star_rating} | {room_name} | {meal_summary} | {display_nightly_price} | {display_stay_total_and_price_label} | {cancellation_summary} | {bookable_or_on_request} |

Why it matches: {reason_1}; {reason_2}; {optional_reason_3}.

Address: {address}
```

Immediately below the final displayed hotel, include the localized equivalent of this note:

> Prices are shown in {display_currency}. {live_conversion_note_if_applicable} Tell me if you would like to see them in another currency.

When conversion was required, replace `{live_conversion_note_if_applicable}` with the localized equivalent of `Converted amounts are approximate, using {exchange_rate} from {exchange_rate_source}, retrieved at {exchange_rate_timestamp}.` When no conversion was required, omit that sentence without leaving an empty placeholder.

Set `{verified_scope}` truthfully. Use the localized equivalent of `all candidates` only after querying live room products for every candidate; otherwise use the localized equivalent of `all candidates that passed the hard constraints`. The default `{ranking_dimensions}` concepts are `immediate bookability, distance, stay total, cancellation flexibility`; translate them into the user's language, adding or replacing dimensions when the user supplied explicit filters or sorting preferences.

If `search_hotels.data.web_url` is absent, omit the entire `👉 More hotels` paragraph. Never require a token only to populate this optional link.

Place the result link between the search summary and first hotel, with a blank line on each side. Keep the underlying credential private. The result page only shows hotel lists, details and room quotes. Verification, booking, payment, `/book/*`, order, finance and account management stay outside the read-only page. Apply the [result-page locale mapping](parameter_guide.md#returned-result-page-url-language) to each returned list or detail URL.

Use `search_hotels.data.total` or the returned list length for candidate count, `distance_km` from the candidate for distance, and the selected hotel’s detail to verify its name and star rating. For the address, use `get_hotel_detail.data.hotel.address_cn`, then `address`. Give the two or three strongest verified reasons in one line; use the exact product for room, meal, cancellation and on-request status. In a complete-pool view, separate matches and non-matches, state each failed constraint and display “No matching live room or quote” for unmatched products.

Use the price already determined by [comparison](search_and_pricing.md#compare) for the stay total. Show the coupon identity and “After coupon” for a discounted quote and label its nightly figure as an average per room per night. A successful empty list uses the checked price without a coupon label. If the user asked about discounts for that quote, say in the response language: “No coupons are currently available for this quote.” Mark a failed lookup “Before coupons; coupon check unavailable” and keep it separate from verified after-coupon rankings and budget matches. For explicitly pre-coupon budgets, state that basis even if you also show a discount. Label supplier-confirmation inventory explicitly. The cancellation deadline includes its exact returned time-zone offset.

On the first priced result of a signed-out search (hotel list or room detail), show this invitation once in the response language: “Register or sign in to see available coupons. You may get a lower price.” Continue with public results; do not repeat it for each room or interrupt the booking review.

Hero-image rendering rules for both hotel-list and hotel-detail responses:

- Select the original hero-image URL from `hotel.hotel_image`; otherwise use the `Primary image` from `image_groups` (prefer a valid `1000px` or largest `href`), then the first valid `hotel_images` item.
- If the user is currently using this Skill in the ChatGPT or Codex client, download the selected returned hero image to a client-accessible local file before responding. Set `{hotel_image_render_target}` to the file's absolute filesystem path; do not use the remote URL as the primary image render target.
- In other clients, set `{hotel_image_render_target}` to the selected original URL.
- Never expose the original hero-image URL as a separate link. If the local download fails or does not produce an accessible image file, omit the broken Markdown image.
- Directly below the image, or below the unavailable-image notice, show the localized equivalent of `[View hotel details]({hotel_web_url})` using the exact hotel's `query_room_rates.data.web_url` or successful `batch_query_room_rates` item's `data.web_url`. Translate only the link label; after the required locale-path substitution, preserve the rest of the URL exactly.
- Never substitute the hotel-list `search_hotels.data.web_url`, an image URL, or a constructed URL for `{hotel_web_url}`. If the corresponding live-rate response has no `data.web_url`, omit the hotel-detail link.
- If no hero-image URL exists, write the localized equivalent of `A hero image is not currently available for this hotel.` and continue with the hotel-detail link when available.

For each selected hotel:

- Use the live room product for room name, price, meal, cancellation and on-request status.
- Show both per-night and stay-total price in the selected display currency: CNY for Chinese requests, USD for non-Chinese requests, or the user's explicitly requested currency. Convert with a current live exchange rate when necessary and keep the returned transaction currency and amounts unchanged for later verification and booking.
- Show a fee or tax note only when the API explicitly returns a fee, tax amount, or inclusion status, or when the user asks about taxes and fees. Do not notify the user that fee or tax data is absent, incomplete, or unknown.

End every default five-hotel list with the localized equivalent of this English source text:

> These are the {selected_count} best matches selected from {candidate_count} returned candidates. If they are not suitable, I can show the remaining {remaining_count} candidates or the complete result set; candidates that fail hard constraints will be clearly labeled with the reasons. Reply with a hotel number or name to see its room types, room images, and corresponding live quotes.

Adjust the sentence when fewer than five qualify or when all results are already shown.

<a id="room-detail"></a>

## Hotel and room details

Show the selected hotel’s summary, images and matching live quotes together. Include the hero image (see hotel-list rules), address, stars, distance, check-in/out and facilities. Show a fee summary only if a fee was returned or the user asks. After [comparing](search_and_pricing.md#compare), list up to five distinct room products by default in the requested order and offer the rest. Use the same price labels and search-wide invitation as the hotel list. For every product, render:

If `query_room_rates.data.web_url` exists, include it as a clickable read-only hotel and room-rate page. The linked page only displays hotel details and room quotes. It does not support price verification, booking, payment, `/book/*`, order management, finance or account management. Continue those actions in the current conversation through the Skill APIs. If no link is returned, continue with the room-rate response and do not require sign-in.

```markdown
#### {room_name}

![{room_name} room image]({basic_room_image})

| Bed type | Capacity per room (adults + children) | Meal | Per night | Stay total | Cancellation | Inventory status |
|---|---|---|---:|---:|---|---|
| {bed_type} | {adult_child_capacity_summary} | {meal_summary} | {display_nightly_price} | {display_stay_total_and_price_label} | {cancellation_summary} | {bookable_or_on_request} |
```

Room-image rules:

- Prefer `query_room_rates.data.room_types[].basic_room_image` for the exact live room type.
- Otherwise use the matching `get_hotel_detail.rooms[].basic_room_image` only when the room code/name maps confidently.
- If only a generic hotel room gallery exists, use the localized label equivalent of `Generic hotel room image; not guaranteed to match the quoted room type`.
- If no matching image exists, say so and omit the image. Never attach an unrelated image.

For a Chinese response, use nonempty `name_cn`, then `name`. For other languages use `name`, then `name_cn`. Treat empty or `Others` as “Other / room assigned at check-in”. Show the bed, separate adult and child limits, meal name and quantity, nightly and stay prices, cancellation and `is_on_request` status together.

- Interpret meals using [Meal type mapping](parameter_guide.md#meal-type-mapping), including numeric and string codes 1–19. `meal_type=2` means breakfast for the booked guests; `meal_type=4` means two breakfasts. `meal_count` is supplementary and must not override a known type, including when it is zero.
- Match and display capacity using [Adult and child capacity](parameter_guide.md#adult-and-child-capacity). `maxOccupancy` / `max_occupancy` limits adults; a returned `maxChildren` / `max_children` permits additional children. For `2` and `1`, show `Up to 2 adults + 1 child per room`; compare adult and child counts separately for every room and retain the requested child ages through availability checking.

End with a clear next action: the user can choose a room for final availability and price verification. Then include the same localized currency note used by the hotel-list template so the user knows which currency is shown and can request another display currency.

<a id="booking-review"></a>

## Booking review

Display the following review using the latest verified quote and policy. A signed-out guest may review the pre-coupon price. Room selection alone is not confirmation. Use hotel detail for check-in/out times, instructions and explicit mandatory fees. For missing times say “Not provided by the hotel”. If no mandatory fees were disclosed, use “The hotel did not return any additional mandatory fee information.” Do not add prose fees numerically unless the amount and charging basis are unambiguous. Always show both occupancy rows; when there are no children show “0 children” and “Not applicable”.

```markdown
### Please confirm your booking

| Item | Verified details |
|---|---|
| Hotel | {hotel_name} |
| Room | {room_name} |
| Check-in date | {check_in_date} |
| Check-out date | {check_out_date} |
| Check-in / check-out time | Check-in from {checkin_begin_time_or_not_provided}; check-out by {checkout_time_or_not_provided} |
| Occupancy | {adults_per_room} adults and {children_per_room} children per room; {room_count} rooms |
| Children's ages | {children_ages_per_room_or_not_applicable} per room |
| Room price total | {checked_total_price} {currency} |
| Cancellation policy | {checked_cancellation_policy} |
| Availability | {checked_availability_status} |

**At-property charges**

{mandatory_fee_summary_or_fallback}

Our prices include taxes. However, in a small number of countries or regions, city or tourism taxes must be collected directly by the hotel. The final amount is determined by the hotel and may be charged when you check in. Please be aware of this possible additional charge and plan accordingly. Thank you for your understanding.

TourMind Customer Service

- **+86-021-67572867** — 08:00–23:59 (UTC+8)
- **+1-833-5504358** — 24/7

Please review the booking details above. To proceed, reply **“Confirm booking”** and provide the guest's **full legal name** and **contact email**. I will then create the booking and continue to payment.
```

Only for a chosen coupon, insert these rows immediately after `Room price total` (which remains the pre-coupon amount). Use the selected preview’s transaction currency and obtain explicit confirmation of the amounts. Omit all three rows if the user does not select a coupon. If the user asked about discounts for this quote and the current account’s latest lookup for it succeeded with `coupons=[]`, add a sentence next to the review in the response language: “No coupons are currently available for this quote.” A skipped or failed lookup does not establish this result.

```markdown
| Coupon | {coupon_code} |
| Coupon discount | {discount_amount} {currency} |
| Room charge after coupon (payment fee excluded) | {payable_amount} {currency} |
```

Ask: “Please provide a contact email. It is required to place the booking and will receive booking-success, booking-failure, and cancellation notifications.” The guest’s full legal name must match their identification. Confirm that the plausible email belongs to this booking; do not promise a specific transliteration of a Chinese or Latin-script name.

<a id="payment-review"></a>

## Payment review

After creation, show the order reference, returned pre-coupon total, actual discount and post-coupon room charge. When a retry returns an existing order say so. Describe the current order status according to the order lookup; a created order, a link or a prepayment ID alone does not prove payment or hotel confirmation. Use [payment rules](booking_and_payment.md#payment) to determine which methods to offer and how to verify the amounts.

Only when Stripe is under consideration, show the following review before requesting a link. If the fee and total are estimates, label both clearly. The 3.5% fee is charged by Stripe, separately from the room price, hotel taxes and TourMind charges. Show the actual returned fee and total with the link after reconciliation. If the amounts differ from the confirmed review, present the difference and obtain new confirmation before showing the link.

```markdown
### Please review your Stripe payment

| Item | Amount ({currency}) |
|---|---:|
| Room charge after any coupon | {post_coupon_room_charge} |
| Stripe processing fee (3.5%) | {fee_amount_or_labeled_estimate} |
| Total including Stripe fee | {fee_inclusive_total_or_labeled_estimate} |

Once charged, the Stripe processing fee is non-refundable, even if you cancel within the hotel's free-cancellation period. Please confirm that you choose Stripe and accept the fee and its non-refundable terms before I request the payment link.
```

For a WeChat Pay or Alipay link, present the returned expiry and one-time-use status. Alipay AI Pay uses the native Qwen cashier and a `prepay_id`; it does not produce a normal clickable link.

<a id="cancellation"></a>

## Cancellation notice

Before cancelling, ask the user to confirm the exact order reference and its creation channel. Show the applicable cancellation deadline with its returned time-zone offset and the penalty after it. If paid via Stripe, state: “Your room-charge refund follows the hotel’s cancellation policy. The Stripe processing fee already charged will not be refunded, even during free cancellation.” Obtain explicit cancellation confirmation after the notice.
