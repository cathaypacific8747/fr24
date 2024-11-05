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

protoc --proto_path=src --python_out=src --pyi_out=src $DIR_PROTO/*.proto