import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city_name = data["name"]
        country = data["sys"]["country"]
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        result_text = (
            f"Weather in {city_name}, {country}:\n"
            f"Temperature: {temperature}°C\n"
            f"Weather: {weather_description.capitalize()}\n"
            f"Humidity: {humidity}%\n"
            f"Pressure: {pressure} hPa\n"
            f"Wind Speed: {wind_speed} m/s"
        )
        result_label.config(text=result_text)
    else:
        messagebox.showerror("Error", "City not found or invalid API key. Please try again.")

def clear_fields():
    city_entry.delete(0, tk.END)
    result_label.config(text="")

def show_home_interface():
    for widget in window.winfo_children():
        widget.destroy()
    home_label = tk.Label(window, text="Welcome to the Weather App", font=("Arial", 16, "bold"), bg="#FFFFFF", fg="#333333")
    home_label.pack(pady=40)
    start_button = tk.Button(window, text="Start", font=("Arial", 14, "bold"), bg="#4CAF50", fg="#FFFFFF", command=show_weather_interface)
    start_button.pack(pady=20)
    footer_label = tk.Label(window, text="Powered by OpenWeatherMap", font=("Arial", 10), bg="#FFFFFF", fg="#666666")
    footer_label.pack(side="bottom", pady=10)

def show_weather_interface():
    for widget in window.winfo_children():
        widget.destroy()
    try:
        background_image = Image.open("project.png")
        background_image = background_image.resize((450, 400), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(background_image)
        canvas = tk.Canvas(window, width=450, height=400)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
        window.bg_image = bg_image
    except FileNotFoundError:
        messagebox.showerror("Error", "Background image not found.")
    api_key = "43cfd1394f26e5dae167fd5d2cba06c3"
    city_label = tk.Label(window, text="Enter City Name:", font=("Arial", 12), bg="#FFFFFF", fg="#333333")
    canvas.create_window(115, 50, window=city_label)
    global city_entry
    city_entry = tk.Entry(window, font=("Arial", 12), width=20)
    canvas.create_window(275, 50, window=city_entry)
    def on_fetch_weather():
        city = city_entry.get().strip()
        if city:
            get_weather(city, api_key)
        else:
            messagebox.showerror("Error", "Please enter a city name.")
    fetch_button = tk.Button(window, text="Get Weather", font=("Arial", 12, "bold"), bg="#4CAF50", fg="#FFFFFF", command=on_fetch_weather)
    canvas.create_window(150, 120, window=fetch_button)
    retry_button = tk.Button(window, text="Retry", font=("Arial", 12, "bold"), bg="#FF5733", fg="#FFFFFF", command=clear_fields)
    canvas.create_window(300, 120, window=retry_button)
    back_button = tk.Button(window, text="Back", font=("Arial", 12, "bold"), bg="#333333", fg="#FFFFFF", command=show_home_interface)
    canvas.create_window(225, 180, window=back_button)
    global result_label
    result_label = tk.Label(window, text="", font=("Arial", 12), bg="#FFFFFF", fg="#333333", justify="left", wraplength=400)
    canvas.create_window(225, 250, window=result_label)

window = tk.Tk()
window.title("Weather App")
window.geometry("450x400")
window.resizable(False, False)
window.config(bg="#FFFFFF")
show_home_interface()
window.mainloop()