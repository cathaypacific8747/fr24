"""
Helper functions for the gRPC+protobuf protocol.
For more information, see: https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md
"""
from __future__ import annotations
from typing import Type, TypeVar
import struct

from google.protobuf.message import Message
from ..utils import SupportsToProto

T = TypeVar("T", bound=Message)

# similar to impl Into<Proto>
def to_proto(message_like: SupportsToProto[T] | T) -> T:
    return (
        message_like.to_proto()
        if isinstance(message_like, SupportsToProto)
        else message_like
    )


def encode_message(msg: T) -> bytes:
    msg_bytes = msg.SerializeToString()
    return (
        b"\x00" # u8, no compression
        + struct.pack(">I", len(msg_bytes)) # u64, length of message, big endian
        + msg_bytes # binary octet
    )

# TODO: use Result<T, E> instead
def parse_data(data: bytes, msg_type: Type[T]) -> T:
    """Decode a DATA frame into a protobuf message."""
    assert len(data), "empty DATA frame"
    assert data[0] != 1, "compressed message not implemented" # no compression
    assert data[0] == 0, f"received unknown message: {data!r}"
    data_len = int.from_bytes(data[1:5], byteorder="big") # length of message
    assert data_len > 0, "empty message"
    data_proto = data[5:5 + data_len]
    return msg_type.FromString(data_proto)

