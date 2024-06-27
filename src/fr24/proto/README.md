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

On VSCode, [`settings.json`](../../../.vscode/settings.json) has `formatOnSave` is true. To compile everything at once, open command palette then `proto3: Compile all Protos`.

## Usage

Once compiled, everything should be in the [`v1` namespace](./v1_pb2.pyi).

```py
from fr24.proto.v1_pb2 import LiveFeedRequest

...
```