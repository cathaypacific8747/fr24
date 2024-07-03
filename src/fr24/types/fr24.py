from typing import Literal

LiveFeedFieldAuthenticated = Literal[
    "squawk", "vspeed", "airspace", "logo_id", "age"
]

LivefeedField = Literal[
    "flight", "reg", "route", "type", LiveFeedFieldAuthenticated
]
