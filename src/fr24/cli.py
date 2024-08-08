from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Annotated, BinaryIO, Literal, Optional

import rich
import typer
from appdirs import user_cache_dir, user_config_dir
from loguru import logger
from rich.console import Console

from .core import FR24, FlightListArrow, LiveFeedArrow, PlaybackArrow
from .tui.tui import main as tui_main

app = typer.Typer(no_args_is_help=True)
logger.configure(handlers=[{"sink": sys.stderr, "level": "INFO"}])


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
    datac: FlightListArrow | LiveFeedArrow | PlaybackArrow,
    fp: Path | BinaryIO | None,
    action: Literal["added", "wrote"] = "wrote",
) -> str:
    num_rows = datac.data.num_rows
    size = datac.data.nbytes
    fp = fp or datac._fp(datac.ctx)  # type: ignore[arg-type]
    return (
        f"[bold green]Success: {action} {num_rows} rows ({size} bytes) "
        f"to {fp}.[/bold green]\n"
        "Preview:\n"
        f"{datac.df}"
    )


def resolve_path(path: Path | None) -> Path | BinaryIO | None:
    if path is None:
        return None
    if str(path) == "-":
        return sys.stdout.buffer
    return path.resolve()


def get_console(path: Path | BinaryIO | None) -> Console:
    return Console(stderr=path is not None and not isinstance(path, Path))


Output = Annotated[
    Optional[Path],
    typer.Option(
        "-o",
        "--output",
        help=(
            "Save results as parquet to a specific filepath. "
            "If `-`, results will be printed to stdout."
        ),
        exists=False,
        file_okay=True,
        dir_okay=False,
    ),
]
Fmt = Annotated[
    str,  # literal not yet supported: https://github.com/tiangolo/typer/pull/429
    typer.Option(
        "-f",
        "--format",
        help="Output format, `parquet` or `csv`",
    ),
]


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
    output: Output = None,
    fmt: Fmt = "parquet",
) -> None:
    """Fetches current (or playback of) live feed at a given time"""

    fp = resolve_path(output)
    console = get_console(fp)

    async def feed_() -> None:
        async with FR24() as fr24:
            await fr24.login()
            response = await fr24.live_feed.fetch(timestamp)
            datac = response.to_arrow()
            datac.save(fp, fmt)  # type: ignore[arg-type]
            console.print(get_success_message(datac, fp))

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
    output: Output = None,
    fmt: Fmt = "parquet",
) -> None:
    """Fetches flight list for the given registration or flight number"""

    fp = resolve_path(output)
    console = get_console(fp)

    async def flight_list_() -> None:
        async with FR24() as fr24:
            await fr24.login()
            if all:
                page = 0
                datac = fr24.flight_list.load(reg=reg, flight=flight)
                async for response in fr24.flight_list.fetch_all(
                    reg=reg, flight=flight, timestamp=timestamp
                ):
                    data_new = response.to_arrow()
                    datac.concat(data_new, inplace=True)
                    datac.save(fp, fmt)  # type: ignore[arg-type]
                    console.print(
                        get_success_message(data_new, fp, action="added")
                    )
                    page += 1
            else:
                response = await fr24.flight_list.fetch(
                    reg=reg, flight=flight, timestamp=timestamp
                )
                datac = response.to_arrow()
                datac.save(fp, fmt)  # type: ignore[arg-type]
                console.print(get_success_message(response.to_arrow(), fp))

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
    output: Output = None,
    fmt: Fmt = "parquet",
) -> None:
    """Fetches historical track playback data for the given flight"""

    fp = resolve_path(output)
    console = get_console(fp)

    async def playback_() -> None:
        async with FR24() as fr24:
            await fr24.login()
            response = await fr24.playback.fetch(
                flight_id=flight_id, timestamp=timestamp
            )
            datac = response.to_arrow()
            datac.save(fp, fmt)  # type: ignore[arg-type]
            console.print(get_success_message(response.to_arrow(), fp))

    asyncio.run(playback_())


if __name__ == "__main__":
    app()
