import urllib3
import httpx
import time
import secrets
import asyncio
from loguru import logger
import rich
import struct
from proto.request_pb2 import (
    LiveFeedRequest, Bounds, Settings, TrafficType,
    LiveFeedResponse
)
from google.protobuf.json_format import MessageToDict
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.csv as csv

DEFAULT_REQUEST = LiveFeedRequest(
    bounds=Bounds(
        north=28.12,
        south=12.89,
        west=96.04,
        east=129.82
    ),
    settings=Settings(
        sources_list=list(range(10)),
        services_list=list(range(12)),
        traffic_type=TrafficType.ALL,
    ),
    stats=False,
    limit=1500,
    maxage=14400,
    # selected_flightid=0x31da4a31,
)
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'fr24-device-id': "web-00000000000000000000000000000000",
    'x-envoy-retry-grpc-on': 'unavailable',
    'Content-Type': 'application/grpc-web+proto',
    'X-User-Agent': 'grpc-web-javascript/0.1',
    'X-Grpc-Web': '1',
    'Origin': 'https://www.flightradar24.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.flightradar24.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'TE': 'trailers'
}
FLIGHTINFO_SCHEMA = pa.schema([
    pa.field("flightid", pa.uint64()),
    pa.field("latitude", pa.float32()),
    pa.field("longitude", pa.float32()),
    pa.field("heading", pa.uint16()),
    pa.field("altitude", pa.int32()),
    pa.field("ground_speed", pa.int16()),
    pa.field("timestamp", pa.uint32()),
    pa.field("on_ground", pa.bool_()),
    pa.field("callsign", pa.string()),
    pa.field("source", pa.uint8()),
])
BOUNDS = [
    (-180, -117),
    (-117, -110),
    (-110, -100),
    (-100, -95),
    (-95, -90),
    (-90, -85),
    (-85, -82),
    (-82, -79),
    (-79, -75),
    (-75, -68),
    (-68, -30),
    (-30, -2),
    (-2, 5),
    (5, 10),
    (10, 20),
    (20, 40),
    (40, 60),
    (60, 100),
    (100, 110),
    (110, 120),
    (120, 180),
]

def download(device_id: str = None):
    if not device_id:
        device_id = f"web-{secrets.token_urlsafe(32)}"

    url = 'https://data-feed.flightradar24.com/fr24.feed.api.v1.Feed/LiveFeed'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'fr24-device-id': device_id,
        'x-envoy-retry-grpc-on': 'unavailable',
        'Content-Type': 'application/grpc-web+proto',
        'X-User-Agent': 'grpc-web-javascript/0.1',
        'X-Grpc-Web': '1',
        'Origin': 'https://www.flightradar24.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.flightradar24.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'TE': 'trailers'
    }

    data = b'\x00\x00\x00\x00>\n\x14\r\x1f\x85\xbfA\x15\xecQ\xaaA\x1d\x14\xae\xdbB%\xb8\x9e\xecB\x12\x1c\n\n\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x12\x0c\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\n\x0b\x18\x030\x018\xdc\x0b@\xc0pR\x00'

    http = urllib3.PoolManager()
    response = http.request('POST', url, headers=headers, body=data)
    with open(f'log/{time.time()*1000:.0f}_raw.txt', 'wb') as f:
        f.write(response.data)
    
    logger.info(f"Downloaded {len(response.data)} bytes")

def scrape():
    while True:
        download()
        time.sleep(5)


def generate_post_data(west, east):
    request = LiveFeedRequest()
    request.CopyFrom(DEFAULT_REQUEST)
    request.bounds.CopyFrom(Bounds(
        north=90,
        south=-90,
        west=west,
        east=east
    ))
    request_s = request.SerializeToString()
    post_data = b"\x00" + struct.pack("!I", len(request_s)) + request_s
    return post_data

def construct_requests(we_bounds: list[tuple[int, int]]):
    requests = []
    for west, east in we_bounds:
        data = generate_post_data(west, east)
        headers = DEFAULT_HEADERS.copy()
        headers['fr24-device-id'] = f"web-{secrets.token_urlsafe(32)}"
        requests.append(httpx.Request(
            "POST",
            "https://data-feed.flightradar24.com/fr24.feed.api.v1.Feed/LiveFeed",
            headers=headers,
            data=data
        ))
    return requests

def handle_response(data: bytes, i=0) -> LiveFeedResponse:
    # print(data[:500])
    # print(base64.b64encode(data).decode("utf-8"))
    assert len(data) and data[0] == 0
    data_len = int.from_bytes(data[1:5])
    # print("len", data[1:5], data_len)
    lfr = LiveFeedResponse()
    lfr.ParseFromString(data[5:5+data_len])
    return lfr, i

async def do_request(client: httpx.AsyncClient, request: httpx.Request, i=0):
    response = await client.send(request)
    return handle_response(response.content, i)

async def main():
    requests = construct_requests(we_bounds=BOUNDS)
    async with httpx.AsyncClient() as client:
        data = await asyncio.gather(*[do_request(client, request, i) for i, request in enumerate(requests)])
        all_flights = []
        for d, i in data:
            d2 = MessageToDict(d, including_default_value_fields=True, use_integers_for_enums=True, preserving_proto_field_name=True)
            all_flights.extend(d2["flights_list"])
            logger.debug(f"{BOUNDS[i]}: {len(d2['flights_list'])} flights")
        tbl = pa.Table.from_pylist(all_flights, schema=FLIGHTINFO_SCHEMA)
        pq.write_table(tbl, "test.parquet")

# def req():
#     data = generate_post_data(100, 110)
#     print(data)

#     url = 'https://data-feed.flightradar24.com/fr24.feed.api.v1.Feed/LiveFeed'
#     headers = DEFAULT_HEADERS.copy()
#     headers['fr24-device-id'] = f"web-{secrets.token_urlsafe(32)}"

#     http = urllib3.PoolManager()
#     response = http.request('POST', url, headers=headers, body=data)
#     handle_response(response.data)

if __name__ == '__main__':
    # scrape()
    # analyse(f"1693476179790_raw.txt")
    
    # req()
    # run main
    asyncio.run(main())