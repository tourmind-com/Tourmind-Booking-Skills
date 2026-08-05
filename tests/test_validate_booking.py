from __future__ import annotations

import unittest

from scripts.validate_booking import (
    detect_kind,
    validate_booking_response,
    validate_detail_response,
    validate_rates_response,
    validate_search_response,
)


class ResponseValidatorTests(unittest.TestCase):
    def test_valid_search_warns_that_cached_price_is_not_live(self) -> None:
        result = validate_search_response(
            {
                "ok": True,
                "data": {
                    "hotels": [
                        {
                            "hotel_id": "H1",
                            "hotel_name": "Example Hotel",
                            "min_price": 500,
                            "currency_code": "CNY",
                            "distance_km": 1.2,
                        }
                    ]
                },
            }
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["hotel_count"], 1)
        self.assertTrue(any("cached" in warning for warning in result["warnings"]))

    def test_search_rejects_more_than_twenty_candidates(self) -> None:
        hotels = [
            {"hotel_id": f"H{index}", "hotel_name": f"Hotel {index}"}
            for index in range(21)
        ]
        result = validate_search_response({"ok": True, "data": {"hotels": hotels}})
        self.assertFalse(result["valid"])
        self.assertTrue(any("at most 20" in error for error in result["errors"]))

    def test_valid_live_rate_product(self) -> None:
        result = validate_rates_response(
            {
                "ok": True,
                "data": {
                    "room_types": [
                        {
                            "name": "Standard King",
                            "basic_room_image": "https://example.com/room.jpg",
                            "products": [
                                {
                                    "cancellation_policy": {"type": "non_refundable"},
                                    "rate": {
                                        "rate_code": "R1",
                                        "currency": "CNY",
                                        "total_price": 800,
                                        "per_night_price": 800,
                                        "is_on_request": False,
                                    },
                                }
                            ],
                        }
                    ]
                },
            }
        )
        self.assertTrue(result["valid"])
        self.assertTrue(result["bookable"])
        self.assertEqual(result["product_count"], 1)

    def test_empty_live_rates_are_not_bookable(self) -> None:
        result = validate_rates_response(
            {"ok": True, "data": {"room_types": []}}
        )
        self.assertFalse(result["valid"])
        self.assertFalse(result["bookable"])

    def test_detail_without_image_requires_explicit_fallback(self) -> None:
        result = validate_detail_response(
            {
                "ok": True,
                "data": {
                    "hotel": {
                        "hotel_id": "H1",
                        "name": "Example Hotel",
                        "address": "Example Street",
                    },
                    "rooms": [],
                },
            }
        )
        self.assertTrue(result["valid"])
        self.assertFalse(result["has_image"])
        self.assertTrue(any("no hero-image" in warning for warning in result["warnings"]))

    def test_booking_requires_nonempty_order_reference(self) -> None:
        result = validate_booking_response(
            {"ok": True, "data": {"agent_ref_id": "", "status": "UNPAID"}}
        )
        self.assertFalse(result["valid"])

    def test_ambiguous_response_kind_is_not_guessed(self) -> None:
        self.assertIsNone(
            detect_kind({"ok": True, "data": {"hotels": [], "room_types": []}})
        )


if __name__ == "__main__":
    unittest.main()
