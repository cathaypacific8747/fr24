# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: fr24/proto/_follow_flight.proto
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
    'fr24/proto/_follow_flight.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from fr24.proto import _common_pb2 as fr24_dot_proto_dot___common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1f\x66r24/proto/_follow_flight.proto\x1a\x18\x66r24/proto/_common.proto\"]\n\tImageInfo\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x11\n\tcopyright\x18\x02 \x01(\t\x12\x11\n\tthumbnail\x18\x03 \x01(\t\x12\x0e\n\x06medium\x18\x04 \x01(\t\x12\r\n\x05large\x18\x05 \x01(\t\"\xec\x02\n\x0c\x41ircraftInfo\x12\x14\n\x0cicao_address\x18\x01 \x01(\x05\x12\x0b\n\x03reg\x18\x02 \x01(\x05\x12\x16\n\x0e\x63ountry_of_reg\x18\x03 \x01(\x05\x12\x0c\n\x04type\x18\x04 \x01(\t\x12\x1b\n\x04icon\x18\x05 \x01(\x0e\x32\r._common.Icon\x12\x18\n\x10\x66ull_description\x18\x06 \x01(\t\x12\x0b\n\x03msn\x18\x07 \x01(\t\x12!\n\x07service\x18\x08 \x01(\x0e\x32\x10._common.Service\x12\x15\n\rac_birth_date\x18\t \x01(\t\x12\x13\n\x0b\x61\x63_age_text\x18\n \x01(\t\x12\x1f\n\x0bimages_list\x18\x0b \x03(\x0b\x32\n.ImageInfo\x12\x16\n\x0eis_test_flight\x18\x0c \x01(\x08\x12\x15\n\rmsn_available\x18\r \x01(\x08\x12\x15\n\rage_available\x18\x0e \x01(\x08\x12\x19\n\x11registered_owners\x18\x0f \x01(\t\",\n\x05Point\x12\x10\n\x08latitude\x18\x01 \x01(\x05\x12\x11\n\tlongitude\x18\x02 \x01(\x05\"1\n\nCoordinate\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x15\n\x05point\x18\x02 \x01(\x0b\x32\x06.Point\"E\n\x03\x46ix\x12\x0f\n\x07\x61irport\x18\x01 \x01(\t\x12\x0c\n\x04\x61rea\x18\x02 \x01(\t\x12\x1f\n\ncoordinate\x18\x03 \x01(\x0b\x32\x0b.Coordinate\"3\n\nAltArrival\x12\x15\n\x07\x61rrival\x18\x01 \x01(\x0b\x32\x04.Fix\x12\x0e\n\x06length\x18\x02 \x01(\x02\"\xc6\x01\n\nFlightPlan\x12\x11\n\tdeparture\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65stination\x18\x02 \x01(\t\x12\x18\n\x10\x66light_plan_icao\x18\x03 \x01(\t\x12\x0e\n\x06length\x18\x04 \x01(\x01\x12\"\n\ralt_arrival_1\x18\x05 \x01(\x0b\x32\x0b.AltArrival\x12\"\n\ralt_arrival_2\x18\x06 \x01(\x0b\x32\x0b.AltArrival\x12\x1e\n\x0ewaypoints_list\x18\x07 \x03(\x0b\x32\x06.Point\"\xbf\x02\n\x0cScheduleInfo\x12\x15\n\rflight_number\x18\x01 \x01(\t\x12\x16\n\x0eoperated_by_id\x18\x02 \x01(\r\x12\x15\n\rpainted_as_id\x18\x03 \x01(\r\x12\x11\n\torigin_id\x18\x04 \x01(\r\x12\x16\n\x0e\x64\x65stination_id\x18\x05 \x01(\r\x12\x16\n\x0e\x64iverted_to_id\x18\x06 \x01(\r\x12\x1b\n\x13scheduled_departure\x18\x07 \x01(\r\x12\x19\n\x11scheduled_arrival\x18\x08 \x01(\r\x12\x18\n\x10\x61\x63tual_departure\x18\t \x01(\r\x12\x16\n\x0e\x61\x63tual_arrival\x18\n \x01(\r\x12\x14\n\x0c\x61rr_terminal\x18\x0b \x01(\t\x12\x10\n\x08\x61rr_gate\x18\x0c \x01(\t\x12\x14\n\x0c\x62\x61ggage_belt\x18\r \x01(\t\"\x9a\x02\n\x0e\x46lightProgress\x12\x1a\n\x12traversed_distance\x18\x01 \x01(\r\x12\x1a\n\x12remaining_distance\x18\x02 \x01(\r\x12\x14\n\x0c\x65lapsed_time\x18\x03 \x01(\r\x12\x16\n\x0eremaining_time\x18\x04 \x01(\r\x12\x0b\n\x03\x65ta\x18\x05 \x01(\r\x12\x1d\n\x15great_circle_distance\x18\x06 \x01(\r\x12\x18\n\x10mean_flight_time\x18\x07 \x01(\r\x12\"\n\x0c\x66light_stage\x18\x08 \x01(\x0e\x32\x0c.FlightStage\x12\"\n\x0c\x64\x65lay_status\x18\t \x01(\x0e\x32\x0c.DelayStatus\x12\x14\n\x0cprogress_pct\x18\n \x01(\x05\"b\n\x13\x46ollowFlightRequest\x12\x11\n\tflight_id\x18\x01 \x01(\x07\x12\x38\n\x10restriction_mode\x18\x02 \x01(\x0e\x32\x1e._common.RestrictionVisibility\"\xcc\x03\n\x12\x45xtendedFlightInfo\x12\x10\n\x08\x66lightid\x18\x01 \x01(\r\x12\x0b\n\x03lat\x18\x02 \x01(\x02\x12\x0b\n\x03lon\x18\x03 \x01(\x02\x12\r\n\x05track\x18\x04 \x01(\x05\x12\x0b\n\x03\x61lt\x18\x05 \x01(\x05\x12\r\n\x05speed\x18\x06 \x01(\x05\x12\x1f\n\x06status\x18\x07 \x01(\x0e\x32\x0f._common.Status\x12\x11\n\ttimestamp\x18\x08 \x01(\x04\x12\x11\n\ton_ground\x18\t \x01(\x08\x12\x10\n\x08\x63\x61llsign\x18\n \x01(\t\x12#\n\x06source\x18\x0b \x01(\x0e\x32\x13._common.DataSource\x12\x32\n\x10\x65ms_availability\x18\x0c \x01(\x0b\x32\x18._common.EMSAvailability\x12\"\n\x08\x65ms_info\x18\r \x01(\x0b\x32\x10._common.EMSInfo\x12\x1b\n\x13squawk_availability\x18\x0e \x01(\x08\x12\x0e\n\x06squawk\x18\x0f \x01(\x05\x12\x1b\n\x13vspeed_availability\x18\x10 \x01(\x08\x12\x0e\n\x06vspeed\x18\x11 \x01(\x05\x12\x1d\n\x15\x61irspace_availability\x18\x12 \x01(\x08\x12\x10\n\x08\x61irspace\x18\x13 \x01(\t\"y\n\nTrailPoint\x12\x13\n\x0bsnapshot_id\x18\x01 \x01(\x04\x12\x0b\n\x03lat\x18\x02 \x01(\x02\x12\x0b\n\x03lon\x18\x03 \x01(\x02\x12\x10\n\x08\x61ltitude\x18\x04 \x01(\x05\x12\x0b\n\x03spd\x18\x05 \x01(\r\x12\x0f\n\x07heading\x18\x06 \x01(\r\x12\x0c\n\x04vspd\x18\x07 \x01(\x05\"\x80\x02\n\x14\x46ollowFlightResponse\x12$\n\raircraft_info\x18\x01 \x01(\x0b\x32\r.AircraftInfo\x12 \n\x0b\x66light_plan\x18\x02 \x01(\x0b\x32\x0b.FlightPlan\x12$\n\rschedule_info\x18\x03 \x01(\x0b\x32\r.ScheduleInfo\x12(\n\x0f\x66light_progress\x18\x04 \x01(\x0b\x32\x0f.FlightProgress\x12(\n\x0b\x66light_info\x18\x05 \x01(\x0b\x32\x13.ExtendedFlightInfo\x12&\n\x11\x66light_trail_list\x18\x06 \x03(\x0b\x32\x0b.TrailPoint*X\n\x0b\x46lightStage\x12\x0b\n\x07UNKNOWN\x10\x00\x12\r\n\tON_GROUND\x10\x01\x12\x0e\n\nTAKING_OFF\x10\x02\x12\x0c\n\x08\x41IRBORNE\x10\x03\x12\x0f\n\x0bON_APPROACH\x10\x04*7\n\x0b\x44\x65layStatus\x12\x08\n\x04GRAY\x10\x00\x12\t\n\x05GREEN\x10\x01\x12\n\n\x06YELLOW\x10\x02\x12\x07\n\x03RED\x10\x03\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fr24.proto._follow_flight_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_FLIGHTSTAGE']._serialized_start=2497
  _globals['_FLIGHTSTAGE']._serialized_end=2585
  _globals['_DELAYSTATUS']._serialized_start=2587
  _globals['_DELAYSTATUS']._serialized_end=2642
  _globals['_IMAGEINFO']._serialized_start=61
  _globals['_IMAGEINFO']._serialized_end=154
  _globals['_AIRCRAFTINFO']._serialized_start=157
  _globals['_AIRCRAFTINFO']._serialized_end=521
  _globals['_POINT']._serialized_start=523
  _globals['_POINT']._serialized_end=567
  _globals['_COORDINATE']._serialized_start=569
  _globals['_COORDINATE']._serialized_end=618
  _globals['_FIX']._serialized_start=620
  _globals['_FIX']._serialized_end=689
  _globals['_ALTARRIVAL']._serialized_start=691
  _globals['_ALTARRIVAL']._serialized_end=742
  _globals['_FLIGHTPLAN']._serialized_start=745
  _globals['_FLIGHTPLAN']._serialized_end=943
  _globals['_SCHEDULEINFO']._serialized_start=946
  _globals['_SCHEDULEINFO']._serialized_end=1265
  _globals['_FLIGHTPROGRESS']._serialized_start=1268
  _globals['_FLIGHTPROGRESS']._serialized_end=1550
  _globals['_FOLLOWFLIGHTREQUEST']._serialized_start=1552
  _globals['_FOLLOWFLIGHTREQUEST']._serialized_end=1650
  _globals['_EXTENDEDFLIGHTINFO']._serialized_start=1653
  _globals['_EXTENDEDFLIGHTINFO']._serialized_end=2113
  _globals['_TRAILPOINT']._serialized_start=2115
  _globals['_TRAILPOINT']._serialized_end=2236
  _globals['_FOLLOWFLIGHTRESPONSE']._serialized_start=2239
  _globals['_FOLLOWFLIGHTRESPONSE']._serialized_end=2495
# @@protoc_insertion_point(module_scope)