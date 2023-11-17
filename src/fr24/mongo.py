from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import TypedDict

import sshtunnel
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

import pandas as pd

from .proto.request_pb2 import LiveFeedResponse


class AircraftType(TypedDict):
    icao24: str
    registration: str
    typecode: str
    callsign: str
    fr24id: str
    ts: int
    latitude: float
    longitude: float
    altitude: float


class Mongo:
    localhost: str = "127.0.0.1"
    local_port: int = 27017
    remote_port: int = 27017
    ssh_server: str
    ssh_port: int = 22
    ssh_username: None | str = None
    ssh_password: None | str = None

    def __init__(
        self,
        handle: None | str = None,
        *,
        ssh_server: None | str = None,
        local_port: None | int = None,
        remote_port: None | int = None,
        ssh_username: None | str = None,
        ssh_password: None | str = None,
        ssh_port: int = 22,
    ) -> None:
        self.local_port = (
            local_port if local_port is not None else self.local_port
        )
        self.remote_port = (
            remote_port if remote_port is not None else self.remote_port
        )
        self.ssh_username = (
            ssh_username if ssh_username is not None else self.ssh_username
        )
        self.ssh_password = (
            ssh_password if ssh_password is not None else self.ssh_password
        )
        self.ssh_server = (
            ssh_server if ssh_server is not None else self.ssh_server
        )
        self.ssh_port = ssh_port if ssh_port is not None else self.ssh_port

    @asynccontextmanager
    async def async_client(self, force: bool = False) -> AsyncIOMotorClient:
        with sshtunnel.open_tunnel(
            (self.ssh_server, self.ssh_port),
            ssh_username=self.ssh_username,
            ssh_password=self.ssh_password,
            remote_bind_address=("127.0.0.1", self.remote_port),
            local_bind_address=(self.localhost, self.local_port),
        ) as _tunnel:
            client = AsyncIOMotorClient(
                f"mongodb://{self.localhost}:{self.local_port}"
            )
            yield client


async def lookup_registration(
    collection: AsyncIOMotorCollection,
    registration: str | list,
) -> pd.DataFrame:
    registration = (
        registration if isinstance(registration, str) else {"$in": registration}
    )
    query = collection.find(
        {"registration": registration},
        {
            "icao24": 1,
            "registration": 1,
            "typecode": 1,
            "serial": 1,
            "owner": 1,
            "operator": 1,
            "type": 1,
            "age": 1,
            "_id": 0,
        },
    )

    return pd.json_normalize([res async for res in query])


async def update_aircraft(
    collection: AsyncIOMotorCollection,
    flightdata: LiveFeedResponse.FlightData,
) -> AircraftType:
    ac: AircraftType = {
        "icao24": f"{flightdata.extra_info.icao_address:x}",
        "registration": flightdata.extra_info.reg,
        "typecode": flightdata.extra_info.type,
        "callsign": flightdata.callsign,
        "fr24id": flightdata.flightid,
        "ts": flightdata.timestamp,
        "latitude": flightdata.latitude,
        "longitude": flightdata.longitude,
        "altitude": flightdata.altitude,
    }

    if ac["registration"] == "00000000":
        return {}

    if ac["icao24"] == "0":
        return {}

    ac_old = await collection.find_one({"icao24": ac["icao24"]})
    if ac_old is not None:
        if ac["callsign"] == "":  # safeguard
            del ac["callsign"]

        if ac["registration"] == "":  # safeguard
            del ac["registration"]
            del ac["typecode"]

        elif ac["registration"] != ac_old["registration"]:
            await collection.update_one(
                {"icao24": ac["icao24"]}, {"$set": ac}, upsert=True
            )
            await collection.update_one(
                {"icao24": ac["icao24"]},
                {
                    "$unset": {
                        "operator": 1,
                        "owner": 1,
                        "type": 1,
                        "serial": 1,
                        "age": 1,
                    }
                },
            )
            logging.warning(f"** REGISTRATION CHANGE ** {ac}")
            return ac

    logging.warning(f"** NEW AIRCRAFT ** {ac}")
    await collection.update_one(
        {"icao24": ac["icao24"]}, {"$set": ac}, upsert=True
    )
    return ac


def aircraft_db(ssh_server: str = "eyjafjallajokull"):
    columns = [
        "icao24",
        "registration",
        "typecode",
        "serial",
        "owner",
        "operator",
        "type",
        "age",
    ]

    async def get_database():
        with Mongo(ssh_server=ssh_server).async_client() as client:
            query = client.adb.aircraft.find(
                {},
                {
                    "icao24": 1,
                    "registration": 1,
                    "typecode": 1,
                    "serial": 1,
                    "owner": 1,
                    "operator": 1,
                    "type": 1,
                    "age": 1,
                    "_id": 0,
                },
            )

            return pd.json_normalize([res async for res in query])

    res = asyncio.run(get_database())
    filename = "aircraft_db.csv.gz"
    res[columns].sort_values("icao24").to_csv(filename, index=0)
    print(f"{filename} written")
