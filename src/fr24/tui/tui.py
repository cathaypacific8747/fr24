from __future__ import annotations

import httpx
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import ScrollableContainer
from textual.widgets import DataTable, Footer, Header, Input, Label, Static

import pandas as pd
from fr24.authentication import login
from fr24.history import airport_list, flight_list
from fr24.json_types import Airport as AirportJSON
from fr24.json_types import (
    AirportList,
    Authentication,
    FlightList,
    FlightListAircraftData,
    FlightListItem,
)

# -- Formatters --


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
    def __init__(self, airport: AirportJSON):
        self.airport = airport

    def __format__(self, __format_spec: str) -> str:
        if self.airport is None:
            return ""
        output = __format_spec
        if code := self.airport.get("code"):
            output = output.replace("%a", code["iata"])
            output = output.replace("%o", code["icao"])
        else:
            output = output.replace("%a", "")
            output = output.replace("%o", "")
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
    def __init__(self, aircraft: FlightListAircraftData):
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


# -- Widgets --


class SearchBlock(Static):
    def compose(self) -> ComposeResult:
        yield SearchButton(id="date")
        yield SearchButton(id="aircraft")
        yield SearchButton(id="flight number")
        yield SearchButton(id="origin")
        yield SearchButton(id="destination")


class SearchButton(Static):
    def compose(self) -> ComposeResult:
        assert self.id is not None
        yield Label(self.id)
        yield Input(id=self.id)

    def on_mount(self) -> None:
        input = self.query(Input).first()
        if input.id == "date":
            input.value = f"{pd.Timestamp('now'):%d %b %y}"
        if input.id == "flight number":
            input.focus()

    def on_input_changed(self, message: Input.Changed) -> None:
        if message.input.id == "aircraft":
            for input in self.app.query(Input):
                if input.id in ["flight number", "origin", "destination"]:
                    input.value = ""
        if message.input.id == "flight number":
            for input in self.app.query(Input):
                if input.id in ["aircraft", "origin", "destination"]:
                    input.value = ""

    async def on_input_submitted(self, message: Input.Submitted) -> None:
        ts_widget = next(
            input for input in self.app.query(Input) if input.id == "date"
        )
        ts = pd.Timestamp(
            ts_widget.value if ts_widget.value != "" else "now",
            tz="utc",
        )

        if message.value:
            if message.input.id == "aircraft":
                await self.app.lookup_aircraft(message.value, ts=ts)  # type: ignore
            if message.input.id == "flight number":
                await self.app.lookup_number(message.value, ts=ts)  # type: ignore
            if message.input.id == "origin":
                await self.app.lookup_departure(message.value, ts=ts)  # type: ignore
            if message.input.id == "destination":
                await self.app.lookup_arrival(message.value, ts=ts)  # type: ignore


# -- Application --


class FR24(App[None]):
    CSS_PATH = "style.tcss"
    BINDINGS = [  # noqa: RUF012
        ("q", "quit", "Quit"),
        ("l", "login", "Log in"),
        ("r", "refresh", "Refresh"),  # TODO
        ("s", "search", "Search"),
        Binding("escape", "escape", show=False),
    ]

    def compose(self) -> ComposeResult:
        self.auth: Authentication | None = None
        self.client = httpx.AsyncClient()
        self.search_visible = True
        yield Header()
        yield Footer()
        yield SearchBlock()
        yield ScrollableContainer(DataTable())

    def on_mount(self) -> None:
        self.title = "FlightRadar24"
        table = self.query_one(DataTable)
        table.add_columns(
            "date",
            "number",
            "callsign",
            "aircraft",
            "from",
            "to",
            "STD",
            "ATD",
            "STA",
            "status",
            "flightid",
        )

    def action_search(self) -> None:
        self.search_visible = not self.search_visible
        if self.search_visible:
            self.query_one(SearchBlock).remove_class("hidden")
        else:
            self.query_one(SearchBlock).add_class("hidden")
            self.query_one(DataTable).focus()

    async def action_escape(self) -> None:
        if not self.search_visible:
            await self.action_quit()

        self.search_visible = False
        self.query_one(SearchBlock).add_class("hidden")
        self.query_one(DataTable).focus()

    async def action_login(self) -> None:
        self.auth = await login(self.client)
        if self.auth is not None:
            self.sub_title = "authenticated"
            self.query_one(Header).add_class("authenticated")
            self.query_one(Footer).add_class("authenticated")

    async def lookup_aircraft(self, value: str, ts: str) -> None:
        results: FlightList = await flight_list(
            self.client, reg=value, limit=100, timestamp=ts, auth=self.auth
        )
        self.update_table(results["result"]["response"].get("data", None))

    async def lookup_number(self, value: str, ts: str) -> None:
        results: FlightList = await flight_list(
            self.client, flight=value, limit=100, timestamp=ts, auth=self.auth
        )
        self.update_table(results["result"]["response"].get("data", None))

    async def lookup_arrival(self, value: str, ts: str) -> None:
        results: AirportList = await airport_list(
            self.client,
            airport=value,
            mode="arrivals",
            limit=100,
            timestamp=ts,
            auth=self.auth,
        )
        s = results["result"]["response"]["airport"]["pluginData"]["schedule"]
        self.update_table(
            [  # TODO add airport info from
                elt["flight"]  # type: ignore
                for elt in s["arrivals"].get("data", [])
            ]
        )

    async def lookup_departure(self, value: str, ts: str) -> None:
        results: AirportList = await airport_list(
            self.client,
            airport=value,
            mode="departures",
            limit=100,
            timestamp=ts,
            auth=self.auth,
        )
        s = results["result"]["response"]["airport"]["pluginData"]["schedule"]
        self.update_table(
            [  # TODO add airport info from
                elt["flight"]  # type: ignore
                for elt in s["departures"].get("data", [])
            ]
        )

    def update_table(self, data: None | list[FlightListItem]) -> None:
        table = self.query_one(DataTable)
        table.clear()
        if data is None:
            return
        table.add_rows(
            [
                (
                    f'{Time(entry["time"]["scheduled"]["departure"]):%d %b %y}',
                    entry["identification"]["number"]["default"],
                    entry["identification"]["callsign"],
                    f'{Aircraft(entry["aircraft"]):%r (%c)}',
                    f'{Airport(entry["airport"]["origin"]):%y (%o)}',
                    f'{Airport(entry["airport"]["destination"]):%y (%o)}',
                    f'{Time(entry["time"]["scheduled"]["departure"]):%H:%MZ}',
                    f'{Time(entry["time"]["real"]["departure"]):%H:%MZ}',
                    f'{Time(entry["time"]["scheduled"]["arrival"]):%H:%MZ}',
                    entry["status"]["text"],
                    entry["identification"]["id"],
                )
                for entry in data
            ]
        )


def main() -> None:
    app = FR24()
    app.run()


if __name__ == "__main__":
    main()
