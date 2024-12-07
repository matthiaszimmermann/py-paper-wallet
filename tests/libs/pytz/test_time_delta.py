from datetime import datetime, timedelta  # noqa: INP001

import pytz
from pytz import timezone


def test_flight_time() -> None:
    """Tests times and related properties for a flight from Zurich to Bankok."""
    # Time zones
    tz_zurich = timezone("Europe/Zurich")
    tz_bangkok = timezone("Asia/Bangkok")

    # Set a date in winter to avoid DST issues
    departure_date = datetime(  # noqa: DTZ001
        2024, 1, 15, 17, 30
    )  # Jan 15, 2024, 13:30 local Zurich time
    arrival_date = datetime(  # noqa: DTZ001
        2024, 1, 16, 10, 30
    )  # Jan 16, 2024, 10:30 local Bangkok time

    # Expectations
    expected_flight_hours = 11.0
    expected_tz_depature = timedelta(hours=1)
    expected_tz_arrival = timedelta(hours=7)
    expected_tz_difference = expected_tz_arrival - expected_tz_depature

    # Localize the naive datetimes to their respective time zones
    departure_local = tz_zurich.localize(departure_date)
    arrival_local = tz_bangkok.localize(arrival_date)

    # Convert both times to UTC for comparison
    departure_utc = departure_local.astimezone(pytz.UTC)
    arrival_utc = arrival_local.astimezone(pytz.UTC)

    # Check UTC times
    assert departure_utc

    # 1. Check the expected time zone difference
    # At chosen date, Zurich should be UTC+1 and Bangkok UTC+7, a 6-hour difference.
    # Verify by comparing UTC offsets:
    zurich_offset = departure_local.utcoffset()
    bangkok_offset = arrival_local.utcoffset()

    # Both offsets should not be None
    assert zurich_offset is not None
    assert bangkok_offset is not None

    # Check time zone offsets
    assert zurich_offset == expected_tz_depature
    assert bangkok_offset == expected_tz_arrival

    # Calculate offset difference in hours
    tz_diff_hours = bangkok_offset - zurich_offset
    assert (
        tz_diff_hours == expected_tz_difference
    ), f"Unexpected TZ difference, exected {expected_tz_difference} got {tz_diff_hours}"

    # 2. Check the expected flight time
    # Calculate actual flight duration
    flight_duration = arrival_utc - departure_utc
    flight_hours = flight_duration.total_seconds() / 3600.0
    assert (
        abs(flight_hours - expected_flight_hours) < 0.0001
    ), f"Expected flight time ~{expected_flight_hours}h, got {flight_hours:.2f}h"

    # 3. Check that the arrival time equals departure time + flight duration
    # Add the expected flight time to the departure time and compare to arrival time
    recalculated_arrival = departure_utc + timedelta(hours=expected_flight_hours)
    # Since we're comparing datetimes, let's ensure they're equal
    assert recalculated_arrival == arrival_utc, (
        f"Arrival time does not match departure + flight time. "
        f"Expected {recalculated_arrival}, got {arrival_utc}"
    )
