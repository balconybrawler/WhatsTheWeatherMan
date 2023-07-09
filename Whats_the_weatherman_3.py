import customtkinter
import tkinter as tk
from tkinter import ttk
from tkinter import * #import all
from tkinter import Text
import json
import customtkinter as CTk
from customtkinter import CTkLabel
import requests
import weather_api
from weather_api import api_key
import os
from PIL import Image, ImageTk
import calendar
import datetime
import sys

#pulling the key and setup
my_key = api_key
base_url = 'http://api.weatherapi.com/v1'



# Check if the file exists
if os.path.exists('weather.json'):
    # Open the file and load the JSON data
    with open('weather.json', 'r') as file:
        try:
            weather_file = json.load(file)
        except json.JSONDecodeError:
            weather_file = {}
else:
    weather_file = {}

dictionary = {}

if dictionary == {}:
    dictionary = weather_file

#create the json to store the multi day forecast
if os.path.exists('multi_day_forecast.json'):
    #open the file and load the JSON data
    with open('multi_day_forecast.json', 'r') as forecast_file:
        try:
            multi_day_forecast_file = json.load(forecast_file)
        except json.JSONDecodeError:
            multi_day_forecast_file = {}
else:
    multi_day_forecast_file = {}
multi_day_dictionary = {}

if multi_day_dictionary == {}:
    multi_day_dictionary = multi_day_forecast_file

#set the appearance theme
customtkinter.set_appearance_mode(("dark"))

#set the color theme
customtkinter.set_default_color_theme(("blue"))


#create root window
root = customtkinter.CTk()

#transparent root window hack
# root.wm_attributes('-transparentcolor', 'red')

#background frame

#window title
root.title("Whats The Weatherman 3")


#window size
root.geometry("600x800")

#the frame to place our text in
weather_data_frame = customtkinter.CTkFrame(root, fg_color=("#C4DFAA"), height=300, width=550)

# #another frame for our icons and related data
# lower_frame = tk.Frame(root, bg=("#C4DFAA"), height=150, width=400)


def exit_program():
    sys.exit()
#function to grab users desired city
#this function will ping the api with the string the user entere)
#the purpose of this function is to grab the city and pass it to the api call so we can dynamically
#change what city we want to find the weather for depending on the users text entry in the entry widget
def grab_city():
    users_selected_city = users_city.get()
    print(f"the user has chosen his weather city to be: {users_selected_city}")
    if os.path.exists('weather.json'):
        with open('weather.json', 'r') as weather_data:
            try:
                weather_dictionary = json.load(weather_data)
            except json.JSONDecodeError:
                weather_dictionary = {}
    else:
        weather_dictionary = {}

    params = {
        'key': my_key,
        'q': users_selected_city,
        'days': 1
    }
    response = requests.get('http://api.weatherapi.com/v1/forecast.json', params=params)
    data = response.json()
    if response.status_code == 200:
        print(f"{data}\n")
    else:
        print("Request failed with status code:", response.status_code)

    with open('weather.json', 'w') as weather_data:
        json.dump(data, weather_data)

    country = data['location']['country']
    city = data['location']['name']
    temperature = data['current']['temp_c']
    wind_speed = data['current']["wind_kph"]
    local_time = data['location']['localtime']
    condition = data['current']['condition']

    print(f"Country: {country}")
    print(f"The weather in {city}: ")
    print(f"The temperature is {temperature} °C")
    print(f"The wind speed is {wind_speed} km/h")
    print(f"The time in {city} is {local_time}")
    print(f"The conditions: {condition['text']} ")

    def fade_image(image_label, new_image_path):
        # Create a transparent image with the same size as the image label
        transparent_image = Image.new("RGBA", image_size, (0, 0, 0, 0))
        transparent_photo = ImageTk.PhotoImage(transparent_image)

        # Replace the current image with the transparent image
        image_label.configure(image=transparent_photo)
        image_label.image = transparent_photo

        # Open the new image
        new_image = Image.open(new_image_path)
        new_image = new_image.resize(image_size)  # Resize the new image to match the label size
        new_photo = ImageTk.PhotoImage(new_image)

        # Fade in the new image
        alpha = 0
        while alpha < 255:
            alpha += 8  # Adjust the step size to control the fade speed
            faded_image = Image.blend(transparent_image, new_image.convert("RGBA"), alpha / 255)
            faded_photo = ImageTk.PhotoImage(faded_image)

            # Update the image label with the faded image
            image_label.configure(image=faded_photo)
            image_label.image = faded_photo
            image_label.update()

        # Update the image label with the final image
        image_label.configure(image=new_photo)
        image_label.image = new_photo

#matches the current condition to the label which is placed inside the weather data frame
    #also places the appropriate icon inside the lower frame
    def image_to_condition_matcher():
        global weather_data_frame

        # lower frame color label
        lower_frame_color_label = customtkinter.CTkLabel(root, fg_color=("#F7FFE5"), width=410, height=160)
        lower_frame_color_label.place(x=95, y=455)

        #the lower frame is the frame below the larger frame on the second page
        lower_frame = tk.Frame(root, bg=("#C4DFAA"), height=150, width=400)
        lower_frame.place(x=100, y=460)

        if condition['text'] == 'Sunny':
            # Load the icon
            sun_icon = Image.open("day/113.png")
            # Convert to a tkinter-compatible object
            sun_icon_tk = ImageTk.PhotoImage(sun_icon)
            # Create the label widget to store the image
            sun_icon_label = tk.Label(master=root, image=sun_icon_tk, bg=("#C4DFAA"))
            sun_icon_label.place(x=270, y=540)

            # Store the image reference to prevent garbage collection
            sun_icon_label.image = sun_icon_tk

            return "weather images/Sunny.png"


        elif condition['text'] == 'Clear':
            # Load the icon
            clear_icon = Image.open("day/113.png")
            # Convert to a tkinter-compatible object
            clear_icon_tk = ImageTk.PhotoImage(clear_icon)
            # Create the label widget to store the image
            sun_icon_label = tk.Label(master=root, image=clear_icon_tk, bg=("#C4DFAA"))
            sun_icon_label.place(x=270, y=540)

            # Store the image reference to prevent garbage collection
            sun_icon_label.image = clear_icon_tk



            return ("weather images/base.png")

        elif condition['text'] == 'Partly cloudy':
            # Load the icon
            partly_icon = Image.open("day/116.png")
            # Convert to a tkinter-compatible object
            partly_icon_tk = ImageTk.PhotoImage(partly_icon)
            # Create the label widget to store the image
            sun_icon_label = tk.Label(master=root, image=partly_icon_tk, bg=("#C4DFAA"))
            sun_icon_label.place(x=270, y=540)

            # Store the image reference to prevent garbage collection
            sun_icon_label.image = partly_icon_tk
            return ("weather images/Partly_cloudy.png")


        elif condition['text'] == 'Overcast':
            # Load the icon
            overcast_icon = Image.open("day/119.png")
            # Convert to a tkinter-compatible object
            overcast_icon_tk = ImageTk.PhotoImage(overcast_icon)
            # Create the label widget to store the image
            sun_icon_label = tk.Label(master=root, image=overcast_icon_tk, bg=("#C4DFAA"))
            sun_icon_label.place(x=270, y=540)

            # Store the image reference to prevent garbage collection
            sun_icon_label.image = overcast_icon_tk
            return ("weather images/Overcast.png")


        elif condition['text'] == 'Mist':
            # Load the icon
            mist_icon = Image.open("day/248.png")
            # Convert to a tkinter-compatible object
            mist_icon_tk = ImageTk.PhotoImage(mist_icon)
            # Create the label widget to store the image
            mist_icon_label = tk.Label(master=root, image=mist_icon_tk, bg=("#C4DFAA"))
            mist_icon_label.place(x=270, y=540)

            # Store the image reference to prevent garbage collection
            mist_icon_label.image = mist_icon_tk
            return("weather images/Mist.png")


        elif condition['text'] == "Patchy rain possible" or condition['text'] == "Patchy snow possible" or condition[
            'text'] == "Patchy sleet possible" or condition['text'] == "Patchy freezing drizzle possible":

            # Load the icon
            patchy_rain_icon = Image.open("day/317.png")
            # Convert to a tkinter-compatible object
            patchy_rain_icon_tk = ImageTk.PhotoImage(patchy_rain_icon)
            # Create the label widget to store the image
            patchy_rain_icon_label = tk.Label(master=root, image=patchy_rain_icon_tk, bg=("#C4DFAA"))
            patchy_rain_icon_label.place(x=270, y=540)
            # Store the image reference to prevent garbage collection
            patchy_rain_icon_label.image = patchy_rain_icon_tk
            return "weather images/Mist.png"


        elif condition['text'] == 'Thundery outbreaks possible':
            # Load the icon
            thundery_outbreaks_icon = Image.open("day/386.png")
            # Convert to a tkinter-compatible object
            thundery_outbreaks_icon_tk = ImageTk.PhotoImage(thundery_outbreaks_icon)
            # Create the label widget to store the image
            thundery_outbreaks_icon_label = tk.Label(master=root, image=thundery_outbreaks_icon_tk, bg=("#C4DFAA"))
            thundery_outbreaks_icon_label.place(x=270, y=541)

            # Store the image reference to prevent garbage collection
            thundery_outbreaks_icon_label.image = thundery_outbreaks_icon_tk

            return("weather images/thunder.png")

        elif condition['text'] == 'Blowing snow':
            # Load the icon
            blowing_snow_icon = Image.open("day/326.png")
            # Convert to a tkinter-compatible object
            blowing_snow_icon_tk = ImageTk.PhotoImage(blowing_snow_icon)
            # Create the label widget to store the image
            blowing_snow_icon_label = tk.Label(master=root, image=blowing_snow_icon_tk, bg=("#C4DFAA"))
            blowing_snow_icon_label.place(x=270, y=541)

            # Store the image reference to prevent garbage collection
            blowing_snow_icon_label.image = blowing_snow_icon_tk
            return("weather images/Blowing Snow.png")

        elif condition['text'] == 'Fog':
            # Load the icon
            fog_icon = Image.open("day/248.png")
            # Convert to a tkinter-compatible object
            fog_icon_tk = ImageTk.PhotoImage(fog_icon)
            # Create the label widget to store the image
            fog_icon_label = tk.Label(master=root, image=fog_icon_tk, bg=("#C4DFAA"))
            fog_icon_label.place(x=270, y=541)

            # Store the image reference to prevent garbage collection
            fog_icon_label.image = fog_icon_tk

            # Store the image reference to prevent garbage collection
            fog_icon_label.image = fog_icon_tk
            return("weather images/foggy.png")

        elif condition['text'] == 'Freezing fog':
            # Load the icon
            freezing_fog_icon = Image.open("day/314.png")
            # Convert to a tkinter-compatible object
            freezing_fog_icon_tk = ImageTk.PhotoImage(freezing_fog_icon)
            # Create the label widget to store the image
            freezing_fog_icon_label = tk.Label(master=root, image=freezing_fog_icon_tk, bg=("#C4DFAA"))
            freezing_fog_icon_label.place(x=270, y=541)

            # Store the image reference to prevent garbage collection
            freezing_fog_icon_label.image = freezing_fog_icon_tk
            return("weather images/freezing_rain.png")


        elif condition['text'] == 'Patchy light drizzle' or condition['text'] == 'Light drizzle' or condition[
            'text'] == 'Patchy light rain' or condition['text'] == 'Light rain':
            # Load the icon
            patchy_drizzle_icon = Image.open("day/176.png")
            # Convert to a tkinter-compatible object
            patchy_drizzle_icon_tk = ImageTk.PhotoImage(patchy_drizzle_icon)
            # Create the label widget to store the image
            patchy_drizzle_icon_label = tk.Label(master=root, image=patchy_drizzle_icon_tk, bg=("#C4DFAA"))
            patchy_drizzle_icon_label.place(x=270, y=541)

            # Store the image reference to prevent garbage collection
            patchy_drizzle_icon_label.image = patchy_drizzle_icon_tk

            return "weather images/Patchy Rain.png"


        elif condition['text'] == 'Light sleet' or condition['text'] == 'Light snow' or condition['text'] == 'Patchy moderate snow' or condition['text'] == 'Moderate snow':
            # Load the icon
            blowing_snow_icon = Image.open("day/179.png")
            # Convert to a tkinter-compatible object
            blowing_snow_icon_tk = ImageTk.PhotoImage(blowing_snow_icon)
            # Create the label widget to store the image
            blowing_snow_icon_label = tk.Label(master=root, image=blowing_snow_icon_tk, bg=("#C4DFAA"))
            blowing_snow_icon_label.place(x=270, y=541)

            # Store the image reference to prevent garbage collection
            blowing_snow_icon_label.image = blowing_snow_icon_tk
            return "weather images/Blowing Snow.png"


        elif condition['text'] == 'Light sleet' or condition['text'] == 'Light snow' or condition[
            'text'] == 'Patchy moderate snow' or condition['text'] == 'Moderate snow':
            # Load the icon
            sleet_icon = Image.open("day/326.png")
            # Convert to a tkinter-compatible object
            sleet_icon_tk = ImageTk.PhotoImage(sleet_icon)
            # Create the label widget to store the image
            sleet_icon_label = tk.Label(master=root, image=sleet_icon_tk, bg=("#C4DFAA"))
            sleet_icon_label.place(x=270, y=541)

            # Store the image reference to prevent garbage collection
            sleet_icon_label.image = sleet_icon_tk
            return "weather images/Blowing Snow.png"


        elif condition['text'] == 'Heavy snow' or condition['text'] == 'Ice pellets':
            # Load the icon
            heavy_snow_icon = Image.open("day/338.png")
            # Convert to a tkinter-compatible object
            heavy_snow_icon_tk = ImageTk.PhotoImage(heavy_snow_icon)
            # Create the label widget to store the image
            heavy_snow_icon_label = tk.Label(master=root, image=heavy_snow_icon_tk, bg=("#C4DFAA"))
            heavy_snow_icon_label.place(x=270, y=541)

            # Store the image reference to prevent garbage collection
            heavy_snow_icon_label.image = heavy_snow_icon_tk
            return "weather images/blizzard.png"



        elif condition['text'] == 'Light rain shower' or condition['text'] == 'Moderate or heavy rain shower' or condition['text'] == 'Moderate rain':
            # Load the icon
            moderate_rain_icon = Image.open("day/308.png")
            # Convert to a tkinter-compatible object
            moderate_rain_icon_tk = ImageTk.PhotoImage(moderate_rain_icon)
            # Create the label widget to store the image
            moderate_rain_icon_label = tk.Label(master=root, image=moderate_rain_icon_tk, bg=("#C4DFAA"))
            moderate_rain_icon_label.place(x=270, y=541)

            # Store the image reference to prevent garbage collection
            moderate_rain_icon_label.image = moderate_rain_icon_tk
            return "weather images/Rain.png"


        elif condition['text'] == 'Torrential rain shower' or condition['text'] == 'Light sleet showers' or condition[
            'text'] == 'Moderate or heavy sleet showers' or condition['text'] == 'Light snow showers' or condition[
            'text'] == 'Moderate or heavy snow showers':
            # Load the icon
            heavy_rain_icon = Image.open("day/308.png")
            # Convert to a tkinter-compatible object
            heavy_rain_icon_tk = ImageTk.PhotoImage(heavy_rain_icon)
            # Create the label widget to store the image
            heavy_rain_icon_label = tk.Label(master=root, image=heavy_rain_icon_tk, bg=("#C4DFAA"))
            heavy_rain_icon_label.place(x=270, y=541)

            # Store the image reference to prevent garbage collection
            heavy_rain_icon_label.image = heavy_rain_icon_tk
            return "weather images/rainy_day.png"



        elif condition['text'] == 'Light showers of ice pellets' or condition['text'] == 'Moderate or heavy showers of ice pellets':
            # Load the icon
            freezing_rain_icon = Image.open("day/320.png")
            # Convert to a tkinter-compatible object
            freezing_rain_icon_tk = ImageTk.PhotoImage(freezing_rain_icon)
            # Create the label widget to store the image
            freezing_rain_icon_label = tk.Label(master=root, image=freezing_rain_icon_tk, bg=("#C4DFAA"))
            freezing_rain_icon_label.place(x=270, y=541)

            # Store the image reference to prevent garbage collection
            freezing_rain_icon_label.image = freezing_rain_icon_tk
            return "weather images/freezing_rain.png"



        elif condition['text'] == 'Patchy light rain with thunder' or condition[
            'text'] == 'Moderate or heavy rain with thunder' or condition['text'] == 'Patchy light snow with thunder' or \
                condition['text'] == 'Moderate or heavy snow with thunder':
            # Load the icon
            rain_thunder_icon = Image.open("day/248.png")
            # Convert to a tkinter-compatible object
            rain_thunder_icon_tk = ImageTk.PhotoImage(rain_thunder_icon)
            # Create the label widget to store the image
            rain_thunder_icon_label = tk.Label(master=root, image=rain_thunder_icon_tk, bg=("#C4DFAA"))
            rain_thunder_icon_label.place(x=270, y=541)

            # Store the image reference to prevent garbage collection
            rain_thunder_icon_label.image = rain_thunder_icon_tk


            return "weather images/thunder rain snow.png"



    image_path = image_to_condition_matcher()
    fade_image(image_label, image_path)

    # we display the temperature dynamically everytime the user enters a location

    def display_temperature():
        #dictionary required data stored in temp
        temp = data['current']['temp_c']
        text = f"{temp}°C"
        country = data['location']['country']
        city = data['location']['name']
        time = data['location']['localtime']
        wind_speed2 = data['current']["wind_kph"]
        humidity = data['current']['humidity']
        feels_like = data['current']['feelslike_c']
        chance_of_rain = data['forecast']['forecastday'][0]['hour'][0]['chance_of_rain']


        #label behind the weather data frame
        weather_data_label = customtkinter.CTkLabel(root, fg_color=("#F7FFE5"), bg_color=("#C4D7B2"), width=564, height=315)
        weather_data_label.place(x=20, y=52)
        #the frame to place our text in
        weather_data_frame = customtkinter.CTkFrame(root, fg_color=("#C4DFAA"), height=300, width=550, corner_radius=5, bg_color=("#C4D7B2"))
        weather_data_frame.place(x=27, y=60)




        #the label to display the temperature which is overlayed ontop of the weather data frame
        temperature_label = customtkinter.CTkLabel(master=weather_data_frame, text=str(text), font=("Arial", 75, "bold"), fg_color=("#C4DFAA"), bg_color=("#393646"),  padx=4, pady=4, text_color=("#73A9AD"))
        temperature_label.place(relx=0.5, rely=0.5, anchor="center")

        #display the country in the frame
        country_textbox = tk.Label(master=weather_data_frame, bg="#C4DFAA", font=("Arial", 25, "bold"), fg="#73A9AD", text=str(country))
        country_textbox.place(relx=.5, rely=.15, anchor="center")

        #display the city in the frame
        city_textbox = tk.Label(master=weather_data_frame, bg="#C4DFAA", font=("Arial", 30, "bold"), fg="#73A9AD", text=str(city))
        city_textbox.place(relx=.5, rely=.3, anchor="center")

        #display the date and time
        time_textbox = tk.Label(master=weather_data_frame, bg="#C4DFAA", font=("Arial", 15, "bold"), fg="#73A9AD", text=str(time))
        time_textbox.place(relx=.5, rely=.7, anchor="center")

        #the current conditions textbox overlaid on top of the frame
        conditions_textbox = tk.Label(master=weather_data_frame, bg="#C4DFAA", font=("Arial", 15, "bold"), fg="#73A9AD")
        conditions_textbox.place(relx=.5, rely=.8, anchor="center")

        #windspeed textbox
        wind_speed2 = tk.Label(master=weather_data_frame, bg="#C4DFAA", font=("Arial", 15, "bold"), fg="#73A9AD", text=str(f"Wind Speed: {wind_speed2} km/h"))
        wind_speed2.place(relx=.5, rely=.9, anchor="center")

        #humidity textbox
        humidity_textbox = tk.Label(master=root, bg="#C4DFAA", font=("Arial", 15, "bold"), fg="#73A9AD", text=str(f"Humidity: {humidity}"))
        humidity_textbox.place(x=240, y=461)

        #feels liket textbox
        feels_like_textbox = tk.Label(master=root, bg="#C4DFAA", font=("Arial", 15, "bold"), fg="#73A9AD", text=str(f"Feels Like: {feels_like}°C"))
        feels_like_textbox.place(x=215, y=491)

        # feels like textbox
        chance_of_rain_textbox = tk.Label(master=root, bg="#C4DFAA", font=("Arial", 15, "bold"), fg="#73A9AD", text=str(f"Chance of Rain: {chance_of_rain}%"))
        chance_of_rain_textbox.place(x=208, y=521)

        # dynamically update the textbox that displays current weather conditions
        def update_textbox():
            conditions_textbox.config(text=condition['text'])

        # call the function
        update_textbox()


    display_temperature()

    def show_back_forward_buttons():

        # load in the arrow images
        # back_button = Image.open('back_arrow.png')
        forward_button = Image.open('forward_arrow.png')


        # resize the arrow icons
        icon_size = (32, 32)
        forward_icon = forward_button.resize(icon_size)
        forward_icon_tk = ImageTk.PhotoImage(forward_icon)


        # buttons label
        live_forward_button_label = customtkinter.CTkLabel(root, width=61, height=46, fg_color=("#F7FFE5"), text=" ", corner_radius=4, bg_color=("#C4DFAA"))
        live_forward_button_label.place(x=520, y=747)

        # blit the buttons to screen
        live_forward_button = customtkinter.CTkButton(root, image=forward_icon_tk, command=forward_button_multi_day_prediction, text=" ", width=1, bg_color=("#C4DFAA"), corner_radius=4, fg_color=("#C4DFAA"))
        live_forward_button.image = forward_icon_tk #round 2 fight!
        live_forward_button.place(x=523, y=750)

        #

    # dark_button_label = customtkinter.CTkLabel(master=multi_window_label, width=63, height=46, fg_color=("black) text=" ", corner_radius=4, bg_color="black")
    # dark_button_label.place(x=9, y=748)
    #
    # trend_day_back_button = customtkinter.CTkButton(master=multi_window_label, image=back_icon_tk, text=" ", width=1, bg_color="black", corner_radius=4, fg_color=("#1F6E8C"),command=when_trend_day_back_button_pressed)
    # trend_day_back_button.place(x=14, y=751)
    # trend_day_back_button.image = back_icon_tk



    show_back_forward_buttons() #call it


