# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: fr24/proto/_live_flight_status.proto
# Protobuf Python Version: 5.27.1
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
    1,
    '',
    'fr24/proto/_live_flight_status.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$fr24/proto/_live_flight_status.proto\"@\n\x14LiveFlightStatusData\x12\x0b\n\x03lat\x18\x01 \x01(\x02\x12\x0b\n\x03lon\x18\x02 \x01(\x02\x12\x0e\n\x06squawk\x18\x04 \x01(\r\"3\n\x18LiveFlightsStatusRequest\x12\x17\n\x0f\x66light_ids_list\x18\x01 \x03(\x07\"G\n\x19LiveFlightsStatusResponse\x12*\n\x0b\x66lights_map\x18\x01 \x01(\x0b\x32\x15.LiveFlightStatusDatab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fr24.proto._live_flight_status_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_LIVEFLIGHTSTATUSDATA']._serialized_start=40
  _globals['_LIVEFLIGHTSTATUSDATA']._serialized_end=104
  _globals['_LIVEFLIGHTSSTATUSREQUEST']._serialized_start=106
  _globals['_LIVEFLIGHTSSTATUSREQUEST']._serialized_end=157
  _globals['_LIVEFLIGHTSSTATUSRESPONSE']._serialized_start=159
  _globals['_LIVEFLIGHTSSTATUSRESPONSE']._serialized_end=230
# @@protoc_insertion_point(module_scope)
