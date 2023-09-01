import urllib3
import time
import secrets
import base64
from loguru import logger

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

def analyse(filename: str):
    with open(f'log/{filename}', 'rb') as f:
        data = f.read()
        data = base64.b64encode(data)
        print(data)

if __name__ == '__main__':
    # scrape()
    analyse(f"1693476179790_raw.txt")