# Load the initial image
image = Image.open("weather images/base.png")
image_size = image.size  # Store the size of the image
photo = ImageTk.PhotoImage(image)

# Create an image label
image_label = tk.Label(root, image=photo)
image_label.image = photo  # Keep a reference to prevent garbage collection
image_label.pack()

#when refresh weather city is pressed it runs the grab city function which handles the api request
# and grabs the users chosen city and stores it in a variable
# we can do multiple requests so long as they are not concurrent so if the user wants to look at another
#city just create two buttons and we can split the app down the middle with the layout

condition = dictionary['current']['condition']


#buttons and labels
#exit
exit_program_label = customtkinter.CTkLabel(root, text=" ", bg_color=("#F7FFE5"), height=33, width=146)
exit_program_label.place(relx=.5, rely=.95, anchor="center")

exit_program = customtkinter.CTkButton(root, text="Exit", text_color=("white"), fg_color=("#73A9AD"), bg_color=("#F7FFE5"), corner_radius=7, command=exit_program, font=("Arial", 12, "bold"))
exit_program.place(relx=.5, rely=.95, anchor="center")
#entry widget that accepts users query for city
users_city = customtkinter.CTkEntry(master=root,fg_color=("#73A9AD"), placeholder_text="Please Enter Your City", placeholder_text_color=("white"), text_color=("white"), corner_radius=5)
users_city.place(x=150, y=400)

print_city_button = customtkinter.CTkButton(master=root, text="Check Weather", command=grab_city, fg_color=("#73A9AD"), text_color=("white"), bg_color=("#F7FFE5"))
print_city_button.place(x=315, y=400)


#forward and back button functionality


def forward_button_multi_day_prediction():

    #grab the users city and ping the api dump the multi day forecast data into the
    #multi day forecast json

    users_selected_city = users_city.get()
    # global city
    # if users_selected_city is None:
    #     users_selected_city = city
    print(f"the user has chosen his weather city to be: {users_selected_city}")
    if os.path.exists('multi_day_forecast.json'):
        with open('multi_day_forecast.json', 'r') as forecast_file:
            try:
                multi_day_forecast_file = json.load(forecast_file)
            except json.JSONDecodeError:
                multi_day_forecast_file = {}
    else:
        multi_day_forecast_file = {}

    params = {
        'key': my_key,
        'q': users_selected_city,
        'days': 4
    }
    multi_day_response = requests.get('http://api.weatherapi.com/v1/forecast.json', params=params)
    data = multi_day_response.json()
    if multi_day_response.status_code == 200:
        print(f"{data}\n")
    else:
        print("Request failed with status code:", multi_day_response.status_code)

    with open('multi_day_forecast.json', 'w') as forecast_file:
        json.dump(data, forecast_file)

    # switching screens to the multi day forecast screen

    def clear_screen():
        # Clear all the widgets in the root window
        for widget in root.winfo_children():
            widget.destroy()

    clear_screen()


    def draw_widgets():
        # Load the initial image
        multi_window_image = Image.open("weather images/multi_day_windows.png")

        image_size = image.size  # Store the size of the image
        multi_window_photo = ImageTk.PhotoImage(multi_window_image)

        # Create an image label
        multi_window_label = tk.Label(root, image=multi_window_photo)
        multi_window_label.image = multi_window_photo
        multi_window_label.place(x=0, y=0)  # Keep a reference to prevent garbage collection
        #exiting the program function again random errors
        def exiting_again():
            sys.exit()
        #exit program
        exit_program_label = customtkinter.CTkLabel(root, text=" ", bg_color=("black"), height=34, width=147, )
        exit_program_label.place(relx=.5, rely=.97, anchor="center")

        exit_program = customtkinter.CTkButton(root, font=("Arial", 12, "bold"), text="Exit", text_color=("white"), fg_color=("#1F6E8C"), bg_color=("black"), corner_radius=7, command=exiting_again)
        exit_program.place(relx=.5, rely=.97, anchor="center")

################ this function handles bringing the program back to the starting page #################
        def trend_multi_day_back_button():
            #load in the arrow images
            back_button = Image.open('back_arrow.png')


            # resize the arrow icons
            icon_size = (32, 32)
            back_icon = back_button.resize(icon_size)

            # convert arrow icons to tkinter compatible format
            back_icon_tk = ImageTk.PhotoImage(back_icon)


