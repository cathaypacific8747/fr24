#!/bin/bash

PROTOC_VERSION=$(protoc --version)
PROTOC_VERSION_EXPECTED="libprotoc 28.2"

if [ "$PROTOC_VERSION" != "$PROTOC_VERSION_EXPECTED" ]; then
    echo "error: protoc version must be $PROTOC_VERSION_EXPECTED"
    exit 1
fi

DIR_PROTO="src/fr24/proto"

if [ ! -d "$DIR_PROTO" ]; then
    echo "error: cannot find `$DIR_PROTO`"
    echo "help: are you in the root directory?"
    exit 1
fi

DIR_MYPY_PROTOBUF=".venv/bin/protoc-gen-mypy"

# NOTE: because protobuf does not support relative imports (https://github.com/protocolbuffers/protobuf/issues/1491)
# we are forcing the exported package to be `fr24.proto.*`
# workaround: https://grpc.io/docs/languages/python/basics/#generating-grpc-interfaces-with-custom-package-path
protoc --plugin=$DIR_MYPY_PROTOBUF -Ifr24/proto=$DIR_PROTO --python_out=src --mypy_out=readable_stubs:src $DIR_PROTO/*.proto