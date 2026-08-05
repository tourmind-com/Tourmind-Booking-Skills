#!/usr/bin/env python3
"""Validate representative TourMind Skill API responses.

Usage:
    python3 scripts/validate_booking.py auto '<json_response>'
    python3 scripts/validate_booking.py search '<json_response>'
    python3 scripts/validate_booking.py rates '<json_response>'
    python3 scripts/validate_booking.py detail '<json_response>'
    python3 scripts/validate_booking.py booking '<json_response>'

The validator checks current ToB response shapes. It does not call live APIs or
create bookings.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from typing import Any, Dict, Iterable, List, Optional, Tuple


Result = Dict[str, Any]


def _result(kind: str, errors: List[str], warnings: List[str], **extra: Any) -> Result:
    return {
        "kind": kind,
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        **extra,
    }


def _require_fields(value: Dict[str, Any], fields: Iterable[str], path: str) -> List[str]:
    return [f"{path} missing required field: {field}" for field in fields if field not in value]


def _is_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def _is_nonnegative_number(value: Any) -> bool:
    return _is_number(value) and value >= 0


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_identifier(value: Any) -> bool:
    return (
        isinstance(value, int)
        and not isinstance(value, bool)
        and value >= 0
    ) or _is_nonempty_string(value)


def _valid_image_url(value: Any) -> bool:
    return _is_nonempty_string(value) and value.startswith(("http://", "https://"))


def _has_group_image(image_groups: Any) -> bool:
    if not isinstance(image_groups, list):
        return False
    for group in image_groups:
        if not isinstance(group, dict):
            continue
        images = group.get("images")
        if not isinstance(images, list):
            continue
        for image in images:
            if not isinstance(image, dict):
                continue
            links = image.get("links")
            if not isinstance(links, dict):
                continue
            for link in links.values():
                if isinstance(link, dict) and (
                    _valid_image_url(link.get("href"))
                    or _valid_image_url(link.get("local_href"))
                ):
                    return True
    return False


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"Non-standard JSON numeric constant: {value}")


def _unwrap(response: Any) -> Tuple[Any, List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    if not isinstance(response, dict):
        return response, errors, warnings

    if "ok" not in response:
        warnings.append("Response has no top-level 'ok' field; validating as raw data")
        return response.get("data", response), errors, warnings

    if response.get("ok") is not True:
        error = response.get("error")
        errors.append(f"API response is not successful: {error!r}")
        return response.get("data"), errors, warnings

    if "data" not in response:
        errors.append("Successful API response missing top-level data")
        return None, errors, warnings
    return response["data"], errors, warnings


def validate_search_response(response: Any) -> Result:
    data, errors, warnings = _unwrap(response)
    if isinstance(data, list):
        hotels = data
    elif isinstance(data, dict):
        hotels = data.get("hotels")
    else:
        hotels = None

    if not isinstance(hotels, list):
        errors.append("search data.hotels must be a list")
        return _result("search", errors, warnings, hotel_count=0)

    for index, hotel in enumerate(hotels):
        path = f"hotels[{index}]"
        if not isinstance(hotel, dict):
            errors.append(f"{path} must be an object")
            continue
        errors.extend(_require_fields(hotel, ["hotel_id"], path))
        if "hotel_id" in hotel and not _is_identifier(hotel["hotel_id"]):
            errors.append(f"{path}.hotel_id must be a non-empty string or non-negative integer")
        if not any(hotel.get(key) for key in ("hotel_name_cn", "hotel_name", "name_cn", "name")):
            errors.append(f"{path} missing a usable hotel name")
        if "distance_km" in hotel and not _is_nonnegative_number(hotel["distance_km"]):
            errors.append(f"{path}.distance_km must be a finite non-negative number")
        if "min_price" in hotel and not _is_nonnegative_number(hotel["min_price"]):
            errors.append(f"{path}.min_price must be a finite non-negative number")
        if "min_price" in hotel:
            warnings.append(f"{path}.min_price is cached and must not be presented as a live quote")
            if not _is_nonempty_string(hotel.get("currency_code")):
                errors.append(f"{path}.currency_code must be a non-empty string when min_price is present")

    if len(hotels) > 20:
        errors.append(f"search returned {len(hotels)} hotels; endpoint contract allows at most 20")
    if not hotels:
        warnings.append("No hotel candidates returned; this may be valid for the constraints")
    return _result("search", errors, warnings, hotel_count=len(hotels))


def _iter_products(room_types: List[Any]) -> Iterable[Tuple[str, Dict[str, Any]]]:
    for room_index, room in enumerate(room_types):
        if not isinstance(room, dict):
            continue
        products = room.get("products", [])
        if not isinstance(products, list):
            continue
        for product_index, product in enumerate(products):
            if isinstance(product, dict):
                yield f"room_types[{room_index}].products[{product_index}]", product


def validate_rates_response(response: Any) -> Result:
    data, errors, warnings = _unwrap(response)
    room_types = data.get("room_types") if isinstance(data, dict) else None
    if not isinstance(room_types, list):
        errors.append("rates data.room_types must be a list")
        return _result("rates", errors, warnings, room_type_count=0, product_count=0)

    for index, room in enumerate(room_types):
        path = f"room_types[{index}]"
        if not isinstance(room, dict):
            errors.append(f"{path} must be an object")
            continue
        if not any(room.get(key) for key in ("name_cn", "name")):
            warnings.append(f"{path} has no room name; render as 其它/入住时确认房型")
        if not _valid_image_url(room.get("basic_room_image")):
            warnings.append(f"{path} has no exact live room image")
        products = room.get("products", [])
        if not isinstance(products, list):
            errors.append(f"{path}.products must be a list")
            continue
        for product_index, product in enumerate(products):
            if not isinstance(product, dict):
                errors.append(f"{path}.products[{product_index}] must be an object")

    product_count = 0
    for path, product in _iter_products(room_types):
        product_count += 1
        errors.extend(_require_fields(product, ["cancellation_policy", "rate"], path))
        cancellation = product.get("cancellation_policy")
        if not isinstance(cancellation, dict):
            errors.append(f"{path}.cancellation_policy must be an object")
        else:
            errors.extend(_require_fields(cancellation, ["type"], f"{path}.cancellation_policy"))
            if "type" in cancellation and not _is_nonempty_string(cancellation["type"]):
                errors.append(f"{path}.cancellation_policy.type must be a non-empty string")

        rate = product.get("rate")
        if not isinstance(rate, dict):
            errors.append(f"{path}.rate must be an object")
            continue
        errors.extend(
            _require_fields(
                rate,
                ["rate_code", "currency", "total_price", "per_night_price", "is_on_request"],
                f"{path}.rate",
            )
        )
        if "rate_code" in rate and not _is_nonempty_string(rate["rate_code"]):
            errors.append(f"{path}.rate.rate_code must be a non-empty string")
        if "currency" in rate and not _is_nonempty_string(rate["currency"]):
            errors.append(f"{path}.rate.currency must be a non-empty string")
        for field in ("total_price", "per_night_price"):
            if field in rate and not _is_nonnegative_number(rate[field]):
                errors.append(f"{path}.rate.{field} must be a finite non-negative number")
        if "is_on_request" in rate and not isinstance(rate["is_on_request"], bool):
            errors.append(f"{path}.rate.is_on_request must be boolean")

    if product_count == 0:
        errors.append("No usable live products returned; hotel must not be presented as bookable")
    return _result(
        "rates",
        errors,
        warnings,
        room_type_count=len(room_types),
        product_count=product_count,
        bookable=product_count > 0 and not errors,
    )


def validate_detail_response(response: Any) -> Result:
    data, errors, warnings = _unwrap(response)
    hotel = data.get("hotel") if isinstance(data, dict) else None
    rooms = data.get("rooms", []) if isinstance(data, dict) else []
    if not isinstance(hotel, dict):
        errors.append("detail data.hotel must be an object")
        return _result("detail", errors, warnings, room_count=0)

    errors.extend(_require_fields(hotel, ["hotel_id"], "hotel"))
    if "hotel_id" in hotel and not _is_identifier(hotel["hotel_id"]):
        errors.append("hotel.hotel_id must be a non-empty string or non-negative integer")
    if not any(_is_nonempty_string(hotel.get(key)) for key in ("name_cn", "name")):
        errors.append("hotel missing a usable name")
    if not any(_is_nonempty_string(hotel.get(key)) for key in ("address_cn", "address")):
        warnings.append("hotel has no address")

    image_groups = hotel.get("image_groups")
    hotel_images = hotel.get("hotel_images")
    has_image = (
        _valid_image_url(hotel.get("hotel_image"))
        or (
            isinstance(hotel_images, list)
            and any(_valid_image_url(item) for item in hotel_images)
        )
        or _has_group_image(image_groups)
    )
    if not has_image:
        warnings.append("hotel has no hero-image source; output must show an explicit no-image state")
    if not isinstance(rooms, list):
        errors.append("detail data.rooms must be a list when present")
        rooms = []
    else:
        for index, room in enumerate(rooms):
            if not isinstance(room, dict):
                errors.append(f"rooms[{index}] must be an object")
    return _result("detail", errors, warnings, room_count=len(rooms), has_image=has_image)


def validate_booking_response(response: Any) -> Result:
    data, errors, warnings = _unwrap(response)
    if not isinstance(data, dict):
        errors.append("booking data must be an object")
        return _result("booking", errors, warnings, agent_ref_id=None)

    errors.extend(_require_fields(data, ["agent_ref_id"], "booking data"))
    agent_ref_id = data.get("agent_ref_id")
    if "agent_ref_id" in data and not _is_nonempty_string(agent_ref_id):
        errors.append("booking data.agent_ref_id must be a non-empty string")
    if not any(key in data for key in ("status", "message")):
        warnings.append("booking response has no status/message field")
    for field in ("status", "message"):
        if field in data and not _is_nonempty_string(data[field]):
            errors.append(f"booking data.{field} must be a non-empty string when present")
    return _result("booking", errors, warnings, agent_ref_id=agent_ref_id)


def detect_kind(response: Any) -> Optional[str]:
    data = response.get("data") if isinstance(response, dict) and "data" in response else response
    if isinstance(data, list):
        return "search"
    if not isinstance(data, dict):
        return None
    signatures: List[str] = []
    if "hotels" in data:
        signatures.append("search")
    if "room_types" in data:
        signatures.append("rates")
    if "hotel" in data:
        signatures.append("detail")
    if "agent_ref_id" in data:
        signatures.append("booking")
    return signatures[0] if len(signatures) == 1 else None


VALIDATORS = {
    "search": validate_search_response,
    "rates": validate_rates_response,
    "detail": validate_detail_response,
    "booking": validate_booking_response,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=["auto", *VALIDATORS])
    parser.add_argument("response_json", help="JSON response string")
    args = parser.parse_args()

    try:
        response = json.loads(args.response_json, parse_constant=_reject_json_constant)
    except (json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"valid": False, "errors": [f"Invalid JSON: {exc}"]}, ensure_ascii=False, indent=2))
        return 2

    if args.kind == "auto" and isinstance(response, dict) and response.get("ok") is False:
        result = _result(
            "api-error",
            [f"API response is not successful: {response.get('error')!r}"],
            [],
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    kind = detect_kind(response) if args.kind == "auto" else args.kind
    if kind is None:
        print(
            json.dumps(
                {"valid": False, "errors": ["Could not detect response kind; pass an explicit kind"]},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2

    result = VALIDATORS[kind](response)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
