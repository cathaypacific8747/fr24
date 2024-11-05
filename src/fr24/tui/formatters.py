from __future__ import annotations

import pandas as pd
from fr24.types.common import Airport as AirportJSON
from fr24.types.flight_list import AircraftInfo


class Time:
    def __init__(self, timestamp: None | int | str | pd.Timestamp):
        self.ts = timestamp

    def __format__(self, __format_spec: str) -> str:
        if self.ts is None:
            return ""
        if isinstance(self.ts, int):
            ts = pd.Timestamp(self.ts, unit="s", tz="utc")
        else:
            ts = pd.Timestamp(self.ts, tz="utc")
        return format(ts, __format_spec)


class Airport:
    def __init__(self, airport: AirportJSON | None):
        self.airport = airport

    def __format__(self, __format_spec: str) -> str:
        if self.airport is None:
            return ""
        output = __format_spec
        if code := self.airport.get("code"):
            output = output.replace("%a", code["iata"])
            output = output.replace("%o", code["icao"])
        else:
            return ""
        if name := self.airport.get("name"):
            output.replace("%n", name)
        else:
            output = output.replace("%n", "")
        if position := self.airport.get("position"):
            output = output.replace("%y", position["region"]["city"])
        else:
            output = output.replace("%y", "")
        return output


class Aircraft:
    def __init__(self, aircraft: AircraftInfo):
        self.aircraft = aircraft

    def __format__(self, __format_spec: str) -> str:
        if self.aircraft is None:
            return ""
        registration = self.aircraft["registration"]
        hexcode = self.aircraft["hex"]
        model_text = self.aircraft["model"]["text"]
        return (
            __format_spec.replace("%c", self.aircraft["model"]["code"])
            .replace("%r", registration if registration else "")
            .replace("%x", hexcode if hexcode else "")
            .replace("%p", model_text if model_text else "")
        )
