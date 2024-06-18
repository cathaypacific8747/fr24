from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Annotated, Optional

import rich
import typer
from appdirs import user_cache_dir, user_config_dir

from .core import FR24, FlightListArrow, LiveFeedArrow, PlaybackArrow
from .tui.tui import main as tui_main

app = typer.Typer(no_args_is_help=True)


@app.command()
def dirs() -> None:
    """Shows relevant directories"""
    rich.print(f"Config: {user_config_dir('fr24')}")
    rich.print(f" Cache: {user_cache_dir('fr24')}")


@app.command()
def tui() -> None:
    """Starts the TUI"""

    tui_main()


app_auth = typer.Typer()
app.add_typer(
    app_auth,
    name="auth",
    no_args_is_help=True,
    help="Commands for authentication",
)


@app_auth.command()
def show() -> None:
    """Shows authentication status"""

    async def show_() -> None:
        async with FR24() as fr24:
            await fr24.login()
            if fr24.http.auth is None:
                rich.print(
                    "[bold red]You are not authenticated.[/bold red]\n"
                    "Provide credentials in environment variables: either \n"
                    "- fr24_username + fr24_password or \n"
                    "- fr24_subscription_key + fr24_token\n"
                    "Alternatively, copy the example config file to "
                    f"{Path(user_config_dir('fr24')) / 'fr24.conf'}."
                )
            else:
                rich.print("[bold green]Authenticated[/bold green]")
                rich.print(fr24.http.auth)

    asyncio.run(show_())


def get_success_message(
    service: FlightListArrow | LiveFeedArrow | PlaybackArrow,
) -> str:
    num_rows = service.data.num_rows
    size = service.data.nbytes
    fp = service._fp(service.ctx)  # type: ignore[arg-type]
    return (
        f"[bold green]Success: Saved {num_rows} rows ({size} bytes) "
        f"to {fp}.[/bold green]"
    )


@app.command()
def feed(
    timestamp: Annotated[
        Optional[str],
        typer.Option(
            help=(
                "Time of the snapshot (optional), "
                "a pd.Timestamp-supported input (e.g. 2024-06-04T00:00:00). "
                "Live data will be fetched if not provided."
            )
        ),
    ] = None,
) -> None:
    """Fetches current livefeed / playback of live feed at a given time"""

    async def feed_() -> None:
        async with FR24() as fr24:
            await fr24.login()
            response = await fr24.livefeed.fetch(timestamp)
            datac = response.to_arrow()
            datac.save()
            rich.print(get_success_message(datac))

    asyncio.run(feed_())


@app.command()
def flight_list(
    reg: Annotated[
        Optional[str], typer.Option(help="Aircraft registration (e.g. B-HUJ)")
    ] = None,
    flight: Annotated[
        Optional[str], typer.Option(help="Flight number (e.g. CX8747)")
    ] = None,
    timestamp: Annotated[
        Optional[str],
        typer.Option(
            help=(
                "Show flights with ATD before this time (optional), "
                "a pd.Timestamp-supported input (e.g. 2024-06-04T00:00:00)"
            )
        ),
    ] = "now",
    all: Annotated[
        bool,
        typer.Option(
            "--all", help="Get all pages of flight list", is_flag=True
        ),
    ] = False,
) -> None:
    """Fetches flight list for the given registration or flight number"""

    async def flight_list_() -> None:
        async with FR24() as fr24:
            await fr24.login()
            if all:
                data = fr24.flight_list.load(reg=reg, flight=flight)
                async for response in fr24.flight_list.fetch_all(
                    reg=reg, flight=flight, timestamp=timestamp
                ):
                    data_new = response.to_arrow()
                    data.concat(data_new, inplace=True)
                    data.save()
                rich.print(get_success_message(data))
            else:
                response = await fr24.flight_list.fetch(
                    reg=reg, flight=flight, timestamp=timestamp
                )
                response.to_arrow().save()
                rich.print(get_success_message(response.to_arrow()))

    asyncio.run(flight_list_())


@app.command()
def playback(
    flight_id: Annotated[
        str, typer.Argument(help="Hex Flight ID (e.g. `2d81a27`, `0x2d81a27`)")
    ],
    timestamp: Annotated[
        Optional[str],
        typer.Option(
            help=(
                "ATD (optional), "
                "a pd.Timestamp-supported input (e.g. 2024-06-04T00:00:00)"
            )
        ),
    ] = None,
) -> None:
    """Fetches historical track playback data for the given flight"""

    async def playback_() -> None:
        async with FR24() as fr24:
            await fr24.login()
            response = await fr24.playback.fetch(
                flight_id=flight_id, timestamp=timestamp
            )
            response.to_arrow().save()
            rich.print(get_success_message(response.to_arrow()))

    asyncio.run(playback_())


if __name__ == "__main__":
    app()
