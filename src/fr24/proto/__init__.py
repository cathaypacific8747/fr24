"""
Helper functions for the gRPC protocol.
For more information, see: https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md
"""

from typing import Type, TypeVar
import struct

from google.protobuf.message import Message

T = TypeVar("T", bound=Message)

def encode_message(msg: T) -> bytes:
    msg_bytes = msg.SerializeToString()
    return (
        b"\x00" # u8, no compression
        + struct.pack(">I", len(msg_bytes)) # u64, length of message, big endian
        + msg_bytes # binary octet
    )

# TODO: use Result<T, E> instead
def parse_data(data: bytes, msg_type: Type[T]) -> T:
    assert len(data), "empty DATA frame"
    assert data[0] == 0, "compressed message not implemented" # no compression
    data_len = int.from_bytes(data[1:5], byteorder="big") # length of message
    assert data_len > 0, "empty message"
    data_proto = data[5:5 + data_len]
    # import base64
    # print(data_len, base64.b64encode(data))
    return msg_type.FromString(data_proto)
