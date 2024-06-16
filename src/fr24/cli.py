from __future__ import annotations

import asyncio

# from datetime import datetime
from pathlib import Path

# from typing import Annotated, Optional
import rich
import typer
from appdirs import user_cache_dir, user_config_dir

from .core import FR24  # , FlightListService, LiveFeedService, PlaybackService
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


# def get_success_message(
#     service: FlightListService | LiveFeedService | PlaybackService,
# ) -> str:
#     num_rows = t.num_rows if (t := service.data.table) is not None else 0
#     size = service.data._get_fp.stat().st_size
#     return (
#         f"[bold green]Success: Saved {num_rows} rows ({size} bytes) "
#         f"to {service.data._get_fp}.[/bold green]"
#     )


# @app.command()
# def feed(
#     timestamp: Annotated[
#         Optional[int], typer.Option(help="Start unix timestamp (s, UTC)")
#     ] = None,
#     time: Annotated[
#         Optional[datetime], typer.Option(help="Start datetime (UTC)")
#     ] = None,
# ) -> None:
#     """Fetches current livefeed / playback of live feed at a given time"""
#     if time is not None and timestamp is not None:
#         raise typer.BadParameter("Only one of time and timestamp can be set")
#     if time is not None:
#         timestamp = int(time.timestamp())

#     async def feed_() -> None:
#         async with FR24() as fr24:
#             await fr24.http._login()

#             lf = fr24.livefeed(timestamp)
#             lf.data._add_api_response(await lf.api._fetch())
#             lf.data._save_parquet()
#             rich.print(get_success_message(lf))

#     asyncio.run(feed_())


if __name__ == "__main__":
    app()