#########################brings you back to the beginning on the program########################
            def when_trend_day_back_button_pressed():
                clear_screen()

                def grab_city():
                    global city
                    exit_program_label = customtkinter.CTkLabel(root, text=" ", bg_color=("#F7FFE5"), height=34, width=147)
                    exit_program_label.place(relx=.5, rely=.95, anchor="center")

                    exit_program = customtkinter.CTkButton(root, text="Exit", text_color=("#1F6E8C"), fg_color=("#C4DFAA"), bg_color=("#F7FFE5"), corner_radius=7, command=exiting_again)
                    exit_program.place(relx=.5, rely=.95, anchor="center")

                    users_selected_city = users_city.get()
                    print(f"the user has chosen his weather city to be: {users_selected_city}")
                    if users_selected_city is None:
                        users_selected_city = city


                    if os.path.exists('weather.json'):
                        with open('weather.json', 'r') as weather_data:
                            try:
                                weather_dictionary = json.load(weather_data)
                            except json.JSONDecodeError:
                                weather_dictionary = {}
                    else:
                        weather_dictionary = {}

                    params = {
                        'key': my_key,
                        'q': users_selected_city,
                        'days': 1
                    }
                    response = requests.get('http://api.weatherapi.com/v1/forecast.json', params=params)
                    data = response.json()
                    if response.status_code == 200:
                        print(f"{data}\n")
                    else:
                        print("Request failed with status code:", response.status_code)

                    with open('weather.json', 'w') as weather_data:
                        json.dump(data, weather_data)

                    country = data['location']['country']
                    city = data['location']['name']
                    temperature = data['current']['temp_c']
                    wind_speed = data['current']["wind_kph"]
                    local_time = data['location']['localtime']
                    condition = data['current']['condition']



                    # print(f"Country: {country}")
                    # print(f"The weather in {city}: ")
                    # print(f"The temperature is {temperature} °C")
                    # print(f"The wind speed is {wind_speed} km/h")
                    # print(f"The time in {city} is {local_time}")
                    # print(f"The conditions: {condition['text']} ")

                    def fade_image(image_label, new_image_path):
                        # Create a transparent image with the same size as the image label
                        transparent_image = Image.new("RGBA", image_size, (0, 0, 0, 0))
                        transparent_photo = ImageTk.PhotoImage(transparent_image)

                        # Replace the current image with the transparent image
                        image_label.configure(image=transparent_photo)
                        image_label.image = transparent_photo

                        # Open the new image
                        new_image = Image.open(new_image_path)
                        new_image = new_image.resize(image_size)  # Resize the new image to match the label size
                        new_photo = ImageTk.PhotoImage(new_image)

                        # Fade in the new image
                        alpha = 0
                        while alpha < 255:
                            alpha += 8  # Adjust the step size to control the fade speed
                            faded_image = Image.blend(transparent_image, new_image.convert("RGBA"), alpha / 255)
                            faded_photo = ImageTk.PhotoImage(faded_image)

                            # Update the image label with the faded image
                            image_label.configure(image=faded_photo)
                            image_label.image = faded_photo
                            image_label.update()

                        # Update the image label with the final image
                        image_label.configure(image=new_photo)
                        image_label.image = new_photo

                    # matches the current condition to the label which is placed inside the weather data frame
                    # also places the appropriate icon inside the lower frame
                    def image_to_condition_matcher():
                        global weather_data_frame

                        # lower frame color label
                        lower_frame_color_label = customtkinter.CTkLabel(root, fg_color=("#F7FFE5"), width=410, height=160)
                        lower_frame_color_label.place(x=95, y=455)

                        # the lower frame is the frame below the larger frame on the second page
                        lower_frame = tk.Frame(root, bg=("#C4DFAA"), height=150, width=400)
                        lower_frame.place(x=100, y=460)

                        if condition['text'] == 'Sunny':
                            # Load the icon
                            sun_icon = Image.open("day/113.png")
                            # Convert to a tkinter-compatible object
                            sun_icon_tk = ImageTk.PhotoImage(sun_icon)
                            # Create the label widget to store the image
                            sun_icon_label = tk.Label(master=root, image=sun_icon_tk, bg=("#C4DFAA"))
                            sun_icon_label.place(x=270, y=540)

                            # Store the image reference to prevent garbage collection
                            sun_icon_label.image = sun_icon_tk

                            return "weather images/Sunny.png"


                        elif condition['text'] == 'Clear':
                            # Load the icon
                            clear_icon = Image.open("day/113.png")
                            # Convert to a tkinter-compatible object
                            clear_icon_tk = ImageTk.PhotoImage(clear_icon)
                            # Create the label widget to store the image
                            sun_icon_label = tk.Label(master=root, image=clear_icon_tk, bg=("#C4DFAA"))
                            sun_icon_label.place(x=270, y=540)

                            # Store the image reference to prevent garbage collection
                            sun_icon_label.image = clear_icon_tk

                            return ("weather images/base.png")

                        elif condition['text'] == 'Partly cloudy':
                            # Load the icon
                            partly_icon = Image.open("day/116.png")
                            # Convert to a tkinter-compatible object
                            partly_icon_tk = ImageTk.PhotoImage(partly_icon)
                            # Create the label widget to store the image
                            sun_icon_label = tk.Label(master=root, image=partly_icon_tk, bg=("#C4DFAA"))
                            sun_icon_label.place(x=270, y=540)

                            # Store the image reference to prevent garbage collection
                            sun_icon_label.image = partly_icon_tk
                            return ("weather images/Partly_cloudy.png")


                        elif condition['text'] == 'Overcast':
                            # Load the icon
                            overcast_icon = Image.open("day/119.png")
                            # Convert to a tkinter-compatible object
                            overcast_icon_tk = ImageTk.PhotoImage(overcast_icon)
                            # Create the label widget to store the image
                            sun_icon_label = tk.Label(master=root, image=overcast_icon_tk, bg=("#C4DFAA"))
                            sun_icon_label.place(x=270, y=540)

                            # Store the image reference to prevent garbage collection
                            sun_icon_label.image = overcast_icon_tk
                            return ("weather images/Overcast.png")


                        elif condition['text'] == 'Mist':
                            # Load the icon
                            mist_icon = Image.open("day/248.png")
                            # Convert to a tkinter-compatible object
                            mist_icon_tk = ImageTk.PhotoImage(mist_icon)
                            # Create the label widget to store the image
                            mist_icon_label = tk.Label(master=root, image=mist_icon_tk, bg=("#C4DFAA"))
                            mist_icon_label.place(x=270, y=540)

                            # Store the image reference to prevent garbage collection
                            mist_icon_label.image = mist_icon_tk
                            return ("weather images/Mist.png")


                        elif condition['text'] == "Patchy rain possible" or condition[
                            'text'] == "Patchy snow possible" or condition[
                            'text'] == "Patchy sleet possible" or condition[
                            'text'] == "Patchy freezing drizzle possible":

                            # Load the icon
                            patchy_rain_icon = Image.open("day/317.png")
                            # Convert to a tkinter-compatible object
                            patchy_rain_icon_tk = ImageTk.PhotoImage(patchy_rain_icon)
                            # Create the label widget to store the image
                            patchy_rain_icon_label = tk.Label(master=root, image=patchy_rain_icon_tk, bg=("#C4DFAA"))
                            patchy_rain_icon_label.place(x=270, y=540)
                            # Store the image reference to prevent garbage collection
                            patchy_rain_icon_label.image = patchy_rain_icon_tk
                            return "weather images/Mist.png"


                        elif condition['text'] == 'Thundery outbreaks possible':
                            # Load the icon
                            thundery_outbreaks_icon = Image.open("day/386.png")
                            # Convert to a tkinter-compatible object
                            thundery_outbreaks_icon_tk = ImageTk.PhotoImage(thundery_outbreaks_icon)
                            # Create the label widget to store the image
                            thundery_outbreaks_icon_label = tk.Label(master=root, image=thundery_outbreaks_icon_tk,
                                                                     bg=("#C4DFAA"))
                            thundery_outbreaks_icon_label.place(x=270, y=541)

                            # Store the image reference to prevent garbage collection
                            thundery_outbreaks_icon_label.image = thundery_outbreaks_icon_tk

                            return ("weather images/thunder.png")

                        elif condition['text'] == 'Blowing snow':
                            # Load the icon
                            blowing_snow_icon = Image.open("day/326.png")
                            # Convert to a tkinter-compatible object
                            blowing_snow_icon_tk = ImageTk.PhotoImage(blowing_snow_icon)
                            # Create the label widget to store the image
                            blowing_snow_icon_label = tk.Label(master=root, image=blowing_snow_icon_tk, bg=("#C4DFAA"))
                            blowing_snow_icon_label.place(x=270, y=541)

                            # Store the image reference to prevent garbage collection
                            blowing_snow_icon_label.image = blowing_snow_icon_tk
                            return ("weather images/Blowing Snow.png")

                        elif condition['text'] == 'Fog':
                            # Load the icon
                            fog_icon = Image.open("day/248.png")
                            # Convert to a tkinter-compatible object
                            fog_icon_tk = ImageTk.PhotoImage(fog_icon)
                            # Create the label widget to store the image
                            fog_icon_label = tk.Label(master=root, image=fog_icon_tk, bg=("#C4DFAA"))
                            fog_icon_label.place(x=270, y=541)

                            # Store the image reference to prevent garbage collection
                            fog_icon_label.image = fog_icon_tk

                            # Store the image reference to prevent garbage collection
                            fog_icon_label.image = fog_icon_tk
                            return ("weather images/foggy.png")

                        elif condition['text'] == 'Freezing fog':
                            # Load the icon
                            freezing_fog_icon = Image.open("day/314.png")
                            # Convert to a tkinter-compatible object
                            freezing_fog_icon_tk = ImageTk.PhotoImage(freezing_fog_icon)
                            # Create the label widget to store the image
                            freezing_fog_icon_label = tk.Label(master=root, image=freezing_fog_icon_tk, bg=("#C4DFAA"))
                            freezing_fog_icon_label.place(x=270, y=541)

                            # Store the image reference to prevent garbage collection
                            freezing_fog_icon_label.image = freezing_fog_icon_tk
                            return ("weather images/freezing_rain.png")


                        elif condition['text'] == 'Patchy light drizzle' or condition['text'] == 'Light drizzle' or \
                                condition[
                                    'text'] == 'Patchy light rain' or condition['text'] == 'Light rain':
                            # Load the icon
                            patchy_drizzle_icon = Image.open("day/176.png")
                            # Convert to a tkinter-compatible object
                            patchy_drizzle_icon_tk = ImageTk.PhotoImage(patchy_drizzle_icon)
                            # Create the label widget to store the image
                            patchy_drizzle_icon_label = tk.Label(master=root, image=patchy_drizzle_icon_tk,
                                                                 bg=("#C4DFAA"))
                            patchy_drizzle_icon_label.place(x=270, y=541)

                            # Store the image reference to prevent garbage collection
                            patchy_drizzle_icon_label.image = patchy_drizzle_icon_tk

                            return "weather images/Patchy Rain.png"


                        elif condition['text'] == 'Light sleet' or condition['text'] == 'Light snow' or condition[
                            'text'] == 'Patchy moderate snow' or condition['text'] == 'Moderate snow':
                            # Load the icon
                            blowing_snow_icon = Image.open("day/179.png")
                            # Convert to a tkinter-compatible object
                            blowing_snow_icon_tk = ImageTk.PhotoImage(blowing_snow_icon)
                            # Create the label widget to store the image
                            blowing_snow_icon_label = tk.Label(master=root, image=blowing_snow_icon_tk, bg=("#C4DFAA"))
                            blowing_snow_icon_label.place(x=270, y=541)

                            # Store the image reference to prevent garbage collection
                            blowing_snow_icon_label.image = blowing_snow_icon_tk
                            return "weather images/Blowing Snow.png"


                        elif condition['text'] == 'Light sleet' or condition['text'] == 'Light snow' or condition[
                            'text'] == 'Patchy moderate snow' or condition['text'] == 'Moderate snow':
                            # Load the icon
                            sleet_icon = Image.open("day/326.png")
                            # Convert to a tkinter-compatible object
                            sleet_icon_tk = ImageTk.PhotoImage(sleet_icon)
                            # Create the label widget to store the image
                            sleet_icon_label = tk.Label(master=root, image=sleet_icon_tk, bg=("#C4DFAA"))
                            sleet_icon_label.place(x=270, y=541)

                            # Store the image reference to prevent garbage collection
                            sleet_icon_label.image = sleet_icon_tk
                            return "weather images/Blowing Snow.png"


                        elif condition['text'] == 'Heavy snow' or condition['text'] == 'Ice pellets':
                            # Load the icon
                            heavy_snow_icon = Image.open("day/338.png")
                            # Convert to a tkinter-compatible object
                            heavy_snow_icon_tk = ImageTk.PhotoImage(heavy_snow_icon)
                            # Create the label widget to store the image
                            heavy_snow_icon_label = tk.Label(master=root, image=heavy_snow_icon_tk, bg=("#C4DFAA"))
                            heavy_snow_icon_label.place(x=270, y=541)

                            # Store the image reference to prevent garbage collection
                            heavy_snow_icon_label.image = heavy_snow_icon_tk
                            return "weather images/blizzard.png"



                        elif condition['text'] == 'Light rain shower' or condition[
                            'text'] == 'Moderate or heavy rain shower' or condition['text'] == 'Moderate rain':
                            # Load the icon
                            moderate_rain_icon = Image.open("day/308.png")
                            # Convert to a tkinter-compatible object
                            moderate_rain_icon_tk = ImageTk.PhotoImage(moderate_rain_icon)
                            # Create the label widget to store the image
                            moderate_rain_icon_label = tk.Label(master=root, image=moderate_rain_icon_tk,
                                                                bg=("#C4DFAA"))
                            moderate_rain_icon_label.place(x=270, y=541)

                            # Store the image reference to prevent garbage collection
                            moderate_rain_icon_label.image = moderate_rain_icon_tk
                            return "weather images/Rain.png"


                        elif condition['text'] == 'Torrential rain shower' or condition[
                            'text'] == 'Light sleet showers' or condition[
                            'text'] == 'Moderate or heavy sleet showers' or condition['text'] == 'Light snow showers' or \
                                condition[
                                    'text'] == 'Moderate or heavy snow showers':
                            # Load the icon
                            heavy_rain_icon = Image.open("day/308.png")
                            # Convert to a tkinter-compatible object
                            heavy_rain_icon_tk = ImageTk.PhotoImage(heavy_rain_icon)
                            # Create the label widget to store the image
                            heavy_rain_icon_label = tk.Label(master=root, image=heavy_rain_icon_tk, bg=("#C4DFAA"))
                            heavy_rain_icon_label.place(x=270, y=541)

                            # Store the image reference to prevent garbage collection
                            heavy_rain_icon_label.image = heavy_rain_icon_tk
                            return "weather images/rainy_day.png"



                        elif condition['text'] == 'Light showers of ice pellets' or condition[
                            'text'] == 'Moderate or heavy showers of ice pellets':
                            # Load the icon
                            freezing_rain_icon = Image.open("day/320.png")
                            # Convert to a tkinter-compatible object
                            freezing_rain_icon_tk = ImageTk.PhotoImage(freezing_rain_icon)
                            # Create the label widget to store the image
                            freezing_rain_icon_label = tk.Label(master=root, image=freezing_rain_icon_tk,
                                                                bg=("#C4DFAA"))
                            freezing_rain_icon_label.place(x=270, y=541)

                            # Store the image reference to prevent garbage collection
                            freezing_rain_icon_label.image = freezing_rain_icon_tk
                            return "weather images/freezing_rain.png"



                        elif condition['text'] == 'Patchy light rain with thunder' or condition[
                            'text'] == 'Moderate or heavy rain with thunder' or condition[
                            'text'] == 'Patchy light snow with thunder' or \
                                condition['text'] == 'Moderate or heavy snow with thunder':
                            # Load the icon
                            rain_thunder_icon = Image.open("day/248.png")
                            # Convert to a tkinter-compatible object
                            rain_thunder_icon_tk = ImageTk.PhotoImage(rain_thunder_icon)
                            # Create the label widget to store the image
                            rain_thunder_icon_label = tk.Label(master=root, image=rain_thunder_icon_tk, bg=("#C4DFAA"))
                            rain_thunder_icon_label.place(x=270, y=541)

                            # Store the image reference to prevent garbage collection
                            rain_thunder_icon_label.image = rain_thunder_icon_tk

                            return "weather images/thunder rain snow.png"

                    image_path = image_to_condition_matcher()
                    fade_image(image_label, image_path)

                    # we display the temperature dynamically everytime the user enters a location

                    def display_temperature():
                        # dictionary required data stored in temp
                        temp = data['current']['temp_c']
                        text = f"{temp}°C"
                        country = data['location']['country']
                        city = data['location']['name']
                        time = data['location']['localtime']
                        wind_speed2 = data['current']["wind_kph"]
                        humidity = data['current']['humidity']
                        feels_like = data['current']['feelslike_c']
                        chance_of_rain = data['forecast']['forecastday'][0]['hour'][0]['chance_of_rain']
                        # the frame to place our text in
                        # label behind the weather data frame
                        weather_data_label = customtkinter.CTkLabel(root, fg_color=("#F7FFE5"), bg_color=("#C4D7B2"), width=564, height=315)
                        weather_data_label.place(x=20, y=52)
                        # the frame to place our text in
                        weather_data_frame = customtkinter.CTkFrame(root, fg_color=("#C4DFAA"), height=300, width=550, corner_radius=5, bg_color=("#C4D7B2"))
                        weather_data_frame.place(x=27, y=60)

                        # the label to display the temperature which is overlayed ontop of the weather data frame
                        temperature_label = customtkinter.CTkLabel(master=weather_data_frame, text=str(text), font=("Arial", 75, "bold"), fg_color=("#C4DFAA"), bg_color=("#393646"), padx=4, pady=4, text_color=("#73A9AD"))
                        temperature_label.place(relx=0.5, rely=0.5, anchor="center")

                        # display the country in the frame
                        country_textbox = tk.Label(master=weather_data_frame, bg="#C4DFAA", font=("Arial", 25, "bold"), fg="#73A9AD", text=str(country))
                        country_textbox.place(relx=.5, rely=.15, anchor="center")

                        # display the city in the frame
                        city_textbox = tk.Label(master=weather_data_frame, bg="#C4DFAA", font=("Arial", 30, "bold"), fg="#73A9AD", text=str(city))
                        city_textbox.place(relx=.5, rely=.3, anchor="center")

                        # display the date and time
                        time_textbox = tk.Label(master=weather_data_frame, bg="#C4DFAA", font=("Arial", 15, "bold"), fg="#73A9AD", text=str(time))
                        time_textbox.place(relx=.5, rely=.7, anchor="center")

                        # the current conditions textbox overlaid on top of the frame
                        conditions_textbox = tk.Label(master=weather_data_frame, bg="#C4DFAA", font=("Arial", 15, "bold"), fg="#73A9AD")
                        conditions_textbox.place(relx=.5, rely=.8, anchor="center")

                        # windspeed textbox
                        wind_speed2 = tk.Label(master=weather_data_frame, bg="#C4DFAA", font=("Arial", 15, "bold"), fg="#73A9AD", text=str(f"Wind Speed: {wind_speed2} km/h"))
                        wind_speed2.place(relx=.5, rely=.9, anchor="center")

                        # humidity textbox
                        humidity_textbox = tk.Label(master=root, bg="#C4DFAA", font=("Arial", 15, "bold"), fg="#73A9AD",
                                                    text=str(f"Humidity: {humidity}"))
                        humidity_textbox.place(x=240, y=461)

                        # feels liket textbox
                        feels_like_textbox = tk.Label(master=root, bg="#C4DFAA", font=("Arial", 15, "bold"),
                                                      fg="#73A9AD",
                                                      text=str(f"Feels Like: {feels_like}°C"))
                        feels_like_textbox.place(x=215, y=491)

                        # feels like textbox
                        chance_of_rain_textbox = tk.Label(master=root, bg="#C4DFAA", font=("Arial", 15, "bold"),
                                                          fg="#73A9AD",
                                                          text=str(f"Chance of Rain: {chance_of_rain}%"))
                        chance_of_rain_textbox.place(x=208, y=521)

                        # dynamically update the textbox that displays current weather conditions
                        def update_textbox():
                            conditions_textbox.config(text=condition['text'])

                        # call the function
                        update_textbox()

                    display_temperature()

                    def show_back_forward_buttons():

                        # load in the arrow images
                        # back_button = Image.open('back_arrow.png')
                        forward_button = Image.open('forward_arrow.png')

                        # resize the arrow icons
                        icon_size = (32, 32)
                        forward_icon = forward_button.resize(icon_size)
                        forward_icon_tk = ImageTk.PhotoImage(forward_icon)

                        # buttons label
                        live_forward_button_label = customtkinter.CTkLabel(root, width=61, height=46,
                                                                           fg_color=("#F7FFE5"), text=" ",
                                                                           corner_radius=4, bg_color=("#C4DFAA"))
                        live_forward_button_label.place(x=520, y=747)

                        #second iteration of the progam logic loop as you cycle through it changes the city dynamically based on input
                        def big_brain():

                            print("Gulpadshah Khan is #1")
                            clear_screen()
                            draw_widgets()






                        # blit the buttons to screen
                        live_forward_button = customtkinter.CTkButton(root, image=forward_icon_tk, command=big_brain, text=" ", width=1, bg_color=("#C4DFAA"), corner_radius=4, fg_color=("#C4DFAA"))
                        live_forward_button.image = forward_icon_tk  # round 2 fight!
                        live_forward_button.place(x=523, y=750)

                        exit_program_label = customtkinter.CTkLabel(root, text=" ", bg_color=("#F7FFE5"), height=34, width=147)
                        exit_program_label.place(relx=.5, rely=.95, anchor="center")

                        exit_program = customtkinter.CTkButton(root, text="Exit", text_color=("#1F6E8C"), fg_color=("#C4DFAA"), bg_color=("#F7FFE5"), corner_radius=7, command=big_brain)
                        exit_program.place(relx=.5, rely=.95, anchor="center")
                    show_back_forward_buttons()  # call it



                #exit
                exit_program_label = customtkinter.CTkLabel(root, text=" ", bg_color=("#F7FFE5"), height=2, width=1)
                exit_program_label.place(x=250, y=750)

                exit_program = customtkinter.CTkButton(root, text="Exit", text_color=("#1F6E8C"), fg_color=("#C4DFAA"), bg_color=("#F7FFE5"), corner_radius=5, command=exiting_again)
                exit_program.place(x=251, y=750)
                # Load the initial image


                image = Image.open("weather images/base.png")
                image_size = image.size  # Store the size of the image
                photo = ImageTk.PhotoImage(image)

                # Create an image label
                image_label = tk.Label(root, image=photo)
                image_label.image = photo  # Keep a reference to prevent garbage collection
                image_label.pack()

                # when refresh weather city is pressed it runs the grab city function which handles the api request
                # and grabs the users chosen city and stores it in a variable
                # we can do multiple requests so long as they are not concurrent so if the user wants to look at another
                # city just create two buttons and we can split the app down the middle with the layout

                condition = dictionary['current']['condition']

                # buttons and labels

                users_city = customtkinter.CTkEntry(master=root, fg_color=("#73A9AD"),
                                                    placeholder_text="Please Enter Your City",
                                                    placeholder_text_color=("white"), text_color=("white"),
                                                    corner_radius=2)
                users_city.place(x=150, y=400)

                print_city_button = customtkinter.CTkButton(master=root, text="Check Weather", command=grab_city,
                                                            fg_color=("#73A9AD"), text_color=("white"))
                print_city_button.place(x=315, y=400)

