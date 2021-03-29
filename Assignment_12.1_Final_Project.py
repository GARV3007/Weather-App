# File : Assignment 12.1 Final Project.py
# Name : Gourav Verma
# Date : 11/13/2019
# Course : DSC-510 - Introduction to Programming
# Des  : Week-12 : Final Project
# This program accepts city or zip code and displays the weather. Users can check weather for
# as many cities or zip codes as they want. Secure API key is used to invoke the secure http
# web service call to openweather.

# import required libraries
import requests
import datetime
import sys

api_key = "e64a68ef9d782816def0fd03477ee93f"    # API key used to invoke open weather map API services
req_url = "https://api.openweathermap.org/data/2.5/weather?APPID={}&units=imperial&"    # generic part of req url


# function to invoke API using city
def retrieveWeatherByCity(city):
    req = (req_url + "q={}").format(api_key, city)
    response = requests.request("GET", req)  # invoke GET request
    return response     # return response


# function to invoke API using Zip code
def retrieveWeatherByZip(zipCode):
    req = (req_url + "zip={},us").format(api_key, zipCode)
    response = requests.request("GET", req)  # invoke GET request
    return response     # return response


# parse response from API call
def parseWeather(jsonMsg):
    print("{}".format("Current weather condition for {}").format(jsonMsg["name"]).center(40))
    print(" {:18}:  {}°F".format("Temperature", jsonMsg["main"]["temp"]))
    print(" {:18}:  {}".format("Condition", jsonMsg["weather"][0]["description"]))
    if len(jsonMsg["weather"]) > 1:
        for cond in jsonMsg["weather"][1:]:
            if cond["description"]:
                print(" {:18}:  {}".format(" ", cond["description"]))
    if jsonMsg["main"]["pressure"] is not None:
        print(" {:18}:  {} hPa".format("Pressure", jsonMsg["main"]["pressure"]))
    if jsonMsg["main"]["humidity"] is not None:
        print(" {:18}:  {} %".format("Humidity", jsonMsg["main"]["humidity"]))
    if jsonMsg["wind"] is not None:
        print(" {:18}:  {} m/s, {}°".format("Wind", jsonMsg["wind"]["speed"], jsonMsg["wind"]["deg"]))


# main function
def main():

    print("Welcome to Weather Application")

    while True:
        user_choice = input("Look up weather by city or zip, enter 1 for US City, 2 for zip \n")

        if user_choice == '1':
            location = input("Please enter a city \n")
            response = retrieveWeatherByCity(location)
        elif user_choice == '2':
            location = input("Please enter a Zip \n")
            if location.isnumeric():
                response = retrieveWeatherByZip(location)
            else:
                sys.exit("Invalid entry, Zip code must be numeric")  # Error message
        else:
            sys.exit("Invalid entry, Please try again later")  # Error message

        if response.status_code != 200:
            print("Not able to retrieve weather information for '{}'; error - {}".format(location,
                                                                                      response.json()["message"]))
        else:
            try:
                parseWeather(response.json())
            except Exception as e:
                print("Error in printing the details; error - {} not found".format(e), "\n")

        cont_flag = input("Would you like to like to perform another lookup \n "
                          "(enter y to continue)? \n")
        if cont_flag.capitalize() != "Y":
            break

    print("Thank you for using the weather application \n")


# mainline code
if __name__ == '__main__':
    main()