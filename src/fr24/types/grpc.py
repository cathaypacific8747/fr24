from typing import Literal

LiveFeedFieldAuthenticated = Literal[
    "squawk", "vspeed", "airspace", "logo_id", "age"
]

LiveFeedField = Literal[
    "flight", "reg", "route", "type", LiveFeedFieldAuthenticated
]
