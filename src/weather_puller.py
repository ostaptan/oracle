import time
import requests

class WeatherPuller:
  def __init__(self, json_data):
    self.json_data = json_data

  def __temperature(self):
    return self.json_data['main']['temp']

  def __weather_type(self):
    return self.json_data['weather'][0]['description']

  def __wind_speed(self):
    return self.json_data['wind']['speed']

  def __pressure(self):
    return self.json_data['main']['pressure']

  def __humidity(self):
    return self.json_data['main']['humidity']

  def __sunset(self):
    timestamp = self.json_data['sys']['sunset']
    return time.strftime('%H:%M', time.gmtime(timestamp))

  def format_speech(self, city):
    return "The weather in {} is currently {} with: a temperature {} degrees and wind speeds reaching {} km/ph. Pressure is {} millibars and humidity {} %. A Sun is going down at {}." \
      .format(
        city,
        self.__weather_type(),
        self.__temperature(),
        self.__wind_speed(),
        self.__pressure(),
        self.__humidity(),
        self.__sunset()
      )

def main(city):
  url = 'https://api.openweathermap.org/data/2.5/weather?appid=a10fd8a212e47edf8d946f26fb4cdef8'
  final_url = url + '&q=' + city + "&units=metric"
  json_data = requests.get(final_url).json()
  wp = WeatherPuller(json_data)
  return wp.format_speech(city)
