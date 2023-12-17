# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: request.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rrequest.proto\"\xaf\x07\n\x0b\x46iltersList\x12\x38\n\x14\x61ltitude_ranges_list\x18\x01 \x03(\x0b\x32\x1a.FiltersList.AltitudeRange\x12\x32\n\x11speed_ranges_list\x18\x02 \x03(\x0b\x32\x17.FiltersList.SpeedRange\x12\x38\n\x14\x61irline_filters_list\x18\x03 \x03(\x0b\x32\x1a.FiltersList.AirlineFilter\x12\x16\n\x0e\x63\x61llsigns_list\x18\x04 \x03(\t\x12\x13\n\x0bradars_list\x18\x05 \x03(\t\x12\x11\n\tregs_list\x18\x06 \x03(\t\x12\x31\n\rairports_list\x18\x07 \x03(\x0b\x32\x1a.FiltersList.AirportFilter\x12\x12\n\ntypes_list\x18\t \x03(\t\x12;\n\x16\x62irth_year_ranges_list\x18\n \x03(\x0b\x32\x1b.FiltersList.BirthYearRange\x12+\n\x0corigins_list\x18\x0c \x03(\x0b\x32\x15.FiltersList.ODFilter\x12\x30\n\x11\x64\x65stinations_list\x18\r \x03(\x0b\x32\x15.FiltersList.ODFilter\x12!\n\x0f\x63\x61tegories_list\x18\x0e \x03(\x0e\x32\x08.Service\x1a)\n\rAltitudeRange\x12\x0b\n\x03min\x18\x01 \x01(\x05\x12\x0b\n\x03max\x18\x02 \x01(\x05\x1a&\n\nSpeedRange\x12\x0b\n\x03min\x18\x01 \x01(\x05\x12\x0b\n\x03max\x18\x02 \x01(\x05\x1au\n\rAirlineFilter\x12\x0c\n\x04icao\x18\x01 \x01(\t\x12-\n\x04type\x18\x02 \x01(\x0e\x32\x1f.FiltersList.AirlineFilter.Type\"\'\n\x04Type\x12\x0e\n\nPAINTED_AS\x10\x00\x12\x0f\n\x0bOPERATED_AS\x10\x01\x1a\x8d\x01\n\rAirportFilter\x12\x0c\n\x04iata\x18\x01 \x01(\t\x12\x12\n\ncountry_id\x18\x02 \x01(\x05\x12-\n\x04type\x18\x03 \x01(\x0e\x32\x1f.FiltersList.AirportFilter.Type\"+\n\x04Type\x12\x08\n\x04\x42OTH\x10\x00\x12\x0b\n\x07INBOUND\x10\x01\x12\x0c\n\x08OUTBOUND\x10\x02\x1a*\n\x0e\x42irthYearRange\x12\x0b\n\x03min\x18\x01 \x01(\x05\x12\x0b\n\x03max\x18\x02 \x01(\x05\x1a,\n\x08ODFilter\x12\x0c\n\x04iata\x18\x01 \x01(\t\x12\x12\n\ncountry_id\x18\x02 \x01(\x05\"\xf6\x06\n\x0fLiveFeedRequest\x12\'\n\x06\x62ounds\x18\x01 \x01(\x0b\x32\x17.LiveFeedRequest.Bounds\x12+\n\x08settings\x18\x02 \x01(\x0b\x32\x19.LiveFeedRequest.Settings\x12\"\n\x0c\x66ilters_list\x18\x03 \x01(\x0b\x32\x0c.FiltersList\x12\x17\n\x0f\x63ustom_fleet_id\x18\x04 \x01(\t\x12\x16\n\x0ehighlight_mode\x18\x05 \x01(\x08\x12\x12\n\x05stats\x18\x06 \x01(\x08H\x00\x88\x01\x01\x12\x12\n\x05limit\x18\x07 \x01(\x05H\x01\x88\x01\x01\x12\x13\n\x06maxage\x18\x08 \x01(\x05H\x02\x88\x01\x01\x12?\n\x10restriction_mode\x18\t \x01(\x0e\x32 .LiveFeedRequest.RestrictionModeH\x03\x88\x01\x01\x12.\n\nfield_mask\x18\n \x01(\x0b\x32\x1a.LiveFeedRequest.FieldMask\x12\x19\n\x11selected_flightid\x18\x0b \x03(\x07\x1a\x42\n\x06\x42ounds\x12\r\n\x05north\x18\x01 \x01(\x02\x12\r\n\x05south\x18\x02 \x01(\x02\x12\x0c\n\x04west\x18\x03 \x01(\x02\x12\x0c\n\x04\x65\x61st\x18\x04 \x01(\x02\x1a\x83\x02\n\x08Settings\x12!\n\x0csources_list\x18\x01 \x03(\x0e\x32\x0b.DataSource\x12\x1f\n\rservices_list\x18\x02 \x03(\x0e\x32\x08.Service\x12;\n\x0ctraffic_type\x18\x03 \x01(\x0e\x32%.LiveFeedRequest.Settings.TrafficType\x12\x1c\n\x0fonly_restricted\x18\x04 \x01(\x08H\x00\x88\x01\x01\"D\n\x0bTrafficType\x12\x08\n\x04NONE\x10\x00\x12\x0f\n\x0bGROUND_ONLY\x10\x01\x12\x11\n\rAIRBORNE_ONLY\x10\x02\x12\x07\n\x03\x41LL\x10\x03\x42\x12\n\x10_only_restricted\x1a\x1f\n\tFieldMask\x12\x12\n\nfield_name\x18\x01 \x03(\t\"P\n\x0fRestrictionMode\x12\x0f\n\x0bNOT_VISIBLE\x10\x00\x12\x17\n\x13RESTRICTED_INCLUDED\x10\x01\x12\x13\n\x0fRESTRICTED_ONLY\x10\x02\x42\x08\n\x06_statsB\x08\n\x06_limitB\t\n\x07_maxageB\x13\n\x11_restriction_mode\"\xef\r\n\x10LiveFeedResponse\x12\x32\n\x0c\x66lights_list\x18\x01 \x03(\x0b\x32\x1c.LiveFeedResponse.FlightData\x12+\n\x05stats\x18\x02 \x01(\x0b\x32\x1c.LiveFeedResponse.Statistics\x12:\n\x14selected_flight_info\x18\x03 \x03(\x0b\x32\x1c.LiveFeedResponse.FlightData\x1a\xbf\x0b\n\nFlightData\x12\x10\n\x08\x66lightid\x18\x01 \x01(\x05\x12\x10\n\x08latitude\x18\x02 \x01(\x02\x12\x11\n\tlongitude\x18\x03 \x01(\x02\x12\x0f\n\x07heading\x18\x04 \x01(\x05\x12\x10\n\x08\x61ltitude\x18\x05 \x01(\x05\x12\x14\n\x0cground_speed\x18\x06 \x01(\x05\x12\x0c\n\x04icon\x18\x07 \x01(\x05\x12\x0e\n\x06status\x18\x08 \x01(\x05\x12\x11\n\ttimestamp\x18\t \x01(\x05\x12\x11\n\ton_ground\x18\n \x01(\x08\x12\x10\n\x08\x63\x61llsign\x18\x0b \x01(\t\x12\x1b\n\x06source\x18\x0c \x01(\x0e\x32\x0b.DataSource\x12:\n\nextra_info\x18\r \x01(\x0b\x32&.LiveFeedResponse.FlightData.ExtraInfo\x1a\x91\t\n\tExtraInfo\x12\x0e\n\x06\x66light\x18\x01 \x01(\t\x12\x0b\n\x03reg\x18\x02 \x01(\t\x12;\n\x05route\x18\x03 \x01(\x0b\x32,.LiveFeedResponse.FlightData.ExtraInfo.Route\x12\x0c\n\x04type\x18\x04 \x01(\t\x12\x0e\n\x06squawk\x18\x05 \x01(\x05\x12\x0e\n\x06vspeed\x18\x06 \x01(\x05\x12\x13\n\x0b\x61\x63_birthday\x18\x07 \x01(\t\x12\x16\n\x0e\x63ountry_of_reg\x18\x08 \x01(\x05\x12\x41\n\x08schedule\x18\t \x01(\x0b\x32/.LiveFeedResponse.FlightData.ExtraInfo.Schedule\x12\x0f\n\x07logo_id\x18\n \x01(\x05\x12\x10\n\x08\x61irspace\x18\x0b \x01(\x05\x12<\n\x08\x65ms_info\x18\x0c \x01(\x0b\x32*.LiveFeedResponse.FlightData.ExtraInfo.EMS\x12P\n\x10\x65ms_availability\x18\r \x01(\x0b\x32\x36.LiveFeedResponse.FlightData.ExtraInfo.EMSAvailability\x12\x14\n\x0cicao_address\x18\x0e \x01(\x05\x1a\"\n\x05Route\x12\r\n\x05\x66rom_\x18\x01 \x01(\t\x12\n\n\x02to\x18\x02 \x01(\t\x1aX\n\x08Schedule\x12\x0b\n\x03std\x18\x01 \x01(\x05\x12\x0b\n\x03\x65td\x18\x02 \x01(\x05\x12\x0b\n\x03\x61td\x18\x03 \x01(\x05\x12\x0b\n\x03sta\x18\x04 \x01(\x05\x12\x0b\n\x03\x65ta\x18\x05 \x01(\x05\x12\x0b\n\x03\x61ta\x18\x06 \x01(\x05\x1a\xc6\x01\n\x03\x45MS\x12\x0b\n\x03qnh\x18\x01 \x01(\x05\x12\x0c\n\x04\x61mcp\x18\x02 \x01(\x05\x12\x0c\n\x04\x61\x66ms\x18\x03 \x01(\x05\x12\x0b\n\x03oat\x18\x04 \x01(\x05\x12\x0b\n\x03ias\x18\x05 \x01(\x05\x12\x0b\n\x03tas\x18\x06 \x01(\x05\x12\x0c\n\x04mach\x18\x07 \x01(\x05\x12\x0c\n\x04\x61gps\x18\x08 \x01(\x05\x12\x10\n\x08\x61gpsdiff\x18\t \x01(\x05\x12\x0f\n\x07\x61pflags\x18\n \x01(\x05\x12\x10\n\x08wind_dir\x18\x0b \x01(\x05\x12\x12\n\nwind_speed\x18\x0c \x01(\x05\x12\n\n\x02rs\x18\r \x01(\x05\x1a\xfb\x02\n\x0f\x45MSAvailability\x12\x18\n\x10qnh_availability\x18\x01 \x01(\x08\x12\x19\n\x11\x61mcp_availability\x18\x02 \x01(\x08\x12\x19\n\x11\x61\x66ms_availability\x18\x03 \x01(\x08\x12\x18\n\x10oat_availability\x18\x04 \x01(\x08\x12\x18\n\x10ias_availability\x18\x05 \x01(\x08\x12\x18\n\x10tas_availability\x18\x06 \x01(\x08\x12\x19\n\x11mach_availability\x18\x07 \x01(\x08\x12\x19\n\x11\x61gps_availability\x18\x08 \x01(\x08\x12\x1d\n\x15\x61gpsdiff_availability\x18\t \x01(\x08\x12\x1c\n\x14\x61pflags_availability\x18\n \x01(\x08\x12\x1d\n\x15wind_dir_availability\x18\x0b \x01(\x08\x12\x1f\n\x17wind_speed_availability\x18\x0c \x01(\x08\x12\x17\n\x0frs_availability\x18\r \x01(\x08\x1a|\n\nStatistics\x12\x36\n\x07sources\x18\x01 \x03(\x0b\x32%.LiveFeedResponse.Statistics.SourceKV\x1a\x36\n\x08SourceKV\x12\x1b\n\x06source\x18\x01 \x01(\x0e\x32\x0b.DataSource\x12\r\n\x05\x63ount\x18\x02 \x01(\x05\"\x89\x01\n\x17LiveFeedPlaybackRequest\x12+\n\x11live_feed_request\x18\x01 \x01(\x0b\x32\x10.LiveFeedRequest\x12\x11\n\ttimestamp\x18\x02 \x01(\x05\x12\x10\n\x08prefetch\x18\x03 \x01(\x05\x12\x12\n\x05hfreq\x18\x04 \x01(\x05H\x00\x88\x01\x01\x42\x08\n\x06_hfreq\"I\n\x18LiveFeedPlaybackResponse\x12-\n\x12live_feed_response\x18\x01 \x01(\x0b\x32\x11.LiveFeedResponse*\xe6\x01\n\x07Service\x12\r\n\tPASSENGER\x10\x00\x12\t\n\x05\x43\x41RGO\x10\x01\x12\x1b\n\x17MILITARY_AND_GOVERNMENT\x10\x02\x12\x11\n\rBUSINESS_JETS\x10\x03\x12\x14\n\x10GENERAL_AVIATION\x10\x04\x12\x0f\n\x0bHELICOPTERS\x10\x05\x12\x14\n\x10LIGHTER_THAN_AIR\x10\x06\x12\x0b\n\x07GLIDERS\x10\x07\x12\n\n\x06\x44RONES\x10\x08\x12\x13\n\x0fGROUND_VEHICLES\x10\t\x12\x11\n\rOTHER_SERVICE\x10\n\x12\x13\n\x0fNON_CATEGORIZED\x10\x0b*\x8d\x01\n\nDataSource\x12\x08\n\x04\x41\x44SB\x10\x00\x12\x08\n\x04MLAT\x10\x01\x12\t\n\x05\x46LARM\x10\x02\x12\x07\n\x03\x46\x41\x41\x10\x03\x12\r\n\tESTIMATED\x10\x04\x12\r\n\tSATELLITE\x10\x05\x12\x15\n\x11OTHER_DATA_SOURCE\x10\x06\x12\x07\n\x03UAT\x10\x07\x12\x10\n\x0cSPIDERTRACKS\x10\x08\x12\x07\n\x03\x41US\x10\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'request_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SERVICE._serialized_start=3846
  _SERVICE._serialized_end=4076
  _DATASOURCE._serialized_start=4079
  _DATASOURCE._serialized_end=4220
  _FILTERSLIST._serialized_start=18
  _FILTERSLIST._serialized_end=961
  _FILTERSLIST_ALTITUDERANGE._serialized_start=527
  _FILTERSLIST_ALTITUDERANGE._serialized_end=568
  _FILTERSLIST_SPEEDRANGE._serialized_start=570
  _FILTERSLIST_SPEEDRANGE._serialized_end=608
  _FILTERSLIST_AIRLINEFILTER._serialized_start=610
  _FILTERSLIST_AIRLINEFILTER._serialized_end=727
  _FILTERSLIST_AIRLINEFILTER_TYPE._serialized_start=688
  _FILTERSLIST_AIRLINEFILTER_TYPE._serialized_end=727
  _FILTERSLIST_AIRPORTFILTER._serialized_start=730
  _FILTERSLIST_AIRPORTFILTER._serialized_end=871
  _FILTERSLIST_AIRPORTFILTER_TYPE._serialized_start=828
  _FILTERSLIST_AIRPORTFILTER_TYPE._serialized_end=871
  _FILTERSLIST_BIRTHYEARRANGE._serialized_start=873
  _FILTERSLIST_BIRTHYEARRANGE._serialized_end=915
  _FILTERSLIST_ODFILTER._serialized_start=917
  _FILTERSLIST_ODFILTER._serialized_end=961
  _LIVEFEEDREQUEST._serialized_start=964
  _LIVEFEEDREQUEST._serialized_end=1850
  _LIVEFEEDREQUEST_BOUNDS._serialized_start=1355
  _LIVEFEEDREQUEST_BOUNDS._serialized_end=1421
  _LIVEFEEDREQUEST_SETTINGS._serialized_start=1424
  _LIVEFEEDREQUEST_SETTINGS._serialized_end=1683
  _LIVEFEEDREQUEST_SETTINGS_TRAFFICTYPE._serialized_start=1595
  _LIVEFEEDREQUEST_SETTINGS_TRAFFICTYPE._serialized_end=1663
  _LIVEFEEDREQUEST_FIELDMASK._serialized_start=1685
  _LIVEFEEDREQUEST_FIELDMASK._serialized_end=1716
  _LIVEFEEDREQUEST_RESTRICTIONMODE._serialized_start=1718
  _LIVEFEEDREQUEST_RESTRICTIONMODE._serialized_end=1798
  _LIVEFEEDRESPONSE._serialized_start=1853
  _LIVEFEEDRESPONSE._serialized_end=3628
  _LIVEFEEDRESPONSE_FLIGHTDATA._serialized_start=2031
  _LIVEFEEDRESPONSE_FLIGHTDATA._serialized_end=3502
  _LIVEFEEDRESPONSE_FLIGHTDATA_EXTRAINFO._serialized_start=2333
  _LIVEFEEDRESPONSE_FLIGHTDATA_EXTRAINFO._serialized_end=3502
  _LIVEFEEDRESPONSE_FLIGHTDATA_EXTRAINFO_ROUTE._serialized_start=2795
  _LIVEFEEDRESPONSE_FLIGHTDATA_EXTRAINFO_ROUTE._serialized_end=2829
  _LIVEFEEDRESPONSE_FLIGHTDATA_EXTRAINFO_SCHEDULE._serialized_start=2831
  _LIVEFEEDRESPONSE_FLIGHTDATA_EXTRAINFO_SCHEDULE._serialized_end=2919
  _LIVEFEEDRESPONSE_FLIGHTDATA_EXTRAINFO_EMS._serialized_start=2922
  _LIVEFEEDRESPONSE_FLIGHTDATA_EXTRAINFO_EMS._serialized_end=3120
  _LIVEFEEDRESPONSE_FLIGHTDATA_EXTRAINFO_EMSAVAILABILITY._serialized_start=3123
  _LIVEFEEDRESPONSE_FLIGHTDATA_EXTRAINFO_EMSAVAILABILITY._serialized_end=3502
  _LIVEFEEDRESPONSE_STATISTICS._serialized_start=3504
  _LIVEFEEDRESPONSE_STATISTICS._serialized_end=3628
  _LIVEFEEDRESPONSE_STATISTICS_SOURCEKV._serialized_start=3574
  _LIVEFEEDRESPONSE_STATISTICS_SOURCEKV._serialized_end=3628
  _LIVEFEEDPLAYBACKREQUEST._serialized_start=3631
  _LIVEFEEDPLAYBACKREQUEST._serialized_end=3768
  _LIVEFEEDPLAYBACKRESPONSE._serialized_start=3770
  _LIVEFEEDPLAYBACKRESPONSE._serialized_end=3843
# @@protoc_insertion_point(module_scope)
