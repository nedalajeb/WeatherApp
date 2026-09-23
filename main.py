import sys
import os
from dotenv import load_dotenv
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt

load_dotenv()

# creat a new type of window called WeatherApp using QWidget as it base
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
      # the user needs a place to type the city name, so I create QLineEdit object
        self.city_input = QLineEdit()
        # create a QLineEdit and store it inside self.city_input
        self.city_input.setPlaceholderText("Enter city name")
        self.city_input.setStyleSheet("font-size: 18px; padding:8px;")
        # show the user that they should enter a city, so we can tell QlineEdit
        self.get_weather_button = QPushButton("Get Weather")
        self.get_weather_button.setStyleSheet("font-size: 18px; padding:8px;")
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["Celsius", "Fahrenheit", "Kelvin"])
        self.unit_combo.setStyleSheet("font-size: 16px; padding:6px;")

        self.weather_label = QLabel()
        self.weather_label.setAlignment(Qt.AlignCenter)
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)

        self.weather_label.setStyleSheet(
            "background-color: rgb(255, 255, 255);"
            "color: rgb(0, 0,0);"
            "font-size: 24px; padding: 10px;"

        )

        #our main window need title "Weather App to do that we need setWindowtitle()"
        self.setWindowTitle("Weather App")
        self.setFixedSize(400, 500)
        # we need container that will organize them
        # creat an object layout from class QVBoxLayout
        layout = QVBoxLayout()
        layout.addWidget(self.city_input)
        layout.addWidget(self.get_weather_button)
        layout.addWidget(self.unit_combo)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.weather_label)

        # use this layout to organize my widgets
        self.setLayout(layout)
        self.get_weather_button.clicked.connect(self.get_weather)
    def get_weather(self):
        city = self.city_input.text().strip()
        if not(city):
            self.weather_label.setText("Please enter a city name")
            return
        unit = self.unit_combo.currentText()
        if unit == "Celsius":
            units = "metric"
        else:
            units = "imperial"

        if unit == "Celsius":
            symbol = "°C"
        else:
            symbol = "°F"

        self.weather_label.setText("Loading please wait...")

        api_url = "https://api.openweathermap.org/data/2.5/weather"

        api_key = os.getenv("OPENWEATHER_API_KEY")

        params = {"q": city, "appid": api_key, "units": units}
        response = requests.get(api_url, params=params)

        if response.status_code == 404:
            self.weather_label.setText("City not found")
            return
        if response.status_code !=200:
            self.weather_label.setText("Something went Wrong")
            return


        data = response.json()
        temperature = round(data["main"]["temp"])
        description = data ["weather"][0]["description"]
        weather_main = data["weather"][0]["main"]
        if weather_main == "Clear":
            icon = ("☀️")

        elif weather_main == "Rain":
           icon = ("🌧️")
        elif weather_main == "Clouds":
            icon = ("☁️")
        elif weather_main == "Snow":
            icon = "❄️"

        else:
            icon = "🌡️"

        humidity = data ["main"]["humidity"]


        self.icon_label.setText(icon)
        self.icon_label.setStyleSheet("font-size: 80px; padding: 10px;")


        self.weather_label.setText(
            f"Temperature: {temperature}{symbol} \n"
            f"Weather: {description.capitalize()}\n"
            f"Humidity: {humidity}%"
             f"\n"
            
             f"\n"

            f"Design By: Nedal Ajeb"

        )



app = QApplication(sys.argv)
window = WeatherApp()
window.show()
sys.exit(app.exec_())




