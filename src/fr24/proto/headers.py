from __future__ import annotations

import secrets
from ..utils import DEFAULT_HEADERS

from ..types.authentication import Authentication

PLATFORM_VERSION = "25.062.1136"
# see ./README.md.


DEFAULT_HEADERS_GRPC = {
    **DEFAULT_HEADERS,
    "Accept": "*/*",
    "fr24-device-id": "web-000000000-000000000000000000000", # fingerprint
    "fr24-platform": f"web-{PLATFORM_VERSION}",
    "x-envoy-retry-grpc-on": "unavailable",
    "Content-Type": "application/grpc-web+proto",
    "X-User-Agent": "grpc-web-javascript/0.1",
    "X-Grpc-Web": "1",
    "DNT": "1",
}

def get_headers(auth: Authentication | None, *, device_id: None | str = None) -> dict[str, str]:
    headers = DEFAULT_HEADERS_GRPC.copy()
    if device_id is None:
        device_id = f"web-{secrets.token_urlsafe(32)}"
    # TODO: we need to add fr24-platform as well: YY.DDD.HHMM
    headers["fr24-device-id"] = device_id
    if auth is not None and auth["userData"]["accessToken"] is not None:
        headers["authorization"] = f"Bearer {auth['userData']['accessToken']}"
    return DEFAULT_HEADERS_GRPC.copy()