######################## nested within ending ##########################################################



            # blit the buttons to screen
            dark_button_label = customtkinter.CTkLabel(master=multi_window_label, width=63, height=46, fg_color=("black"), text=" ", corner_radius=4, bg_color="black")
            dark_button_label.place(x=9, y=748)

            trend_day_back_button = customtkinter.CTkButton(master=multi_window_label, image=back_icon_tk, text=" ", width=1,bg_color="black", corner_radius=4, fg_color=("#1F6E8C"), command=when_trend_day_back_button_pressed)
            trend_day_back_button.place(x=14, y=751)
            trend_day_back_button.image = back_icon_tk

        trend_multi_day_back_button()




        #dictionary parsing required data
        country = data['location']['country']
        city = data['location']['name']
        temperature = data['current']['temp_c']
        wind_speed = data['current']["wind_kph"]
        local_time = data['location']['localtime']
        condition = data['current']['condition']
        forecast = data['forecast']['forecastday'] #grab the forecast



        #store the time string in current day variable
        current_day = local_time
        #convert the date string to a datetime object and get the weekday name
        weekday_name = calendar.day_name[datetime.datetime.strptime(current_day, '%Y-%m-%d %H:%M').date().weekday()]

        #converting dictionary entries to appropriate string for legibility and formatting reasons
        #weather conditions reformatted
        weather_condition = condition['text']


        city_and_country = (f"{city}, {country}")
        temperature_formatted = (f"{temperature} °C")
        wind_speed_formatted = (f"{wind_speed} km/h")

        #title bar for the page
        location_country_label = customtkinter.CTkLabel(root, height=40, width =580, bg_color=("#254055"), fg_color=("#1F6E8C"), text=city_and_country, corner_radius=10, font=("arial", 25) )
        location_country_label.place(x=12, y=8)

        #black_border_label
        black_border_label = customtkinter.CTkLabel(root, height=235, width=155,  fg_color=("black"))
        black_border_label.place(x=109, y=82)

        #label to display the local time and the label to encompass the other labels
        day_one_label = customtkinter.CTkLabel(root, height=220, width=147, fg_color=("#1F6E8C"),text=local_time, font=("Arial", 14, "bold"), corner_radius=10,bg_color=("black"))
        day_one_label.place(x=113, y=90)

        #week day name
        day_of_week_label = customtkinter.CTkLabel(master=day_one_label, text_color=("white"), fg_color=("#1F6E8C"), text=weekday_name, font=("Arial", 14, "bold"))
        day_of_week_label.place(relx=.35, rely=.32)

        #temperature
        day_one_temperature_label = customtkinter.CTkLabel(master=day_one_label,text_color=("white"), text=temperature_formatted, fg_color=("#1F6E8C"), font=("Arial", 19, "bold" ))
        day_one_temperature_label.place(relx=.5, rely=.1, anchor="center")

        #weather conditions
        day_one_weather_condition = customtkinter.CTkLabel(master=day_one_label, text_color=("white"), fg_color=("#1F6E8C"), text=weather_condition, font=("Arial", 14, "bold"))
        day_one_weather_condition.place(relx=.5, rely=.25, anchor="center")

        #wind speed
        day_one_wind_label = customtkinter.CTkLabel(master=day_one_label, text_color=("white"), fg_color=("#1F6E8C"), text=wind_speed_formatted, font=("Arial", 14, "bold"))
        day_one_wind_label.place(relx=.5, rely=.62, anchor="center")

        if condition['text'] == 'Clear':
            # Load the icon
            clear_icon = Image.open("day/113 _Copy.png")
            # Convert to a tkinter-compatible object
            clear_icon_tk = ImageTk.PhotoImage(clear_icon)
            # Create the label widget to store the image
            clear_icon_label = tk.Label(master=day_one_label, image=clear_icon_tk, bg=("#1F6E8C"))
            clear_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            clear_icon.image = clear_icon_tk

        elif condition['text'] == 'Sunny':
            # Load the icon
            sun_icon = Image.open("day/113.png")
            # Convert to a tkinter-compatible object
            sun_icon_tk = ImageTk.PhotoImage(sun_icon)
            # Create the label widget to store the image
            sun_icon_label = tk.Label(master=day_one_label, image=sun_icon_tk, bg=("#1F6E8C"))
            sun_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            sun_icon_label.image = sun_icon_tk





        elif condition['text'] == 'Partly cloudy':
            # Load the icon
            partly_icon = Image.open("day/116.png")
            # Convert to a tkinter-compatible object
            partly_icon_tk = ImageTk.PhotoImage(partly_icon)
            # Create the label widget to store the image
            partly_icon_label = tk.Label(master=day_one_label, image=partly_icon_tk, bg=("#1F6E8C"))
            partly_icon_label.place(relx=.25, rely=.7)
            # Store the image reference to prevent garbage collection
            partly_icon_label.image = partly_icon_tk

        elif condition['text'] == 'Overcast':
            # Load the icon
            overcast_icon = Image.open("day/119.png")
            # Convert to a tkinter-compatible object
            overcast_icon_tk = ImageTk.PhotoImage(overcast_icon)
            # Create the label widget to store the image
            overcast_icon_label = tk.Label(master=day_one_label, image=overcast_icon_tk, bg=("#1F6E8C"))
            overcast_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            overcast_icon_label.image = overcast_icon_tk


        elif condition['text'] == 'Mist':
            # Load the icon
            mist_icon = Image.open("day/248.png")
            # Convert to a tkinter-compatible object
            mist_icon_tk = ImageTk.PhotoImage(mist_icon)
            # Create the label widget to store the image
            mist_icon_label = tk.Label(master=day_one_label, image=mist_icon_tk, bg=("#1F6E8C"))
            mist_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            mist_icon_label.image = mist_icon_tk

        elif condition['text'] == "Patchy rain possible" or condition['text'] == "Patchy snow possible" or condition[
            'text'] == "Patchy sleet possible" or condition['text'] == "Patchy freezing drizzle possible":

            # Load the icon
            patchy_rain_icon = Image.open("day/317.png")
            # Convert to a tkinter-compatible object
            patchy_rain_icon_tk = ImageTk.PhotoImage(patchy_rain_icon)
            # Create the label widget to store the image
            patchy_rain_icon_label = tk.Label(master=day_one_label, image=patchy_rain_icon_tk, bg=("#1F6E8C"))
            patchy_rain_icon_label.place(relx=.25, rely=.7)
            # Store the image reference to prevent garbage collection
            patchy_rain_icon_label.image = patchy_rain_icon_tk

        elif condition['text'] == 'Thundery outbreaks possible':
            # Load the icon
            thundery_outbreaks_icon = Image.open("day/386.png")
            # Convert to a tkinter-compatible object
            thundery_outbreaks_icon_tk = ImageTk.PhotoImage(thundery_outbreaks_icon)
            # Create the label widget to store the image
            thundery_outbreaks_icon_label = tk.Label(master=day_one_label, image=thundery_outbreaks_icon_tk, bg=("#1F6E8C"))
            thundery_outbreaks_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            thundery_outbreaks_icon_label.image = thundery_outbreaks_icon_tk

        elif condition['text'] == 'Blowing snow':
            # Load the icon
            blowing_snow_icon = Image.open("day/326.png")
            # Convert to a tkinter-compatible object
            blowing_snow_icon_tk = ImageTk.PhotoImage(blowing_snow_icon)
            # Create the label widget to store the image
            blowing_snow_icon_label = tk.Label(master=day_one_label, image=blowing_snow_icon_tk, bg=("#1F6E8C"))
            blowing_snow_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            blowing_snow_icon_label.image = blowing_snow_icon_tk


        elif condition['text'] == 'Fog':
            # Load the icon
            fog_icon = Image.open("day/248.png")
            # Convert to a tkinter-compatible object
            fog_icon_tk = ImageTk.PhotoImage(fog_icon)
            # Create the label widget to store the image
            fog_icon_label = tk.Label(master=day_one_label, image=fog_icon_tk, bg=("#1F6E8C"))
            fog_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            fog_icon_label.image = fog_icon_tk

            # Store the image reference to prevent garbage collection
            fog_icon_label.image = fog_icon_tk

        elif condition['text'] == 'Freezing fog':
            # Load the icon
            freezing_fog_icon = Image.open("day/314.png")
            # Convert to a tkinter-compatible object
            freezing_fog_icon_tk = ImageTk.PhotoImage(freezing_fog_icon)
            # Create the label widget to store the image
            freezing_fog_icon_label = tk.Label(master=day_one_label, image=freezing_fog_icon_tk, bg=("#1F6E8C"))
            freezing_fog_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            freezing_fog_icon_label.image = freezing_fog_icon_tk

        elif condition['text'] == 'Patchy light drizzle' or condition['text'] == 'Light drizzle' or condition[
            'text'] == 'Patchy light rain' or condition['text'] == 'Light rain':
            # Load the icon
            patchy_drizzle_icon = Image.open("day/176.png")
            # Convert to a tkinter-compatible object
            patchy_drizzle_icon_tk = ImageTk.PhotoImage(patchy_drizzle_icon)
            # Create the label widget to store the image
            patchy_drizzle_icon_label = tk.Label(master=day_one_label, image=patchy_drizzle_icon_tk, bg=("#1F6E8C"))
            patchy_drizzle_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            patchy_drizzle_icon_label.image = patchy_drizzle_icon_tk


        elif condition['text'] == 'Light sleet' or condition['text'] == 'Light snow' or condition[
            'text'] == 'Patchy moderate snow' or condition['text'] == 'Moderate snow':
            # Load the icon
            blowing_snow_icon = Image.open("day/179.png")
            # Convert to a tkinter-compatible object
            blowing_snow_icon_tk = ImageTk.PhotoImage(blowing_snow_icon)
            # Create the label widget to store the image
            blowing_snow_icon_label = tk.Label(master=day_one_label, image=blowing_snow_icon_tk, bg=("#1F6E8C"))
            blowing_snow_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            blowing_snow_icon_label.image = blowing_snow_icon_tk

        elif condition['text'] == 'Light sleet' or condition['text'] == 'Light snow' or condition[
            'text'] == 'Patchy moderate snow' or condition['text'] == 'Moderate snow':
            # Load the icon
            sleet_icon = Image.open("day/326.png")
            # Convert to a tkinter-compatible object
            sleet_icon_tk = ImageTk.PhotoImage(sleet_icon)
            # Create the label widget to store the image
            sleet_icon_label = tk.Label(master=day_one_label, image=sleet_icon_tk, bg=("#1F6E8C"))
            sleet_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            sleet_icon_label.image = sleet_icon_tk

        elif condition['text'] == 'Heavy snow' or condition['text'] == 'Ice pellets':
            # Load the icon
            heavy_snow_icon = Image.open("day/338.png")
            # Convert to a tkinter-compatible object
            heavy_snow_icon_tk = ImageTk.PhotoImage(heavy_snow_icon)
            # Create the label widget to store the image
            heavy_snow_icon_label = tk.Label(master=day_one_label, image=heavy_snow_icon_tk, bg=("#1F6E8C"))
            heavy_snow_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            heavy_snow_icon_label.image = heavy_snow_icon_tk

        elif condition['text'] == 'Light rain shower' or condition['text'] == 'Moderate or heavy rain shower' or condition['text'] == 'Moderate rain':
            # Load the icon
            moderate_rain_icon = Image.open("day/308.png")
            # Convert to a tkinter-compatible object
            moderate_rain_icon_tk = ImageTk.PhotoImage(moderate_rain_icon)
            # Create the label widget to store the image
            moderate_rain_icon_label = tk.Label(master=day_one_label, image=moderate_rain_icon_tk, bg=("#1F6E8C"))
            moderate_rain_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            moderate_rain_icon_label.image = moderate_rain_icon_tk

        elif condition['text'] == 'Torrential rain shower' or condition['text'] == 'Light sleet showers' or condition[
            'text'] == 'Moderate or heavy sleet showers' or condition['text'] == 'Light snow showers' or condition[
            'text'] == 'Moderate or heavy snow showers':
            # Load the icon
            heavy_rain_icon = Image.open("day/308.png")
            # Convert to a tkinter-compatible object
            heavy_rain_icon_tk = ImageTk.PhotoImage(heavy_rain_icon)
            # Create the label widget to store the image
            heavy_rain_icon_label = tk.Label(master=day_one_label, image=heavy_rain_icon_tk, bg=("#1F6E8C"))
            heavy_rain_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            heavy_rain_icon_label.image = heavy_rain_icon_tk


        elif condition['text'] == 'Light showers of ice pellets' or condition[
            'text'] == 'Moderate or heavy showers of ice pellets':
            # Load the icon
            freezing_rain_icon = Image.open("day/320.png")
            # Convert to a tkinter-compatible object
            freezing_rain_icon_tk = ImageTk.PhotoImage(freezing_rain_icon)
            # Create the label widget to store the image
            freezing_rain_icon_label = tk.Label(master=day_one_label, image=freezing_rain_icon_tk, bg=("#1F6E8C"))
            freezing_rain_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            freezing_rain_icon_label.image = freezing_rain_icon_tk




        elif condition['text'] == 'Patchy light rain with thunder' or condition[
            'text'] == 'Moderate or heavy rain with thunder' or condition['text'] == 'Patchy light snow with thunder' or \
                condition['text'] == 'Moderate or heavy snow with thunder':
            # Load the icon
            rain_thunder_icon = Image.open("day/248.png")
            # Convert to a tkinter-compatible object
            rain_thunder_icon_tk = ImageTk.PhotoImage(rain_thunder_icon)
            # Create the label widget to store the image
            rain_thunder_icon_label = tk.Label(master=day_one_label, image=rain_thunder_icon_tk, bg=("#1F6E8C"))
            rain_thunder_icon_label.place(relx=.25, rely=.7)



