# TourMind Booking Skill

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [Español](README.es.md)

Turn any AI agent into an end-to-end hotel booking assistant—search global inventory, compare live rates across leading OTAs and hotel suppliers, verify availability, and complete booking, payment, cancellation, and order management in one conversation with TourMind.

## Demo

> **TODO:** Add a real end-to-end screenshot or short GIF showing hotel search, live room rates, final availability verification, and booking.

## Core capabilities

- Resolve cities, hotels, landmarks, stations, addresses, ski areas, and other POIs without inventing coordinates.
- Search up to 20 hotel candidates, query matching live room products, and select the five best verified options.
- Compare live nightly and stay-total rates across leading OTAs and hotel suppliers, including cancellation and inventory status.
- Return hotel and room images, facilities, beds, meals, fees, and evidence-based match reasons.
- Recheck the selected room's price and availability before booking.
- Create bookings, query and cancel orders, and start Stripe, WeChat Pay, or Alipay payments.
- Provide expiring, repeatable, read-only result links without exposing the Skill Token.

## Supported AI clients

| Client | Support |
|---|---|
| OpenAI Codex | Supported as a local Skill installed under `~/.codex/skills` |
| Agent Skills-compatible clients | Compatible when the client can load a root `SKILL.md` and make outbound HTTPS `POST` requests |
| MCP-capable AI clients | Use the companion [TourMind Booking MCP](https://github.com/tourmind-com/Tourmind-Booking-MCP) package |

## Install in 1 minute

1. Clone the Skill into Codex:

   ```bash
   mkdir -p ~/.codex/skills
   git clone https://github.com/tourmind-com/Tourmind-Booking-Skill.git ~/.codex/skills/tourmind-booking
   ```

2. Generate a Skill Token at [tourmind.com/user/skill-token](https://tourmind.com/user/skill-token), save the raw token as `~/.codex/skills/tourmind-booking/skill_token.txt`, and restrict access:

   ```bash
   chmod 600 ~/.codex/skills/tourmind-booking/skill_token.txt
   ```

3. Restart the AI client and ask for a hotel. No local MCP server is required; this Skill calls the TourMind API directly over HTTPS.

Never commit `skill_token.txt`. It is excluded by `.gitignore`.

## Example prompts

```text
Find a hotel near Shenzhen Xili Metro Station for two adults from September 12 to September 14, within 3 km.
```

```text
Show the best five hotels with verified live room rates, breakfast, cancellation terms, and stay totals.
```

```text
Show every candidate returned by the hotel search and clearly label any option that failed my hard constraints.
```

```text
Recheck the selected room, then help me book and pay after I confirm the final price and cancellation policy.
```

## Workflow

```text
Location or POI
  → search_location
  → search_hotels (up to 20 candidates)
  → query_room_rates (live products for eligible candidates)
  → rank and present the five best verified hotels
  → get_hotel_detail + room images and quotes
  → check_room_availability for the selected rate
  → create_booking after explicit confirmation
  → pay_order / query_booking / cancel_booking as requested
```

Cached `search_hotels.min_price` is only a candidate signal. User-visible prices come from `query_room_rates`, and the final booking uses the latest values returned by `check_room_availability`.

## Token and security

- All ToB Skill API calls require the Skill Token stored locally in `skill_token.txt`.
- Keep the token out of prompts, logs, screenshots, URLs, commits, and issue reports.
- Restrict the token file to the current user with `chmod 600`.
- On HTTP 401 or an `unauthorized` response, remove the invalid local token and generate a replacement.
- Result `web_url` sessions are read-only and can be opened repeatedly until they expire; they cannot verify rates, book, pay, cancel, or access account and finance pages.
- Booking, cancellation, and payment remain explicit user-confirmed actions inside the authenticated AI conversation.

## Choose the right TourMind integration

| Audience | Integration | Authentication model | Repository |
|---|---|---|---|
| Consumer / ToC | Direct HTTP Skill | Public search and availability; `user_key` only for order operations | [Hotel Booking AI](https://github.com/tourmind-com/Hotel-Booking-AI) |
| Business / ToB | Direct HTTP Skill | Skill Token required for every API call | **[TourMind Booking Skill](https://github.com/tourmind-com/Tourmind-Booking-Skill)** |
| Consumer / ToC | MCP package + companion Skill | Public MCP connection; `user_key` only for order operations | [Hotel Booking AI MCP](https://github.com/tourmind-com/Hotel-Booking-AI-MCP) |
| Business / ToB | MCP package + companion Skill | Bearer-authenticated MCP connection | [TourMind Booking MCP](https://github.com/tourmind-com/Tourmind-Booking-MCP) |

## API and support

**API base URL:** `https://api.tourmind.com`

| Endpoint | Purpose |
|---|---|
| `POST /skill/tob/check_skill_update` | Check for a Skill update |
| `POST /skill/tob/search_location` | Resolve a region, POI, or hotel |
| `POST /skill/tob/search_hotels` | Search hotel candidates |
| `POST /skill/tob/get_hotel_detail` | Get hotel details and images |
| `POST /skill/tob/query_room_rates` | Get live rooms and rates |
| `POST /skill/tob/check_room_availability` | Recheck the selected rate and inventory |
| `POST /skill/tob/create_booking` | Create a confirmed booking |
| `POST /skill/tob/query_booking` | Query an order |
| `POST /skill/tob/cancel_booking` | Cancel an order after confirmation |
| `POST /skill/tob/pay_order` | Start payment after confirmation |

- Request fields and response contracts: [references/parameter_guide.md](references/parameter_guide.md)
- Skill Token: [tourmind.com/user/skill-token](https://tourmind.com/user/skill-token)
- Product page: [tourmind.com/skill](https://tourmind.com/skill)
- GitHub support: [open an issue](https://github.com/tourmind-com/Tourmind-Booking-Skill/issues)
- Hotel business inquiry: `hotel@tourmind.com`
- Business cooperation: `bp@tourmind.com`

## License

[MIT](LICENSE) © 2026 TourMind
