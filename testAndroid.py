import jpype

def get_lat_lng():
    # Start the JVM
    jpype.startJVM(classpath=['.'])

    # Run the Java code
    GPSTrackerClass = jpype.JClass('GPSTracker')
    gps_tracker = GPSTrackerClass()
    lat = gps_tracker.getLatitude()
    lng = gps_tracker.getLongitude()

    # Shut down the JVM
    jpype.shutdownJVM()

    return lat, lng


lat, lng = get_lat_lng()
print(f'Latitude: {lat}, Longitude: {lng}')
