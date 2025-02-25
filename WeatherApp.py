import requests
import tkinter as tk
from tkinter import messagebox
from flask import Flask, render_template, request
import threading

# OpenWeatherMap API Key (Replace with your own)
API_KEY = "your_api_key_here"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    """Fetch weather data from API"""
    params = {"q": city, "appid": API_KEY, "units": "metric"}  # Use "imperial" for Fahrenheit
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data["cod"] == 200:
        return {
            "city": city,
            "temp": data["main"]["temp"],
            "condition": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
    else:
        return None

# ----------------- Tkinter GUI -----------------
def show_weather():
    """Handles GUI Weather Search"""
    city = city_entry.get()
    weather = get_weather(city)
    if weather:
        result_label.config(text=f"🌡️ Temp: {weather['temp']}°C\n⛅ {weather['condition']}\n💧 Humidity: {weather['humidity']}%\n🌬️ Wind: {weather['wind_speed']} m/s")
    else:
        messagebox.showerror("Error", "City not found!")

def start_gui():
    """Starts the GUI Application"""
    global city_entry, result_label
    root = tk.Tk()
    root.title("Weather App")
    root.geometry("300x250")

    tk.Label(root, text="Enter City:", font=("Arial", 12)).pack()
    city_entry = tk.Entry(root, font=("Arial", 12))
    city_entry.pack()

    tk.Button(root, text="Get Weather", command=show_weather, font=("Arial", 12)).pack()
    result_label = tk.Label(root, text="", font=("Arial", 12))
    result_label.pack()

    root.mainloop()

# ----------------- Flask Web App -----------------
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    """Handles Web Weather Search"""
    weather_data = None
    if request.method == "POST":
        city = request.form["city"]
        weather_data = get_weather(city)
    return render_template("index.html", weather=weather_data)

def start_flask():
    """Runs the Web Server"""
    app.run(debug=True, use_reloader=False)

# ----------------- Choose Mode -----------------
if __name__ == "__main__":
    print("Choose mode: ")
    print("1 - GUI (Tkinter)")
    print("2 - Web App (Flask)")
    choice = input("Enter choice (1/2): ")

    if choice == "1":
        start_gui()
    elif choice == "2":
        threading.Thread(target=start_flask).start()
        print("Flask Web App running at http://127.0.0.1:5000")
    else:
        print("Invalid choice! Restart the script.")
