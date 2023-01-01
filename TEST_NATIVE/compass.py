from jnius import autoclass

# Use the Android Sensor class to access the magnetometer sensor
Sensor = autoclass('android.hardware.Sensor')
SensorManager = autoclass('android.hardware.SensorManager')

sensor_manager = autoclass('android.content.Context').getSystemService(
    autoclass('android.content.Context').SENSOR_SERVICE)

magnetometer = sensor_manager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD)

#