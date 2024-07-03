# Protobuf definitions

fr24 is slowly migrating from JSON to gRPC. This directory contains protobuf definitions derived from the JS `grpc-web` source.

The official structure stores everything under `proto.fr24.feed.api.v1.*`.

We aim to adhere to the official structure and naming as far as possible. Although the current structure is split into multiple files for convenience, they are ultimately re-exported to the same [public `v1` namespace](./v1.proto).

## Development

- the `optional` keyword does not mean it's nullable, but for [presence tracking](https://protobuf.dev/programming-guides/field_presence/) which forces the field to be explicitly sent
- when type is ambiguous, mark as `?`
- when there are updates to messages, enums or fields, comment with the client version `// NEW: XX.YYY.ZZZZ`
    - `XX`: year
    - `YYY`: julian date
    - `ZZZZ`: time
    - omit commit version.

## Compilation

cd into `./fr24` and run:
```command
protoc --proto_path=src --python_out=src --pyi_out=src src/fr24/proto/*.proto
protoc --proto_path=src --grpclib_python_out=src src/fr24/proto/v1.proto
```

## Usage

Once compiled, all protobuf constructors can be accessed via [`fr24.proto.v1`](./v1_pb2.pyi).

gRPC calls involve [length-prefixed messages](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md). Right now, we make POST requests manually:

```py
from fr24.proto.v1_pb2 import SomeMessage

message = SomeMessage(...).SerializeToString()
request = httpx.Request(
    "POST",
    "https://data-feed.flightradar24.com/{service_name}/{method_name}",
    content=(
        b"\x00" + # u8, no compression
        struct.pack("!I", len(message)) + # u64, length of message, big endian
        message # binary octet
    )
)
```

For the response, we do:
```py
response = await client.send(request)
data = response.content
assert len(data) and data[0] == 0 # no compression
data_len = int.from_bytes(data[1:5], byteorder="big") # length of message
return data[5 : 5 + data_len]
```

Future releases will move to [grpclib](https://github.com/vmagamedov/grpclib) for proper handling of `grpc-status` and streaming responses.