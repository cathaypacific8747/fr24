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

Make sure the [correct version](https://protobuf.dev/support/version-support/#python) of `protoc` is installed.

cd into `./fr24` and run:
```command
protoc --proto_path=src --python_out=src --pyi_out=src src/fr24/proto/*.proto
```

## Usage

Once compiled, all protobuf constructors can be accessed via [`fr24.proto.v1`](./v1_pb2.pyi).

Since the gRPC protocol is remarkably simple, we construct and parse [length-prefixed messages](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md) [manually](./__init__.py).

Requests are made with a common [`httpx.AsyncClient`](https://www.python-httpx.org/api/#asyncclient) shared by JSON and gRPC requests.

## Todo

- [ ] handle streaming responses with multiple `DATA` frames
- [ ] handle grpc-status in HEADERS(flags = `END_STREAM`, `END_HEADERS`)