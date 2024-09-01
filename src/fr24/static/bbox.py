"""
live feed will only return 1500 flights per bounding box:
idea is to cut the world in vertical slices and collect them

however, since an airspace is congested in different times of the day,
a static bounding box will require many subdivisions to not exceed this limit.

instead, we should use a dynamic bounding box that will change every 30 minutes
to reduce the number of requests
"""

# ruff: noqa: E501
# fmt: off
lng_bounds = [
    -180, -117, -110, -100, -95, -90, -85, -82, -79, -75, -68, -30, -2, 1,
    5, 8, 11, 15, 20, 30, 40, 60, 100, 110, 120, 140, 180
]
"""default static bounds"""

lng_bounds_per_30_min = {
    0: [-180.0, -121.9, -113.3, -101.5, -95.3, -87.9, -82.2, -77.6, -66.9, 9.8, 47.6, 88.3, 113.7, 126.6, 164.1, 180],
    1: [-180.0, -121.5, -112.1, -99.8, -94.2, -86.4, -80.7, -74.7, -46.5, 29.3, 61.1, 104.0, 114.7, 125.0, 151.8, 180],
    2: [-180.0, -120.7, -111.3, -97.9, -91.6, -84.1, -78.3, -70.0, 7.6, 47.4, 80.9, 108.8, 117.0, 131.0, 171.0, 180],
    3: [-180.0, -119.4, -108.7, -97.1, -88.9, -81.4, -75.8, -47.4, 28.7, 58.2, 100.6, 111.5, 119.0, 138.5, 180],
    4: [-180.0, -118.9, -106.7, -95.9, -86.2, -79.7, -71.0, 4.7, 44.6, 77.7, 106.9, 115.1, 124.3, 150.9, 180],
    5: [-180.0, -118.5, -106.2, -95.1, -84.5, -77.3, -49.2, 21.4, 51.8, 87.7, 108.2, 116.0, 126.7, 153.0, 180],
    6: [-180.0, -117.9, -104.7, -93.3, -82.6, -74.2, -28.1, 28.8, 63.4, 100.7, 110.6, 118.1, 134.6, 175.6, 180],
    7: [-180.0, -117.0, -101.0, -89.2, -78.7, -51.2, 17.3, 48.2, 84.8, 108.1, 115.9, 126.3, 151.7, 180],
    8: [-180.0, -115.2, -98.2, -85.8, -73.2, -2.7, 28.2, 56.0, 100.0, 110.1, 117.7, 133.3, 172.9, 180],
    9: [-180.0, -114.1, -96.3, -79.4, -33.1, 16.7, 46.9, 85.5, 107.8, 115.7, 126.4, 151.5, 180],
    10: [-180.0, -112.4, -90.0, -62.7, 6.9, 27.0, 56.0, 98.4, 109.8, 117.2, 132.5, 174.1, 180],
    11: [-180.0, -111.5, -81.8, -27.1, 11.5, 39.1, 74.0, 104.4, 113.2, 120.6, 140.3, 180],
    12: [-180.0, -108.2, -73.0, -2.1, 15.3, 31.1, 59.4, 101.3, 111.1, 118.2, 135.1, 180],
    13: [-180.0, -103.4, -57.5, -2.3, 10.9, 26.0, 46.7, 80.7, 107.2, 115.2, 124.1, 150.0, 180],
    14: [-180.0, -97.1, -40.3, -0.9, 8.9, 20.8, 37.4, 67.0, 103.9, 113.0, 120.2, 140.2, 180],
    15: [-180.0, -90.6, -29.7, -0.7, 8.3, 18.1, 31.9, 54.8, 99.7, 109.8, 117.8, 132.3, 180],
    16: [-180.0, -88.9, -28.6, -0.8, 7.7, 17.7, 30.2, 51.4, 95.2, 109.5, 117.2, 130.8, 180],
    17: [-180.0, -87.9, -31.5, -0.8, 6.9, 14.0, 27.2, 44.1, 78.7, 106.8, 115.2, 125.8, 180],
    18: [-180.0, -87.6, -43.3, -1.6, 5.2, 11.9, 22.9, 37.7, 74.4, 105.3, 113.9, 121.6, 153.0, 180],
    19: [-180.0, -86.6, -48.5, -3.4, 2.7, 9.3, 16.2, 29.2, 51.0, 98.5, 110.0, 118.0, 136.4, 180],
    20: [-180.0, -86.3, -70.9, -5.8, 0.3, 7.1, 12.4, 23.6, 36.5, 73.0, 105.2, 113.9, 121.3, 152.9, 180],
    21: [-180.0, -86.8, -74.1, -8.5, -0.7, 6.0, 10.6, 18.4, 28.7, 49.4, 93.0, 109.8, 117.9, 138.6, 180],
    22: [-180.0, -89.6, -78.1, -34.3, -2.5, 3.7, 8.9, 14.9, 25.2, 41.4, 77.2, 107.2, 116.1, 130.6, 180],
    23: [-180.0, -89.7, -80.8, -66.1, -7.4, -0.2, 6.3, 11.5, 20.5, 32.1, 56.1, 103.1, 113.3, 121.3, 180],
    24: [-180.0, -91.4, -81.5, -74.2, -42.7, -3.1, 1.3, 7.8, 13.2, 23.7, 37.0, 71.5, 106.1, 114.7, 126.8, 180],
    25: [-180.0, -94.6, -83.5, -78.0, -73.1, -35.2, -2.4, 2.3, 8.4, 14.4, 25.2, 40.5, 76.8, 106.8, 115.9, 132.2, 180],
    26: [-180.0, -98.3, -87.4, -81.7, -78.1, -73.8, -45.8, -3.8, 1.1, 7.5, 14.0, 24.8, 40.2, 76.9, 107.1, 116.2, 137.0, 180],
    27: [-180.0, -104.6, -92.6, -84.8, -81.3, -78.5, -74.1, -50.9, -5.8, -0.1, 6.4, 11.8, 22.3, 34.5, 61.9, 104.3, 114.0, 126.4, 180],
    28: [-180.0, -106.0, -96.0, -88.1, -83.7, -81.0, -78.1, -73.9, -52.0, -6.3, -0.5, 6.2, 11.0, 20.5, 32.3, 55.8, 103.5, 114.3, 133.3, 180],
    29: [-180.0, -109.6, -98.3, -92.6, -86.9, -82.6, -80.7, -77.8, -73.8, -52.2, -6.6, -0.6, 5.9, 10.5, 19.1, 30.2, 52.2, 101.6, 114.4, 135.2, 180],
    30: [-180.0, -113.5, -104.2, -97.0, -91.5, -86.2, -82.1, -80.3, -77.1, -73.5, -48.5, -4.5, 0.5, 6.5, 11.2, 20.1, 31.4, 55.5, 104.5, 116.7, 180],
    31: [-180.0, -115.9, -107.4, -98.8, -95.5, -90.1, -84.9, -81.4, -79.4, -75.6, -70.3, -30.8, -2.3, 3.0, 8.7, 14.7, 26.0, 44.4, 82.8, 113.5, 161.1, 180],
    32: [-180.0, -117.5, -111.2, -102.4, -97.1, -93.2, -87.7, -82.8, -80.6, -77.6, -73.9, -59.5, -8.5, -0.4, 6.2, 11.7, 21.4, 36.9, 73.1, 109.4, 145.9, 180],
    33: [-180.0, -118.7, -111.8, -104.1, -97.3, -93.3, -87.9, -83.6, -80.5, -77.3, -73.5, -52.3, -5.6, 2.0, 8.5, 15.7, 28.5, 49.4, 97.2, 121.9, 180],
    34: [-180.0, -119.8, -112.5, -105.1, -98.0, -94.3, -88.5, -84.2, -80.8, -77.8, -73.9, -60.2, -8.3, 0.9, 8.0, 16.0, 28.6, 50.5, 101.7, 146.6, 180],
    35: [-180.0, -121.1, -114.0, -106.6, -98.8, -95.2, -89.4, -84.8, -81.1, -78.3, -74.4, -66.0, -14.5, 0.0, 8.0, 16.2, 29.3, 53.6, 106.5, 180],
    36: [-180.0, -121.4, -114.5, -107.1, -98.7, -95.2, -89.4, -84.6, -81.0, -77.8, -73.9, -60.7, -8.1, 2.4, 10.1, 21.1, 39.1, 75.1, 123.9, 180],
    37: [-180.0, -121.9, -115.2, -108.1, -98.8, -95.1, -89.4, -84.7, -81.2, -78.1, -74.1, -62.2, -8.5, 2.2, 10.6, 22.6, 41.5, 77.6, 135.1, 180],
    38: [-180.0, -122.0, -115.6, -107.9, -98.1, -94.0, -88.3, -84.3, -80.8, -77.5, -73.5, -55.2, -4.5, 5.2, 13.8, 29.1, 55.4, 111.7, 180],
    39: [-180.0, -122.0, -115.9, -107.9, -98.0, -94.1, -88.3, -84.2, -80.7, -77.5, -73.8, -60.9, -4.5, 5.2, 15.6, 30.6, 58.8, 115.2, 180],
    40: [-180.0, -122.0, -115.5, -106.7, -97.9, -94.3, -88.6, -84.3, -80.5, -77.3, -73.5, -51.4, -1.7, 8.3, 20.9, 40.2, 77.9, 139.7, 180],
    41: [-180.0, -122.1, -116.0, -107.5, -98.2, -94.5, -89.0, -84.3, -80.7, -77.4, -73.8, -58.5, -2.1, 8.7, 23.9, 47.0, 93.4, 164.2, 180],
    42: [-180.0, -122.2, -116.1, -107.4, -98.1, -94.4, -88.8, -84.2, -80.4, -76.9, -72.7, -44.2, 2.0, 16.2, 36.9, 76.7, 135.2, 180],
    43: [-180.0, -122.0, -116.2, -107.4, -97.9, -94.0, -88.3, -83.7, -80.0, -76.0, -71.1, -15.9, 7.0, 26.9, 55.3, 114.2, 178.6, 180],
    44: [-180.0, -122.0, -115.8, -106.4, -97.3, -93.2, -87.6, -82.0, -78.3, -74.2, -59.9, -0.3, 22.6, 49.7, 103.6, 151.8, 180],
    45: [-180.0, -121.6, -114.2, -104.7, -97.1, -92.5, -86.4, -81.3, -77.9, -73.8, -50.2, 5.7, 30.8, 66.7, 120.6, 173.1, 180],
    46: [-180.0, -121.3, -113.4, -103.1, -96.1, -90.1, -84.5, -80.3, -76.2, -70.5, -3.3, 28.6, 57.0, 107.8, 138.1, 180],
    47: [-180.0, -121.5, -114.0, -103.0, -95.7, -89.4, -84.0, -79.5, -74.3, -57.5, 11.8, 44.7, 77.7, 116.3, 145.1, 180],
}
"""
dynamic bounds every 30 minutes, 0 = 00:00UTC
this is tuned on 2023-06-15: each slice should contain 1000 flights.
"""
# fmt: on