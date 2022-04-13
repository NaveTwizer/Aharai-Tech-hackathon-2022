import Adafruit_DHT


def calculate_temperature():
    humidity, tempt = Adafruit_DHT.read_retry(11, 4)
    return humidity, tempt