########### day two label #########################


        second_day_condition = forecast[1]['day']['condition']  # access the condition for the day you need
        second_day_weather_condition = second_day_condition['text']
        temperature_second_day = data['forecast']['forecastday'][1]['day']['avgtemp_c']
        #formatting the above so it reads better
        second_day_temperature_formatted = (f"{temperature_second_day} °C")
        second_day_datetime = data['forecast']['forecastday'][1]['date'] #getting the local date and time
        #converting date time to find the specific day
        second_day_weekday = second_day_datetime
        second_day_weekday_name = calendar.day_name[datetime.datetime.strptime(second_day_weekday,'%Y-%m-%d').date().weekday()]

        #second day wind speed
        second_day_wind_speed = data['forecast']['forecastday'][1]['day']['maxwind_kph']
        second_day_formatted_windspeed = (f"{second_day_wind_speed} km/h")


        # black_border_label goes behind day two label to crate a border effect so that corner radius works
        day_two_black_border_label = customtkinter.CTkLabel(root, height=235, width=155, fg_color=("black"))
        day_two_black_border_label.place(x=288, y=82)

        # label to display the local time and the label to encompass the other labels
        day_two_label = customtkinter.CTkLabel(root, height=220, width=147, fg_color=("#1F6E8C"), text=second_day_datetime, font=("Arial", 14, "bold"), corner_radius=10, bg_color=("black"))
        day_two_label.place(x=292, y=90)

        # week day name
        day_of_week_label = customtkinter.CTkLabel(master=day_two_label, text_color=("white"), fg_color=("#1F6E8C"),text=second_day_weekday_name, font=("Arial", 14, "bold"))
        day_of_week_label.place(relx=.35, rely=.32)

        # temperature
        day_two_temperature_label = customtkinter.CTkLabel(master=day_two_label, text_color=("white"), text=second_day_temperature_formatted, fg_color=("#1F6E8C"), font=("Arial", 19, "bold"))
        day_two_temperature_label.place(relx=.5, rely=.1, anchor="center")

        # weather conditions
        day_two_weather_condition = customtkinter.CTkLabel(master=day_two_label, text_color=("white"),fg_color=("#1F6E8C"), text=second_day_weather_condition, font=("Arial", 14, "bold"))
        day_two_weather_condition.place(relx=.5, rely=.25, anchor="center")

        # wind speed
        day_two_wind_label = customtkinter.CTkLabel(master=day_two_label, text_color=("white"),fg_color=("#1F6E8C"), text=second_day_formatted_windspeed, font=("Arial", 14, "bold"))
        day_two_wind_label.place(relx=.5, rely=.62, anchor="center")

        #icons for day two#
        if second_day_condition['text'] == 'Sunny':
            # Load the icon
            sun_icon = Image.open("day/113.png")
            # Convert to a tkinter-compatible object
            sun_icon_tk = ImageTk.PhotoImage(sun_icon)
            # Create the label widget to store the image
            sun_icon_label = tk.Label(master=day_two_label, image=sun_icon_tk, bg=("#1F6E8C"))
            sun_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            sun_icon_label.image = sun_icon_tk

        elif second_day_condition['text'] == 'Clear':
            # Load the icon
            clear_icon = Image.open("day/113.png")
            # Convert to a tkinter-compatible object
            clear_icon_tk = ImageTk.PhotoImage(clear_icon)
            # Create the label widget to store the image
            clear_icon_label = tk.Label(master=day_two_label, image=clear_icon_tk, bg=("#1F6E8C"))
            clear_icon_label.place(relx=.25, rely=.7)
            # Store the image reference to prevent garbage collection
            clear_icon.image = clear_icon_tk

        elif second_day_condition['text'] == 'Partly cloudy':
            # Load the icon
            partly_icon = Image.open("day/116.png")
            # Convert to a tkinter-compatible object
            partly_icon_tk = ImageTk.PhotoImage(partly_icon)
            # Create the label widget to store the image
            partly_icon_label = tk.Label(master=day_two_label, image=partly_icon_tk, bg=("#1F6E8C"))
            partly_icon_label.place(relx=.25, rely=.7)
            # Store the image reference to prevent garbage collection
            partly_icon_label.image = partly_icon_tk

        elif second_day_condition['text'] == 'Overcast':
            # Load the icon
            overcast_icon = Image.open("day/119.png")
            # Convert to a tkinter-compatible object
            overcast_icon_tk = ImageTk.PhotoImage(overcast_icon)
            # Create the label widget to store the image
            overcast_icon_label = tk.Label(master=day_two_label, image=overcast_icon_tk, bg=("#1F6E8C"))
            overcast_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            overcast_icon_label.image = overcast_icon_tk


        elif second_day_condition['text'] == 'Mist':
            # Load the icon
            mist_icon = Image.open("day/248.png")
            # Convert to a tkinter-compatible object
            mist_icon_tk = ImageTk.PhotoImage(mist_icon)
            # Create the label widget to store the image
            mist_icon_label = tk.Label(master=day_two_label, image=mist_icon_tk, bg=("#1F6E8C"))
            mist_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            mist_icon_label.image = mist_icon_tk

        elif second_day_condition['text'] == "Patchy rain possible" or second_day_condition['text'] == "Patchy snow possible" or second_day_condition[
            'text'] == "Patchy sleet possible" or second_day_condition['text'] == "Patchy freezing drizzle possible":

            # Load the icon
            patchy_rain_icon = Image.open("day/317.png")
            # Convert to a tkinter-compatible object
            patchy_rain_icon_tk = ImageTk.PhotoImage(patchy_rain_icon)
            # Create the label widget to store the image
            patchy_rain_icon_label = tk.Label(master=day_two_label, image=patchy_rain_icon_tk, bg=("#1F6E8C"))
            patchy_rain_icon_label.place(relx=.25, rely=.7)
            # Store the image reference to prevent garbage collection
            patchy_rain_icon_label.image = patchy_rain_icon_tk

        elif second_day_condition['text'] == 'Thundery outbreaks possible':
            # Load the icon
            thundery_outbreaks_icon = Image.open("day/386.png")
            # Convert to a tkinter-compatible object
            thundery_outbreaks_icon_tk = ImageTk.PhotoImage(thundery_outbreaks_icon)
            # Create the label widget to store the image
            thundery_outbreaks_icon_label = tk.Label(master=day_two_label, image=thundery_outbreaks_icon_tk, bg=("#1F6E8C"))
            thundery_outbreaks_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            thundery_outbreaks_icon_label.image = thundery_outbreaks_icon_tk

        elif second_day_condition['text'] == 'Blowing snow':
            # Load the icon
            blowing_snow_icon = Image.open("day/326.png")
            # Convert to a tkinter-compatible object
            blowing_snow_icon_tk = ImageTk.PhotoImage(blowing_snow_icon)
            # Create the label widget to store the image
            blowing_snow_icon_label = tk.Label(master=day_two_label, image=blowing_snow_icon_tk, bg=("#1F6E8C"))
            blowing_snow_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            blowing_snow_icon_label.image = blowing_snow_icon_tk


        elif second_day_condition['text'] == 'Fog':
            # Load the icon
            fog_icon = Image.open("day/248.png")
            # Convert to a tkinter-compatible object
            fog_icon_tk = ImageTk.PhotoImage(fog_icon)
            # Create the label widget to store the image
            fog_icon_label = tk.Label(master=day_two_label, image=fog_icon_tk, bg=("#1F6E8C"))
            fog_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            fog_icon_label.image = fog_icon_tk

            # Store the image reference to prevent garbage collection
            fog_icon_label.image = fog_icon_tk

        elif second_day_condition['text'] == 'Freezing fog':
            # Load the icon
            freezing_fog_icon = Image.open("day/314.png")
            # Convert to a tkinter-compatible object
            freezing_fog_icon_tk = ImageTk.PhotoImage(freezing_fog_icon)
            # Create the label widget to store the image
            freezing_fog_icon_label = tk.Label(master=day_two_label, image=freezing_fog_icon_tk, bg=("#1F6E8C"))
            freezing_fog_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            freezing_fog_icon_label.image = freezing_fog_icon_tk

        elif second_day_condition['text'] == 'Patchy light drizzle' or second_day_condition['text'] == 'Light drizzle' or second_day_condition[
            'text'] == 'Patchy light rain' or second_day_condition['text'] == 'Light rain':
            # Load the icon
            patchy_drizzle_icon = Image.open("day/176.png")
            # Convert to a tkinter-compatible object
            patchy_drizzle_icon_tk = ImageTk.PhotoImage(patchy_drizzle_icon)
            # Create the label widget to store the image
            patchy_drizzle_icon_label = tk.Label(master=day_two_label, image=patchy_drizzle_icon_tk, bg=("#1F6E8C"))
            patchy_drizzle_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            patchy_drizzle_icon_label.image = patchy_drizzle_icon_tk


        elif second_day_condition['text'] == 'Light sleet' or second_day_condition['text'] == 'Light snow' or second_day_condition[
            'text'] == 'Patchy moderate snow' or second_day_condition['text'] == 'Moderate snow':
            # Load the icon
            blowing_snow_icon = Image.open("day/179.png")
            # Convert to a tkinter-compatible object
            blowing_snow_icon_tk = ImageTk.PhotoImage(blowing_snow_icon)
            # Create the label widget to store the image
            blowing_snow_icon_label = tk.Label(master=day_two_label, image=blowing_snow_icon_tk, bg=("#1F6E8C"))
            blowing_snow_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            blowing_snow_icon_label.image = blowing_snow_icon_tk

        elif second_day_condition['text'] == 'Light sleet' or second_day_condition['text'] == 'Light snow' or second_day_condition[
            'text'] == 'Patchy moderate snow' or second_day_condition['text'] == 'Moderate snow':
            # Load the icon
            sleet_icon = Image.open("day/326.png")
            # Convert to a tkinter-compatible object
            sleet_icon_tk = ImageTk.PhotoImage(sleet_icon)
            # Create the label widget to store the image
            sleet_icon_label = tk.Label(master=day_two_label, image=sleet_icon_tk, bg=("#1F6E8C"))
            sleet_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            sleet_icon_label.image = sleet_icon_tk

        elif second_day_condition['text'] == 'Heavy snow' or second_day_condition['text'] == 'Ice pellets':
            # Load the icon
            heavy_snow_icon = Image.open("day/338.png")
            # Convert to a tkinter-compatible object
            heavy_snow_icon_tk = ImageTk.PhotoImage(heavy_snow_icon)
            # Create the label widget to store the image
            heavy_snow_icon_label = tk.Label(master=day_two_label, image=heavy_snow_icon_tk, bg=("#1F6E8C"))
            heavy_snow_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            heavy_snow_icon_label.image = heavy_snow_icon_tk

        elif second_day_condition['text'] == 'Light rain shower' or second_day_condition['text'] == 'Moderate or heavy rain shower' or second_day_condition['text'] == 'Moderate rain' :
            # Load the icon
            moderate_rain_icon = Image.open("day/308.png")
            # Convert to a tkinter-compatible object
            moderate_rain_icon_tk = ImageTk.PhotoImage(moderate_rain_icon)
            # Create the label widget to store the image
            moderate_rain_icon_label = tk.Label(master=day_two_label, image=moderate_rain_icon_tk, bg=("#1F6E8C"))
            moderate_rain_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            moderate_rain_icon_label.image = moderate_rain_icon_tk

        elif second_day_condition['text'] == 'Torrential rain shower' or second_day_condition['text'] == 'Light sleet showers' or second_day_condition[
            'text'] == 'Moderate or heavy sleet showers' or second_day_condition['text'] == 'Light snow showers' or second_day_condition[
            'text'] == 'Moderate or heavy snow showers':
            # Load the icon
            heavy_rain_icon = Image.open("day/308.png")
            # Convert to a tkinter-compatible object
            heavy_rain_icon_tk = ImageTk.PhotoImage(heavy_rain_icon)
            # Create the label widget to store the image
            heavy_rain_icon_label = tk.Label(master=day_two_label, image=heavy_rain_icon_tk, bg=("#1F6E8C"))
            heavy_rain_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            heavy_rain_icon_label.image = heavy_rain_icon_tk


        elif second_day_condition['text'] == 'Light showers of ice pellets' or second_day_condition[
            'text'] == 'Moderate or heavy showers of ice pellets':
            # Load the icon
            freezing_rain_icon = Image.open("day/320.png")
            # Convert to a tkinter-compatible object
            freezing_rain_icon_tk = ImageTk.PhotoImage(freezing_rain_icon)
            # Create the label widget to store the image
            freezing_rain_icon_label = tk.Label(master=day_two_label, image=freezing_rain_icon_tk, bg=("#1F6E8C"))
            freezing_rain_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            freezing_rain_icon_label.image = freezing_rain_icon_tk




        elif second_day_condition['text'] == 'Patchy light rain with thunder' or second_day_condition[
            'text'] == 'Moderate or heavy rain with thunder' or second_day_condition['text'] == 'Patchy light snow with thunder' or \
                second_day_condition['text'] == 'Moderate or heavy snow with thunder':
            # Load the icon
            rain_thunder_icon = Image.open("day/248.png")
            # Convert to a tkinter-compatible object
            rain_thunder_icon_tk = ImageTk.PhotoImage(rain_thunder_icon)
            # Create the label widget to store the image
            rain_thunder_icon_label = tk.Label(master=day_two_label, image=rain_thunder_icon_tk, bg=("#1F6E8C"))
            rain_thunder_icon_label.place(relx=.25, rely=.7)


