# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: fr24/proto/_historic_trail.proto
# Protobuf Python Version: 5.28.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    2,
    '',
    'fr24/proto/_historic_trail.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from fr24.proto import _common_pb2 as fr24_dot_proto_dot___common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n fr24/proto/_historic_trail.proto\x1a\x18\x66r24/proto/_common.proto\")\n\x14HistoricTrailRequest\x12\x11\n\tflight_id\x18\x01 \x01(\x07\"P\n\x15HistoricTrailResponse\x12\x37\n\x12radar_records_list\x18\x01 \x03(\x0b\x32\x1b._common.RadarHistoryRecordb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fr24.proto._historic_trail_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_HISTORICTRAILREQUEST']._serialized_start=62
  _globals['_HISTORICTRAILREQUEST']._serialized_end=103
  _globals['_HISTORICTRAILRESPONSE']._serialized_start=105
  _globals['_HISTORICTRAILRESPONSE']._serialized_end=185
# @@protoc_insertion_point(module_scope)
