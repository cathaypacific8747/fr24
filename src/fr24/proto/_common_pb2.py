# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: fr24/proto/_common.proto
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
    'fr24/proto/_common.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18\x66r24/proto/_common.proto\x12\x07_common\"\xca\x01\n\x07\x45MSInfo\x12\x0b\n\x03qnh\x18\x01 \x01(\x05\x12\x0c\n\x04\x61mcp\x18\x02 \x01(\x05\x12\x0c\n\x04\x61\x66ms\x18\x03 \x01(\x05\x12\x0b\n\x03oat\x18\x04 \x01(\x05\x12\x0b\n\x03ias\x18\x05 \x01(\x05\x12\x0b\n\x03tas\x18\x06 \x01(\x05\x12\x0c\n\x04mach\x18\x07 \x01(\x05\x12\x0c\n\x04\x61gps\x18\x08 \x01(\x05\x12\x10\n\x08\x61gpsdiff\x18\t \x01(\x05\x12\x0f\n\x07\x61pflags\x18\n \x01(\x05\x12\x10\n\x08wind_dir\x18\x0b \x01(\x05\x12\x12\n\nwind_speed\x18\x0c \x01(\x05\x12\n\n\x02rs\x18\r \x01(\x05\"\xfb\x02\n\x0f\x45MSAvailability\x12\x18\n\x10qnh_availability\x18\x01 \x01(\x08\x12\x19\n\x11\x61mcp_availability\x18\x02 \x01(\x08\x12\x19\n\x11\x61\x66ms_availability\x18\x03 \x01(\x08\x12\x18\n\x10oat_availability\x18\x04 \x01(\x08\x12\x18\n\x10ias_availability\x18\x05 \x01(\x08\x12\x18\n\x10tas_availability\x18\x06 \x01(\x08\x12\x19\n\x11mach_availability\x18\x07 \x01(\x08\x12\x19\n\x11\x61gps_availability\x18\x08 \x01(\x08\x12\x1d\n\x15\x61gpsdiff_availability\x18\t \x01(\x08\x12\x1c\n\x14\x61pflags_availability\x18\n \x01(\x08\x12\x1d\n\x15wind_dir_availability\x18\x0b \x01(\x08\x12\x1f\n\x17wind_speed_availability\x18\x0c \x01(\x08\x12\x17\n\x0frs_availability\x18\r \x01(\x08\"X\n\x08Schedule\x12\x0b\n\x03std\x18\x01 \x01(\x05\x12\x0b\n\x03\x65td\x18\x02 \x01(\x05\x12\x0b\n\x03\x61td\x18\x03 \x01(\x05\x12\x0b\n\x03sta\x18\x04 \x01(\x05\x12\x0b\n\x03\x65ta\x18\x05 \x01(\x05\x12\x0b\n\x03\x61ta\x18\x06 \x01(\x05\"6\n\x05Route\x12\x0c\n\x04\x66rom\x18\x01 \x01(\t\x12\n\n\x02to\x18\x02 \x01(\t\x12\x13\n\x0b\x64iverted_to\x18\x03 \x01(\t\"\xdc\x03\n\x0f\x45xtraFlightInfo\x12\x0e\n\x06\x66light\x18\x01 \x01(\t\x12\x0b\n\x03reg\x18\x02 \x01(\t\x12\x1d\n\x05route\x18\x03 \x01(\x0b\x32\x0e._common.Route\x12\x0c\n\x04type\x18\x04 \x01(\t\x12\x0e\n\x06squawk\x18\x05 \x01(\x05\x12\x0e\n\x06vspeed\x18\x06 \x01(\x05\x12\x0b\n\x03\x61ge\x18\x07 \x01(\t\x12\x16\n\x0e\x63ountry_of_reg\x18\x08 \x01(\x05\x12#\n\x08schedule\x18\t \x01(\x0b\x32\x11._common.Schedule\x12\x0f\n\x07logo_id\x18\n \x01(\x05\x12\x10\n\x08\x61irspace\x18\x0b \x01(\x05\x12\"\n\x08\x65ms_info\x18\x0c \x01(\x0b\x32\x10._common.EMSInfo\x12\x32\n\x10\x65ms_availability\x18\r \x01(\x0b\x32\x18._common.EMSAvailability\x12\x14\n\x0cicao_address\x18\x0e \x01(\r\x12\x16\n\x0eoperated_by_id\x18\x0f \x01(\r\x12\x1b\n\x13squawk_availability\x18\x10 \x01(\x08\x12\x1b\n\x13vspeed_availability\x18\x11 \x01(\x08\x12\x1d\n\x15\x61irspace_availability\x18\x12 \x01(\x08\x12\x13\n\x0b\x61irspace_id\x18\x13 \x01(\t\"A\n\x0bSourceStats\x12#\n\x06source\x18\x01 \x01(\x0e\x32\x13._common.DataSource\x12\r\n\x05\x63ount\x18\x02 \x01(\r\".\n\x05Stats\x12%\n\x07sources\x18\x01 \x03(\x0b\x32\x14._common.SourceStats\"\xa8\x02\n\x06\x46light\x12\x10\n\x08\x66lightid\x18\x01 \x01(\x05\x12\x0b\n\x03lat\x18\x02 \x01(\x02\x12\x0b\n\x03lon\x18\x03 \x01(\x02\x12\r\n\x05track\x18\x04 \x01(\x05\x12\x0b\n\x03\x61lt\x18\x05 \x01(\x05\x12\r\n\x05speed\x18\x06 \x01(\x05\x12\x1b\n\x04icon\x18\x07 \x01(\x0e\x32\r._common.Icon\x12\x1f\n\x06status\x18\x08 \x01(\x0e\x32\x0f._common.Status\x12\x11\n\ttimestamp\x18\t \x01(\x05\x12\x11\n\ton_ground\x18\n \x01(\x08\x12\x10\n\x08\x63\x61llsign\x18\x0b \x01(\t\x12#\n\x06source\x18\x0c \x01(\x0e\x32\x13._common.DataSource\x12,\n\nextra_info\x18\r \x01(\x0b\x32\x18._common.ExtraFlightInfo\"\x19\n\x08\x44uration\x12\r\n\x05\x63ount\x18\x01 \x01(\r\"\x15\n\x04Tick\x12\r\n\x05\x63ount\x18\x01 \x01(\r*R\n\x15RestrictionVisibility\x12\x0f\n\x0bNOT_VISIBLE\x10\x00\x12\x15\n\x11PARTIALLY_VISIBLE\x10\x01\x12\x11\n\rFULLY_VISIBLE\x10\x02*\xe6\x01\n\x07Service\x12\r\n\tPASSENGER\x10\x00\x12\t\n\x05\x43\x41RGO\x10\x01\x12\x1b\n\x17MILITARY_AND_GOVERNMENT\x10\x02\x12\x11\n\rBUSINESS_JETS\x10\x03\x12\x14\n\x10GENERAL_AVIATION\x10\x04\x12\x0f\n\x0bHELICOPTERS\x10\x05\x12\x14\n\x10LIGHTER_THAN_AIR\x10\x06\x12\x0b\n\x07GLIDERS\x10\x07\x12\n\n\x06\x44RONES\x10\x08\x12\x13\n\x0fGROUND_VEHICLES\x10\t\x12\x11\n\rOTHER_SERVICE\x10\n\x12\x13\n\x0fNON_CATEGORIZED\x10\x0b*D\n\x0bTrafficType\x12\x08\n\x04NONE\x10\x00\x12\x0f\n\x0bGROUND_ONLY\x10\x01\x12\x11\n\rAIRBORNE_ONLY\x10\x02\x12\x07\n\x03\x41LL\x10\x03*\x8d\x01\n\nDataSource\x12\x08\n\x04\x41\x44SB\x10\x00\x12\x08\n\x04MLAT\x10\x01\x12\t\n\x05\x46LARM\x10\x02\x12\x07\n\x03\x46\x41\x41\x10\x03\x12\r\n\tESTIMATED\x10\x04\x12\r\n\tSATELLITE\x10\x05\x12\x15\n\x11OTHER_DATA_SOURCE\x10\x06\x12\x07\n\x03UAT\x10\x07\x12\x10\n\x0cSPIDERTRACKS\x10\x08\x12\x07\n\x03\x41US\x10\t*\xb3\x02\n\x04Icon\x12\x08\n\x04\x42\x37\x33\x38\x10\x00\x12\x08\n\x04\x46GTR\x10\x01\x12\t\n\x05\x41SW20\x10\x02\x12\x08\n\x04\x43\x32\x30\x36\x10\x03\x12\x08\n\x04\x43\x33\x30\x33\x10\x04\x12\x08\n\x04LJ60\x10\x05\x12\x08\n\x04Q300\x10\x06\x12\x08\n\x04\x42\x37\x33\x36\x10\x07\x12\r\n\tFOKKER100\x10\x08\x12\x08\n\x04RJ85\x10\t\x12\x08\n\x04\x41\x33\x32\x30\x10\n\x12\x08\n\x04\x42\x37\x35\x37\x10\x0b\x12\x08\n\x04\x42\x37\x36\x37\x10\x0c\x12\x08\n\x04\x41\x33ST\x10\r\x12\x08\n\x04MD11\x10\x0e\x12\x08\n\x04\x41\x33\x33\x30\x10\x0f\x12\x08\n\x04\x41\x33\x34\x33\x10\x10\x12\x08\n\x04\x41\x33\x34\x36\x10\x11\x12\x08\n\x04\x42\x37\x37\x37\x10\x12\x12\x08\n\x04\x42\x37\x34\x37\x10\x13\x12\x08\n\x04\x41\x33\x38\x30\x10\x14\x12\x08\n\x04\x41\x32\x32\x35\x10\x15\x12\x07\n\x03SI2\x10\x16\x12\x06\n\x02\x45\x43\x10\x17\x12\x08\n\x04\x42\x41LL\x10\x18\x12\x08\n\x04GRND\x10\x19\x12\x08\n\x04SLEI\x10\x1a\x12\x08\n\x04\x44RON\x10\x1b\x12\x07\n\x03SAT\x10\x1c\x12\x07\n\x03ISS\x10\x1d*P\n\x06Status\x12\n\n\x06NORMAL\x10\x00\x12\x0e\n\nBACKGROUND\x10\x01\x12\r\n\tEMERGENCY\x10\x02\x12\x11\n\rNOT_AVAILABLE\x10\x03\x12\x08\n\x04LIVE\x10\x04*\xc2\x01\n\x0f\x45mergencyStatus\x12\x10\n\x0cNO_EMERGENCY\x10\x00\x12\x15\n\x11GENERAL_EMERGENCY\x10\x01\x12\x1f\n\x1bLIFEGUARD_MEDICAL_EMERGENCY\x10\x02\x12\x10\n\x0cMINIMUM_FUEL\x10\x03\x12\x15\n\x11NO_COMMUNICATIONS\x10\x04\x12\x19\n\x15UNLAWFUL_INTERFERENCE\x10\x05\x12\x13\n\x0f\x44OWNED_AIRCRAFT\x10\x06\x12\x0c\n\x08RESERVED\x10\x07\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fr24.proto._common_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_RESTRICTIONVISIBILITY']._serialized_start=1713
  _globals['_RESTRICTIONVISIBILITY']._serialized_end=1795
  _globals['_SERVICE']._serialized_start=1798
  _globals['_SERVICE']._serialized_end=2028
  _globals['_TRAFFICTYPE']._serialized_start=2030
  _globals['_TRAFFICTYPE']._serialized_end=2098
  _globals['_DATASOURCE']._serialized_start=2101
  _globals['_DATASOURCE']._serialized_end=2242
  _globals['_ICON']._serialized_start=2245
  _globals['_ICON']._serialized_end=2552
  _globals['_STATUS']._serialized_start=2554
  _globals['_STATUS']._serialized_end=2634
  _globals['_EMERGENCYSTATUS']._serialized_start=2637
  _globals['_EMERGENCYSTATUS']._serialized_end=2831
  _globals['_EMSINFO']._serialized_start=38
  _globals['_EMSINFO']._serialized_end=240
  _globals['_EMSAVAILABILITY']._serialized_start=243
  _globals['_EMSAVAILABILITY']._serialized_end=622
  _globals['_SCHEDULE']._serialized_start=624
  _globals['_SCHEDULE']._serialized_end=712
  _globals['_ROUTE']._serialized_start=714
  _globals['_ROUTE']._serialized_end=768
  _globals['_EXTRAFLIGHTINFO']._serialized_start=771
  _globals['_EXTRAFLIGHTINFO']._serialized_end=1247
  _globals['_SOURCESTATS']._serialized_start=1249
  _globals['_SOURCESTATS']._serialized_end=1314
  _globals['_STATS']._serialized_start=1316
  _globals['_STATS']._serialized_end=1362
  _globals['_FLIGHT']._serialized_start=1365
  _globals['_FLIGHT']._serialized_end=1661
  _globals['_DURATION']._serialized_start=1663
  _globals['_DURATION']._serialized_end=1688
  _globals['_TICK']._serialized_start=1690
  _globals['_TICK']._serialized_end=1711
# @@protoc_insertion_point(module_scope)