################## third day weather label #################

        third_day_condition = forecast[2]['day']['condition']  # access the third days condition
        third_day_weather_condition = third_day_condition['text']
        temperature_third_day = data['forecast']['forecastday'][2]['day']['avgtemp_c']
        # formatting the above so it reads better
        third_day_temperature_formatted = (f"{temperature_third_day} °C")
        third_day_datetime = data['forecast']['forecastday'][2]['date']  # getting the local date and time
        # converting date time to find the specific day
        third_day_weekday = third_day_datetime
        third_day_weekday_name = calendar.day_name[
            datetime.datetime.strptime(third_day_weekday, '%Y-%m-%d').date().weekday()]

        # second day wind speed
        third_day_wind_speed = data['forecast']['forecastday'][2]['day']['maxwind_kph']
        third_day_formatted_windspeed = (f"{third_day_wind_speed} km/h")

        # black_border_label goes behind day two label to crate a border effect so that corner radius works
        third_day_black_border_label = customtkinter.CTkLabel(root, height=235, width=155, fg_color=("black"))
        third_day_black_border_label.place(x=110, y=443)

        # label to display the local time and the label to encompass the other labels
        day_three_label = customtkinter.CTkLabel(root, height=220, width=145, fg_color=("#1F6E8C"), text=third_day_datetime, font=("Arial", 14, "bold"), corner_radius=10,bg_color=("black"))
        day_three_label.place(x=116, y=450)

        # week day name
        third_day_of_week_label = customtkinter.CTkLabel(master=day_three_label, text_color=("white"), fg_color=("#1F6E8C"), text=third_day_weekday_name, font=("Arial", 14, "bold"))
        third_day_of_week_label.place(relx=.35, rely=.32)

        # temperature
        day_three_temperature_label = customtkinter.CTkLabel(master=day_three_label, text_color=("white"), text=third_day_temperature_formatted, fg_color=("#1F6E8C"), font=("Arial", 19, "bold"))
        day_three_temperature_label.place(relx=.5, rely=.1, anchor="center")

        # weather conditions
        day_three_weather_condition = customtkinter.CTkLabel(master=day_three_label, text_color=("white"), fg_color=("#1F6E8C"), text=third_day_weather_condition, font=("Arial", 14, "bold"))
        day_three_weather_condition.place(relx=.5, rely=.25, anchor="center")

        # wind speed
        day_three_wind_label = customtkinter.CTkLabel(master=day_three_label, text_color=("white"), fg_color=("#1F6E8C"), text=third_day_formatted_windspeed, font=("Arial", 14, "bold"))
        day_three_wind_label.place(relx=.5, rely=.62, anchor="center")


        if third_day_condition['text'] == 'Sunny':
            # Load the icon
            sun_icon = Image.open("day/113.png")
            # Convert to a tkinter-compatible object
            sun_icon_tk = ImageTk.PhotoImage(sun_icon)
            # Create the label widget to store the image
            sun_icon_label = tk.Label(master=day_three_label, image=sun_icon_tk, bg=("#1F6E8C"))
            sun_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            sun_icon_label.image = sun_icon_tk

        elif third_day_condition['text'] == 'Clear':
            # Load the icon
            clear_icon = Image.open("day/113.png")
            # Convert to a tkinter-compatible object
            clear_icon_tk = ImageTk.PhotoImage(clear_icon)
            # Create the label widget to store the image
            clear_icon_label = tk.Label(master=day_three_label, image=clear_icon_tk, bg=("#1F6E8C"))
            clear_icon_label.place(relx=.25, rely=.7)
            # Store the image reference to prevent garbage collection
            clear_icon.image = clear_icon_tk

        elif third_day_condition['text'] == 'Partly cloudy':
            # Load the icon
            partly_icon = Image.open("day/116.png")
            # Convert to a tkinter-compatible object
            partly_icon_tk = ImageTk.PhotoImage(partly_icon)
            # Create the label widget to store the image
            partly_icon_label = tk.Label(master=day_three_label, image=partly_icon_tk, bg=("#1F6E8C"))
            partly_icon_label.place(relx=.25, rely=.7)
            # Store the image reference to prevent garbage collection
            partly_icon_label.image = partly_icon_tk

        elif third_day_condition['text'] == 'Overcast':
            # Load the icon
            overcast_icon = Image.open("day/119.png")
            # Convert to a tkinter-compatible object
            overcast_icon_tk = ImageTk.PhotoImage(overcast_icon)
            # Create the label widget to store the image
            overcast_icon_label = tk.Label(master=day_three_label, image=overcast_icon_tk, bg=("#1F6E8C"))
            overcast_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            overcast_icon_label.image = overcast_icon_tk


        elif third_day_condition['text'] == 'Mist':
            # Load the icon
            mist_icon = Image.open("day/248.png")
            # Convert to a tkinter-compatible object
            mist_icon_tk = ImageTk.PhotoImage(mist_icon)
            # Create the label widget to store the image
            mist_icon_label = tk.Label(master=day_three_label, image=mist_icon_tk, bg=("#1F6E8C"))
            mist_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            mist_icon_label.image = mist_icon_tk

        elif third_day_condition['text'] == "Patchy rain possible" or third_day_condition['text'] == "Patchy snow possible" or third_day_condition[
            'text'] == "Patchy sleet possible" or third_day_condition['text'] == "Patchy freezing drizzle possible":

            # Load the icon
            patchy_rain_icon = Image.open("day/317.png")
            # Convert to a tkinter-compatible object
            patchy_rain_icon_tk = ImageTk.PhotoImage(patchy_rain_icon)
            # Create the label widget to store the image
            patchy_rain_icon_label = tk.Label(master=day_three_label, image=patchy_rain_icon_tk, bg=("#1F6E8C"))
            patchy_rain_icon_label.place(relx=.25, rely=.7)
            # Store the image reference to prevent garbage collection
            patchy_rain_icon_label.image = patchy_rain_icon_tk

        elif third_day_condition['text'] == 'Thundery outbreaks possible':
            # Load the icon
            thundery_outbreaks_icon = Image.open("day/386.png")
            # Convert to a tkinter-compatible object
            thundery_outbreaks_icon_tk = ImageTk.PhotoImage(thundery_outbreaks_icon)
            # Create the label widget to store the image
            thundery_outbreaks_icon_label = tk.Label(master=day_three_label, image=thundery_outbreaks_icon_tk, bg=("#1F6E8C"))
            thundery_outbreaks_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            thundery_outbreaks_icon_label.image = thundery_outbreaks_icon_tk

        elif third_day_condition['text'] == 'Blowing snow':
            # Load the icon
            blowing_snow_icon = Image.open("day/326.png")
            # Convert to a tkinter-compatible object
            blowing_snow_icon_tk = ImageTk.PhotoImage(blowing_snow_icon)
            # Create the label widget to store the image
            blowing_snow_icon_label = tk.Label(master=day_three_label, image=blowing_snow_icon_tk, bg=("#1F6E8C"))
            blowing_snow_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            blowing_snow_icon_label.image = blowing_snow_icon_tk


        elif third_day_condition['text'] == 'Fog':
            # Load the icon
            fog_icon = Image.open("day/248.png")
            # Convert to a tkinter-compatible object
            fog_icon_tk = ImageTk.PhotoImage(fog_icon)
            # Create the label widget to store the image
            fog_icon_label = tk.Label(master=day_three_label, image=fog_icon_tk, bg=("#1F6E8C"))
            fog_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            fog_icon_label.image = fog_icon_tk

            # Store the image reference to prevent garbage collection
            fog_icon_label.image = fog_icon_tk

        elif third_day_condition['text'] == 'Freezing fog':
            # Load the icon
            freezing_fog_icon = Image.open("day/314.png")
            # Convert to a tkinter-compatible object
            freezing_fog_icon_tk = ImageTk.PhotoImage(freezing_fog_icon)
            # Create the label widget to store the image
            freezing_fog_icon_label = tk.Label(master=day_three_label, image=freezing_fog_icon_tk, bg=("#1F6E8C"))
            freezing_fog_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            freezing_fog_icon_label.image = freezing_fog_icon_tk

        elif third_day_condition['text'] == 'Patchy light drizzle' or third_day_condition['text'] == 'Light drizzle' or third_day_condition[
            'text'] == 'Patchy light rain' or third_day_condition['text'] == 'Light rain':
            # Load the icon
            patchy_drizzle_icon = Image.open("day/176.png")
            # Convert to a tkinter-compatible object
            patchy_drizzle_icon_tk = ImageTk.PhotoImage(patchy_drizzle_icon)
            # Create the label widget to store the image
            patchy_drizzle_icon_label = tk.Label(master=day_three_label, image=patchy_drizzle_icon_tk, bg=("#1F6E8C"))
            patchy_drizzle_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            patchy_drizzle_icon_label.image = patchy_drizzle_icon_tk


        elif third_day_condition['text'] == 'Light sleet' or third_day_condition['text'] == 'Light snow' or third_day_condition[
            'text'] == 'Patchy moderate snow' or third_day_condition['text'] == 'Moderate snow':
            # Load the icon
            blowing_snow_icon = Image.open("day/179.png")
            # Convert to a tkinter-compatible object
            blowing_snow_icon_tk = ImageTk.PhotoImage(blowing_snow_icon)
            # Create the label widget to store the image
            blowing_snow_icon_label = tk.Label(master=day_three_label, image=blowing_snow_icon_tk, bg=("#1F6E8C"))
            blowing_snow_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            blowing_snow_icon_label.image = blowing_snow_icon_tk

        elif third_day_condition['text'] == 'Light sleet' or third_day_condition['text'] == 'Light snow' or third_day_condition[
            'text'] == 'Patchy moderate snow' or condition['text'] == 'Moderate snow':
            # Load the icon
            sleet_icon = Image.open("day/326.png")
            # Convert to a tkinter-compatible object
            sleet_icon_tk = ImageTk.PhotoImage(sleet_icon)
            # Create the label widget to store the image
            sleet_icon_label = tk.Label(master=day_three_label, image=sleet_icon_tk, bg=("#1F6E8C"))
            sleet_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            sleet_icon_label.image = sleet_icon_tk

        elif third_day_condition['text'] == 'Heavy snow' or third_day_condition['text'] == 'Ice pellets':
            # Load the icon
            heavy_snow_icon = Image.open("day/338.png")
            # Convert to a tkinter-compatible object
            heavy_snow_icon_tk = ImageTk.PhotoImage(heavy_snow_icon)
            # Create the label widget to store the image
            heavy_snow_icon_label = tk.Label(master=day_three_label, image=heavy_snow_icon_tk, bg=("#1F6E8C"))
            heavy_snow_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            heavy_snow_icon_label.image = heavy_snow_icon_tk

        elif third_day_condition['text'] == 'Light rain shower' or third_day_condition['text'] == 'Moderate or heavy rain shower' or third_day_condition['text'] == 'Moderate rain':
            # Load the icon
            moderate_rain_icon = Image.open("day/308.png")
            # Convert to a tkinter-compatible object
            moderate_rain_icon_tk = ImageTk.PhotoImage(moderate_rain_icon)
            # Create the label widget to store the image
            moderate_rain_icon_label = tk.Label(master=day_three_label, image=moderate_rain_icon_tk, bg=("#1F6E8C"))
            moderate_rain_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            moderate_rain_icon_label.image = moderate_rain_icon_tk

        elif third_day_condition['text'] == 'Torrential rain shower' or third_day_condition['text'] == 'Light sleet showers' or third_day_condition[
            'text'] == 'Moderate or heavy sleet showers' or third_day_condition['text'] == 'Light snow showers' or third_day_condition[
            'text'] == 'Moderate or heavy snow showers':
            # Load the icon
            heavy_rain_icon = Image.open("day/308.png")
            # Convert to a tkinter-compatible object
            heavy_rain_icon_tk = ImageTk.PhotoImage(heavy_rain_icon)
            # Create the label widget to store the image
            heavy_rain_icon_label = tk.Label(master=day_three_label, image=heavy_rain_icon_tk, bg=("#1F6E8C"))
            heavy_rain_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            heavy_rain_icon_label.image = heavy_rain_icon_tk


        elif third_day_condition['text'] == 'Light showers of ice pellets' or third_day_condition[
            'text'] == 'Moderate or heavy showers of ice pellets':
            # Load the icon
            freezing_rain_icon = Image.open("day/320.png")
            # Convert to a tkinter-compatible object
            freezing_rain_icon_tk = ImageTk.PhotoImage(freezing_rain_icon)
            # Create the label widget to store the image
            freezing_rain_icon_label = tk.Label(master=day_three_label, image=freezing_rain_icon_tk, bg=("#1F6E8C"))
            freezing_rain_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            freezing_rain_icon_label.image = freezing_rain_icon_tk




        elif third_day_condition['text'] == 'Patchy light rain with thunder' or third_day_condition[
            'text'] == 'Moderate or heavy rain with thunder' or third_day_condition['text'] == 'Patchy light snow with thunder' or \
                third_day_condition['text'] == 'Moderate or heavy snow with thunder':
            # Load the icon
            rain_thunder_icon = Image.open("day/248.png")
            # Convert to a tkinter-compatible object
            rain_thunder_icon_tk = ImageTk.PhotoImage(rain_thunder_icon)
            # Create the label widget to store the image
            rain_thunder_icon_label = tk.Label(master=day_three_label, image=rain_thunder_icon_tk, bg=("#1F6E8C"))
            rain_thunder_icon_label.place(relx=.25, rely=.7)

            ################## fourth day weather label #################

        fourth_day_condition = forecast[3]['day']['condition']  # access the third days condition
        fourth_day_weather_condition = fourth_day_condition['text']
        temperature_fourth_day = data['forecast']['forecastday'][3]['day']['avgtemp_c']
        # formatting the above so it reads better
        fourth_day_temperature_formatted = (f"{temperature_fourth_day} °C")
        fourth_day_datetime = data['forecast']['forecastday'][3]['date']  # getting the local date and time
        # converting date time to find the specific day
        fourth_day_weekday = fourth_day_datetime
        fourth_day_weekday_name = calendar.day_name[
            datetime.datetime.strptime(fourth_day_weekday, '%Y-%m-%d').date().weekday()]

        # fourth day wind speed
        fourth_day_wind_speed = data['forecast']['forecastday'][3]['day']['maxwind_kph']
        fourth_day_formatted_windspeed = (f"{fourth_day_wind_speed} km/h")

        # black_border_label goes behind day two label to crate a border effect so that corner radius works
        fourth_day_black_border_label = customtkinter.CTkLabel(root, height=235, width=155, fg_color=("black"))
        fourth_day_black_border_label.place(x=289, y=443)

        # label to display the local time and the label to encompass the other labels
        day_four_label = customtkinter.CTkLabel(root, height=220, width=145, fg_color=("#1F6E8C"), text=fourth_day_datetime, font=("Arial", 14, "bold"), corner_radius=10, bg_color=("black"))
        day_four_label.place(x=294, y=450)

        # week day name
        fourth_day_of_week_label = customtkinter.CTkLabel(master=day_four_label, text_color=("white"), fg_color=("#1F6E8C"), text=fourth_day_weekday_name,  font=("Arial", 14, "bold"))
        fourth_day_of_week_label.place(relx=.35, rely=.32)

        # temperature
        day_four_temperature_label = customtkinter.CTkLabel(master=day_four_label, text_color=("white"), text=fourth_day_temperature_formatted, fg_color=("#1F6E8C"), font=("Arial", 19, "bold"))
        day_four_temperature_label.place(relx=.5, rely=.1, anchor="center")

        # weather conditions
        day_four_weather_condition = customtkinter.CTkLabel(master=day_four_label, text_color=("white"), fg_color=("#1F6E8C"), text=fourth_day_weather_condition, font=("Arial", 14, "bold"))
        day_four_weather_condition.place(relx=.5, rely=.25, anchor="center")

        # wind speed
        day_four_wind_label = customtkinter.CTkLabel(master=day_four_label, text_color=("white"), fg_color=("#1F6E8C"), text=fourth_day_formatted_windspeed, font=("Arial", 14, "bold"))
        day_four_wind_label.place(relx=.5, rely=.62, anchor="center")

        if fourth_day_condition['text'] == 'Sunny':
            # Load the icon
            sun_icon = Image.open("day/113.png")
            # Convert to a tkinter-compatible object
            sun_icon_tk = ImageTk.PhotoImage(sun_icon)
            # Create the label widget to store the image
            sun_icon_label = tk.Label(master=day_four_label, image=sun_icon_tk, bg=("#1F6E8C"))
            sun_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            sun_icon_label.image = sun_icon_tk

        elif fourth_day_condition['text'] == 'Clear':
            # Load the icon
            clear_icon = Image.open("day/113.png")
            # Convert to a tkinter-compatible object
            clear_icon_tk = ImageTk.PhotoImage(clear_icon)
            # Create the label widget to store the image
            clear_icon_label = tk.Label(master=day_four_label, image=clear_icon_tk, bg=("#1F6E8C"))
            clear_icon_label.place(relx=.25, rely=.7)
            # Store the image reference to prevent garbage collection
            clear_icon.image = clear_icon_tk

        elif fourth_day_condition['text'] == 'Partly cloudy':
            # Load the icon
            partly_icon = Image.open("day/116.png")
            # Convert to a tkinter-compatible object
            partly_icon_tk = ImageTk.PhotoImage(partly_icon)
            # Create the label widget to store the image
            partly_icon_label = tk.Label(master=day_four_label, image=partly_icon_tk, bg=("#1F6E8C"))
            partly_icon_label.place(relx=.25, rely=.7)
            # Store the image reference to prevent garbage collection
            partly_icon_label.image = partly_icon_tk

        elif fourth_day_condition['text'] == 'Overcast':
            # Load the icon
            overcast_icon = Image.open("day/119.png")
            # Convert to a tkinter-compatible object
            overcast_icon_tk = ImageTk.PhotoImage(overcast_icon)
            # Create the label widget to store the image
            overcast_icon_label = tk.Label(master=day_four_label, image=overcast_icon_tk, bg=("#1F6E8C"))
            overcast_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            overcast_icon_label.image = overcast_icon_tk


        elif fourth_day_condition['text'] == 'Mist':
            # Load the icon
            mist_icon = Image.open("day/248.png")
            # Convert to a tkinter-compatible object
            mist_icon_tk = ImageTk.PhotoImage(mist_icon)
            # Create the label widget to store the image
            mist_icon_label = tk.Label(master=day_four_label, image=mist_icon_tk, bg=("#1F6E8C"))
            mist_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            mist_icon_label.image = mist_icon_tk

        elif fourth_day_condition['text'] == "Patchy rain possible" or fourth_day_condition['text'] == "Patchy snow possible" or fourth_day_condition[
            'text'] == "Patchy sleet possible" or fourth_day_condition['text'] == "Patchy freezing drizzle possible":

            # Load the icon
            patchy_rain_icon = Image.open("day/317.png")
            # Convert to a tkinter-compatible object
            patchy_rain_icon_tk = ImageTk.PhotoImage(patchy_rain_icon)
            # Create the label widget to store the image
            patchy_rain_icon_label = tk.Label(master=day_four_label, image=patchy_rain_icon_tk, bg=("#1F6E8C"))
            patchy_rain_icon_label.place(relx=.25, rely=.7)
            # Store the image reference to prevent garbage collection
            patchy_rain_icon_label.image = patchy_rain_icon_tk

        elif fourth_day_condition['text'] == 'Thundery outbreaks possible':
            # Load the icon
            thundery_outbreaks_icon = Image.open("day/386.png")
            # Convert to a tkinter-compatible object
            thundery_outbreaks_icon_tk = ImageTk.PhotoImage(thundery_outbreaks_icon)
            # Create the label widget to store the image
            thundery_outbreaks_icon_label = tk.Label(master=day_four_label, image=thundery_outbreaks_icon_tk, bg=("#1F6E8C"))
            thundery_outbreaks_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            thundery_outbreaks_icon_label.image = thundery_outbreaks_icon_tk

        elif fourth_day_condition['text'] == 'Blowing snow':
            # Load the icon
            blowing_snow_icon = Image.open("day/326.png")
            # Convert to a tkinter-compatible object
            blowing_snow_icon_tk = ImageTk.PhotoImage(blowing_snow_icon)
            # Create the label widget to store the image
            blowing_snow_icon_label = tk.Label(master=day_four_label, image=blowing_snow_icon_tk, bg=("#1F6E8C"))
            blowing_snow_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            blowing_snow_icon_label.image = blowing_snow_icon_tk


        elif fourth_day_condition['text'] == 'Fog':
            # Load the icon
            fog_icon = Image.open("day/248.png")
            # Convert to a tkinter-compatible object
            fog_icon_tk = ImageTk.PhotoImage(fog_icon)
            # Create the label widget to store the image
            fog_icon_label = tk.Label(master=day_four_label, image=fog_icon_tk, bg=("#1F6E8C"))
            fog_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            fog_icon_label.image = fog_icon_tk

            # Store the image reference to prevent garbage collection
            fog_icon_label.image = fog_icon_tk

        elif fourth_day_condition['text'] == 'Freezing fog':
            # Load the icon
            freezing_fog_icon = Image.open("day/314.png")
            # Convert to a tkinter-compatible object
            freezing_fog_icon_tk = ImageTk.PhotoImage(freezing_fog_icon)
            # Create the label widget to store the image
            freezing_fog_icon_label = tk.Label(master=day_four_label, image=freezing_fog_icon_tk, bg=("#1F6E8C"))
            freezing_fog_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            freezing_fog_icon_label.image = freezing_fog_icon_tk

        elif fourth_day_condition['text'] == 'Patchy light drizzle' or fourth_day_condition['text'] == 'Light drizzle' or fourth_day_condition[
            'text'] == 'Patchy light rain' or fourth_day_condition['text'] == 'Light rain':
            # Load the icon
            patchy_drizzle_icon = Image.open("day/176.png")
            # Convert to a tkinter-compatible object
            patchy_drizzle_icon_tk = ImageTk.PhotoImage(patchy_drizzle_icon)
            # Create the label widget to store the image
            patchy_drizzle_icon_label = tk.Label(master=day_four_label, image=patchy_drizzle_icon_tk, bg=("#1F6E8C"))
            patchy_drizzle_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            patchy_drizzle_icon_label.image = patchy_drizzle_icon_tk


        elif fourth_day_condition['text'] == 'Light sleet' or fourth_day_condition['text'] == 'Light snow' or fourth_day_condition[
            'text'] == 'Patchy moderate snow' or fourth_day_condition['text'] == 'Moderate snow':
            # Load the icon
            blowing_snow_icon = Image.open("day/179.png")
            # Convert to a tkinter-compatible object
            blowing_snow_icon_tk = ImageTk.PhotoImage(blowing_snow_icon)
            # Create the label widget to store the image
            blowing_snow_icon_label = tk.Label(master=day_four_label, image=blowing_snow_icon_tk, bg=("#1F6E8C"))
            blowing_snow_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            blowing_snow_icon_label.image = blowing_snow_icon_tk

        elif fourth_day_condition['text'] == 'Light sleet' or fourth_day_condition['text'] == 'Light snow' or fourth_day_condition[
            'text'] == 'Patchy moderate snow' or fourth_day_condition['text'] == 'Moderate snow':
            # Load the icon
            sleet_icon = Image.open("day/326.png")
            # Convert to a tkinter-compatible object
            sleet_icon_tk = ImageTk.PhotoImage(sleet_icon)
            # Create the label widget to store the image
            sleet_icon_label = tk.Label(master=day_four_label, image=sleet_icon_tk, bg=("#1F6E8C"))
            sleet_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            sleet_icon_label.image = sleet_icon_tk

        elif fourth_day_condition['text'] == 'Heavy snow' or fourth_day_condition['text'] == 'Ice pellets':
            # Load the icon
            heavy_snow_icon = Image.open("day/338.png")
            # Convert to a tkinter-compatible object
            heavy_snow_icon_tk = ImageTk.PhotoImage(heavy_snow_icon)
            # Create the label widget to store the image
            heavy_snow_icon_label = tk.Label(master=day_four_label, image=heavy_snow_icon_tk, bg=("#1F6E8C"))
            heavy_snow_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            heavy_snow_icon_label.image = heavy_snow_icon_tk

        elif fourth_day_condition['text'] == 'Light rain shower' or fourth_day_condition['text'] == 'Moderate or heavy rain shower' or fourth_day_condition['text'] == 'Moderate rain':
            # Load the icon
            moderate_rain_icon = Image.open("day/308.png")
            # Convert to a tkinter-compatible object
            moderate_rain_icon_tk = ImageTk.PhotoImage(moderate_rain_icon)
            # Create the label widget to store the image
            moderate_rain_icon_label = tk.Label(master=day_four_label, image=moderate_rain_icon_tk, bg=("#1F6E8C"))
            moderate_rain_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            moderate_rain_icon_label.image = moderate_rain_icon_tk

        elif fourth_day_condition['text'] == 'Torrential rain shower' or fourth_day_condition['text'] == 'Light sleet showers' or fourth_day_condition[
            'text'] == 'Moderate or heavy sleet showers' or fourth_day_condition['text'] == 'Light snow showers' or fourth_day_condition[
            'text'] == 'Moderate or heavy snow showers':
            # Load the icon
            heavy_rain_icon = Image.open("day/308.png")
            # Convert to a tkinter-compatible object
            heavy_rain_icon_tk = ImageTk.PhotoImage(heavy_rain_icon)
            # Create the label widget to store the image
            heavy_rain_icon_label = tk.Label(master=day_four_label, image=heavy_rain_icon_tk, bg=("#1F6E8C"))
            heavy_rain_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            heavy_rain_icon_label.image = heavy_rain_icon_tk


        elif fourth_day_condition['text'] == 'Light showers of ice pellets' or fourth_day_condition[
            'text'] == 'Moderate or heavy showers of ice pellets':
            # Load the icon
            freezing_rain_icon = Image.open("day/320.png")
            # Convert to a tkinter-compatible object
            freezing_rain_icon_tk = ImageTk.PhotoImage(freezing_rain_icon)
            # Create the label widget to store the image
            freezing_rain_icon_label = tk.Label(master=day_four_label, image=freezing_rain_icon_tk, bg=("#1F6E8C"))
            freezing_rain_icon_label.place(relx=.25, rely=.7)

            # Store the image reference to prevent garbage collection
            freezing_rain_icon_label.image = freezing_rain_icon_tk




        elif fourth_day_condition['text'] == 'Patchy light rain with thunder' or fourth_day_condition[
            'text'] == 'Moderate or heavy rain with thunder' or fourth_day_condition['text'] == 'Patchy light snow with thunder' or \
                fourth_day_condition['text'] == 'Moderate or heavy snow with thunder':
            # Load the icon
            rain_thunder_icon = Image.open("day/248.png")
            # Convert to a tkinter-compatible object
            rain_thunder_icon_tk = ImageTk.PhotoImage(rain_thunder_icon)
            # Create the label widget to store the image
            rain_thunder_icon_label = tk.Label(master=day_four_label, image=rain_thunder_icon_tk, bg=("#1F6E8C"))
            rain_thunder_icon_label.place(relx=.25, rely=.7)


    draw_widgets()
    forward_button_multi_day_prediction()




    # refresh weather button should be a search icon
    ######## deprecated code and ideas ##########

    # redraw_content()
    #
    # def redraw_content():
        # Redraw or add new content in the root window
        # add_scrollable_canvas(root)
        # Add additional content or modifications as needed

    # # store the time string in current day variableh
    # current_day = local_time
    # # convert the date string to a datetime object and get the weekday name
    # weekday_name = calendar.day_name[datetime.datetime.strptime(current_day, '%Y-%m-%d %H:%M').date().weekday()]

    # city_and_country = (f"{city}, {country}")
    # temperature_formatted = (f"{temperature} °C")
    # wind_speed_formatted = (f"{wind_speed} km/h")

    # def add_scrollable_canvas(master):
    #     # Create a scrollable canvas
    #     canvas = Canvas(master)
    #     canvas.place(x=0, y=0, relwidth=1, relheight=1)
    #
    #     # Create a frame to hold the image and the scrollbar
    #     frame = Frame(canvas)
    #     frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    #
    #     # Add content to the frame
    #     image_path = "weather images/multi_day_windows.png"
    #     image = Image.open(image_path)
    #     photo = ImageTk.PhotoImage(image)
    #     canvas.create_image(0, 0, anchor=NW, image=photo)
    #     canvas.image = photo  # Keep a reference to prevent garbage collection
    #
    #     # Add a scrollbar to the canvas
    #     scrollbar = Scrollbar(canvas, orient=VERTICAL, command=canvas.yview)
    #     scrollbar.place(relx=1, rely=0, relheight=1, anchor=NE)
    #     canvas.configure(yscrollcommand=scrollbar.set)
    #
    #     # Configure the canvas to scroll with the mouse wheel
    #     canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    #     canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
    #
    #     # Configure the canvas to contain the frame
    #     canvas.create_window((0, 0), window=frame, anchor=NW)
    #
    #     # Create a separate frame within the root window for the textbox
    #     textbox_frame = Frame(frame, width=600, height=1600)
    #     textbox_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    #
    #     # Create the textbox
    #     multi_text_box = customtkinter.CTkTextbox(master=textbox_frame, height=400, width=200)
    #     multi_text_box.place(relx=0.5, rely=0.5, anchor=CENTER)
    #
    # # Create a frame to hold the canvas and scrollbars
    # frame = Frame(root, width=300, height=300)
    # frame.place(x=0, y=0, relwidth=1, relheight=1)
    #
    # # Create the canvas and scrollbars
    # canvas = Canvas(frame, bg='#FFFFFF', width=300, height=300, scrollregion=(0, 0, 500, 500))
    # hbar = Scrollbar(frame, orient=HORIZONTAL)
    # hbar.place(relx=0, rely=1, relwidth=1, anchor=S)
    # hbar.config(command=canvas.xview)
    # vbar = Scrollbar(frame, orient=VERTICAL)
    # vbar.place(relx=1, rely=0, relheight=1, anchor=NE)
    # vbar.config(command=canvas.yview)
    # canvas.config(width=300, height=300)
    # canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    # canvas.place(x=0, y=0, relwidth=1, relheight=1)
    #
    # # Clear the screen and redraw the content





# def weather_icons():
#     with open('weather_conditions.json', 'r') as icons:
#         weather_icons_dictionary = json.load(icons)
#         print(weather_icons_dictionary)


# weather_conditions = customtkinter.CTkButton(master=root, text="weather conditions", command=weather_icons)
# weather_conditions.place(x=275, y=150)




# country = dictionary['location']['country']
# city = dictionary['location']['name']
# temperature = dictionary['current']['temp_c']
# wind_speed = dictionary['current']["wind_kph"]
# local_time = dictionary['location']['localtime']
# condition = dictionary['current']['condition']
#
# print(f"Country: {country}")
# print(f"The weather in {city}: ")
# print(f"The temperature is {temperature} °C")
# print(f"The wind speed is {wind_speed} km/h")
# print(f"The time in {city} is {local_time}")
# print(f"The conditions: {condition['text']} ")


# brain storming
# we can use a tree type system to pass important data to each part of the code
# for example if the weather is 27C we can say weather > 20C show image of sun
# if weather rainy show picture of rain
#if weather rainy play sad music
#if sunny play upbeat music
# we can do all the calls based on what is written to our dictionary
# we can have graphics to represent different cities in other parts of the world






#start the event loop
root.mainloop()

