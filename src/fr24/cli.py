from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path
from typing import IO, Annotated, Literal, Optional

import click
import rich
import typer
from rich.console import Console

from . import FR24
from .cache import PATH_CACHE
from .configuration import FP_CONFIG_FILE, PATH_CONFIG
from .service import (
    FlightListResult,
    LiveFeedPlaybackResult,
    LiveFeedResult,
    PlaybackResult,
)
from .tui.tui import main as tui_main
from .utils import to_unix_timestamp

app = typer.Typer(no_args_is_help=True)

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)
console_err = Console(stderr=True)


@app.command()
def dirs() -> None:
    """Shows relevant directories"""
    rich.print(f"Config: {PATH_CONFIG}")
    rich.print(f" Cache: {PATH_CACHE}")


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

    ERR_MSG = (
        "[bold yellow]warning[/bold yellow]: not authenticated\n"
        "[bold cyan]help[/bold cyan]: "
        "provide your credentials in environment variables, either:\n"
        "- `fr24_username` and `fr24_password`, or\n"
        "- `fr24_subscription_key` and `fr24_token`\n"
        "[bold cyan]help[/bold cyan]: "
        "alternatively, create a template configuration file "
        f"at `{FP_CONFIG_FILE}` with the command `fr24 auth create`."
    )

    async def show_() -> None:
        async with FR24() as fr24:
            await fr24.login()
            if fr24.http.auth is None:
                console_err.print(ERR_MSG)
            else:
                rich.print("[bold green]success[/bold green]: authenticated")
                rich.print(fr24.http.auth)

    asyncio.run(show_())


@app_auth.command()
def create(
    force: Annotated[
        bool,
        typer.Option(help="Overwrite existing configuration file"),
    ] = False,
) -> None:
    """Create a template config file in the user config directory"""
    import shutil

    if FP_CONFIG_FILE.exists() and FP_CONFIG_FILE.is_file() and not force:
        console_err.print(
            f"[bold red]error[/bold red]: "
            f"{FP_CONFIG_FILE} already exists, use `--force` to overwrite"
        )
        return

    fp_config_template = (
        Path(__file__).parent.parent.parent / "fr24.example.conf"
    )
    FP_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(fp_config_template, FP_CONFIG_FILE)
    rich.print(
        "[bold green]success[/bold green]: "
        f"created template configuration file at {FP_CONFIG_FILE}"
    )


def get_success_message(
    result: FlightListResult
    | PlaybackResult
    | LiveFeedResult
    | LiveFeedPlaybackResult,
    fp: Path | IO[bytes] | None,
    action: Literal["added", "wrote"] = "wrote",
) -> str:
    df = result.to_polars()
    num_rows = df.height
    return (
        "[bold green]success[/bold green]: "
        f"{action} {num_rows} rows to {fp or 'cache'}.\n"
        # FIXME: find a better way to compute the cached filepath
        "Preview:\n"
        f"{df.head()}"
    )


def resolve_path(path: Path | None) -> Path | IO[bytes] | None:
    if path is None:
        return None
    if str(path) == "-":
        return sys.stdout.buffer
    return path.resolve()


def get_console(path: Path | IO[bytes] | None) -> Console:
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
Format = Annotated[
    str,  # literal not yet supported: https://github.com/tiangolo/typer/pull/429
    typer.Option(
        "-f",
        "--format",
        help="Output format, `parquet` or `csv`",
        click_type=click.Choice(["parquet", "csv"]),
    ),
]


# FIXME: since pandas is now gone, we should only accept ISO8601 format
@app.command()
def feed(
    timestamp: Annotated[
        str,
        typer.Option(
            help=(
                "Time of the snapshot (optional), "
                "a pd.Timestamp-supported input (e.g. 2024-06-04T00:00:00). "
                "Live data will be fetched if not provided."
            )
        ),
    ] = "now",
    output: Output = None,
    format: Format = "parquet",
) -> None:
    """Fetches current (or playback of) live feed at a given time"""

    fp = resolve_path(output)
    console = get_console(fp)
    timestamp_int_or_None = (
        to_unix_timestamp(timestamp) if timestamp is not None else None
    )

    async def feed_() -> None:
        async with FR24() as fr24:
            await fr24.login()
            result: LiveFeedResult | LiveFeedPlaybackResult
            if timestamp_int_or_None is None:
                result = await fr24.live_feed.fetch()
            else:
                result = await fr24.live_feed_playback.fetch(
                    timestamp=timestamp_int_or_None
                )
            result.write_table(fp, format=format)  # type: ignore[arg-type]
            console.print(get_success_message(result, fp))

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
        str,
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
    format: Format = "parquet",
) -> None:
    """Fetches flight list for the given registration or flight number"""

    fp = resolve_path(output)
    console = get_console(fp)
    timestamp_int_or_None = (
        to_unix_timestamp(timestamp) if timestamp is not None else None
    )

    async def flight_list_() -> None:
        async with FR24() as fr24:
            await fr24.login()
            if all:
                page = 0
                results = fr24.flight_list.new_result_collection()
                async for result in fr24.flight_list.fetch_all(
                    reg=reg, flight=flight, timestamp=timestamp_int_or_None
                ):
                    results.append(result)
                    results.write_table(fp, format=format)  # type: ignore[arg-type]
                    console.print(
                        get_success_message(result, fp, action="added")
                    )
                    page += 1
            else:
                result = await fr24.flight_list.fetch(
                    reg=reg, flight=flight, timestamp=timestamp_int_or_None
                )
                result.write_table(fp, format=format)  # type: ignore[arg-type]
                console.print(get_success_message(result, fp))

    asyncio.run(flight_list_())


@app.command()
def playback(
    flight_id: Annotated[
        str, typer.Argument(help="Hex Flight ID (e.g. `2d81a27`, `0x2d81a27`)")
    ],
    timestamp: Annotated[
        str,
        typer.Option(
            help=(
                "ATD (optional), "
                "a `chronos` supported input (e.g. 2024-06-04T00:00:00)"
            )
        ),
    ] = "now",
    output: Output = None,
    format: Format = "parquet",
) -> None:
    """Fetches historical track playback data for the given flight"""

    fp = resolve_path(output)
    console = get_console(fp)
    timestamp_int_or_None = (
        to_unix_timestamp(timestamp) if timestamp is not None else None
    )

    async def playback_() -> None:
        async with FR24() as fr24:
            await fr24.login()
            result = await fr24.playback.fetch(
                flight_id=flight_id, timestamp=timestamp_int_or_None
            )
            result.write_table(fp, format=format)  # type: ignore[arg-type]
            console.print(get_success_message(result, fp))

    asyncio.run(playback_())


if __name__ == "__main__":
    app()
