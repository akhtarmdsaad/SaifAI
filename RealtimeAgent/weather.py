from private import OPEN_WEATHER_API_KEY, MY_CITY
class Weather:
    def __init__(self):
        self.url = "https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    def search(self, city=MY_CITY):
        import requests
        response = requests.get(self.url.format(city=city, api_key=OPEN_WEATHER_API_KEY))
        weather_dict = response.json()

        important_details_dict = {
            "city": weather_dict["name"],
            "temperature": weather_dict["main"]["temp"],
            "feels_like": weather_dict["main"]["feels_like"],
            "temp_min": weather_dict["main"]["temp_min"],
            "temp_max": weather_dict["main"]["temp_max"],
            "pressure": weather_dict["main"]["pressure"],
            "humidity": weather_dict["main"]["humidity"],
            "title":weather_dict["weather"][0]["main"],
            "description": weather_dict["weather"][0]["description"],
            "icon": weather_dict["weather"][0]["icon"],
            "visibility": weather_dict["visibility"],
            "wind_speed": weather_dict["wind"]["speed"],
            "wind_deg": weather_dict["wind"]["deg"],
            "country": weather_dict["sys"]["country"],
            "sunrise": weather_dict["sys"]["sunrise"],
            "sunset": weather_dict["sys"]["sunset"]
        }

        return str(important_details_dict)
        

