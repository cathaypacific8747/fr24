# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: fr24/proto/_top_flights.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'fr24/proto/_top_flights.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1d\x66r24/proto/_top_flights.proto\"\xf7\x01\n\x0e\x46ollowedFlight\x12\x11\n\tflight_id\x18\x01 \x01(\r\x12\x13\n\x0blive_clicks\x18\x02 \x01(\r\x12\x14\n\x0ctotal_clicks\x18\x03 \x01(\r\x12\x15\n\rflight_number\x18\x04 \x01(\t\x12\x10\n\x08\x63\x61llsign\x18\x05 \x01(\t\x12\x0e\n\x06squawk\x18\x06 \x01(\r\x12\x11\n\tfrom_iata\x18\x07 \x01(\t\x12\x11\n\tfrom_city\x18\x08 \x01(\t\x12\x0f\n\x07to_iata\x18\t \x01(\t\x12\x0f\n\x07to_city\x18\n \x01(\t\x12\x0c\n\x04type\x18\x0b \x01(\t\x12\x18\n\x10\x66ull_description\x18\x0c \x01(\t\"\"\n\x11TopFlightsRequest\x12\r\n\x05limit\x18\x01 \x01(\r\">\n\x12TopFlightsResponse\x12(\n\x0fscoreboard_list\x18\x02 \x03(\x0b\x32\x0f.FollowedFlightb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fr24.proto._top_flights_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_FOLLOWEDFLIGHT']._serialized_start=34
  _globals['_FOLLOWEDFLIGHT']._serialized_end=281
  _globals['_TOPFLIGHTSREQUEST']._serialized_start=283
  _globals['_TOPFLIGHTSREQUEST']._serialized_end=317
  _globals['_TOPFLIGHTSRESPONSE']._serialized_start=319
  _globals['_TOPFLIGHTSRESPONSE']._serialized_end=381
# @@protoc_insertion_point(module_scope)
