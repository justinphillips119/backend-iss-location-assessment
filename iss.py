#!/usr/bin/env python

__author__ = 'Justin Phillips'

import requests
import time
import turtle

world_map_img = "map.gif"
iss_img = "iss.gif"
iss_url = "http://api.open-notify.org"

def astronaut_info():
    req = requests.get(iss_url + "/astros.json")
    return req.json()["people"]

def iss_location():
    req = requests.get(iss_url + "/iss-now.json")
    position = req.json()["iss_position"]
    latitude = float(position["latitude"])
    longitude = float(position["longitude"])
    return latitude, longitude

def iss_map(latitude, longitude):
    map = turtle.Screen()
    map.setup(720, 360)
    map.bgpic(world_map_img)
    map.setworldcoordinates(-180, -90, 180, 90)
    map.register_shape(iss_img)
    iss = turtle.Turtle()
    iss.shape(iss_img)
    iss.setheading(90)
    iss.penup()
    iss.goto(longitude, latitude)
    return map

def rise_time(latitude, longitude):
    params = {"lat": latitude, "lon": longitude}
    req = requests.get(iss_url + "/iss-pass.json", 
                    params = params)
    passover_time = req.json()["response"][1]["risetime"]
    return time.ctime(passover_time)



def main():
    astro_info = astronaut_info()
    print("Number of astronauts currently in space: {}".format(len(astro_info)))
    for astronaut in astro_info:
        print(" - {} on {}".format(astronaut["name"], astronaut["craft"]))
    latitude, longitude = iss_location()
    print("Current coordinates of the ISS: latitude={:.02f} longitude={:.02f}".format(latitude, longitude))

    map = None
    try:
        map = iss_map(latitude, longitude)
        indiana_latitude = 39.791000
        indiana_longitude = -86.148003
        location_pin = turtle.Turtle()
        location_pin.penup()
        location_pin.color("red")
        location_pin.goto(indiana_longitude, indiana_latitude)
        location_pin.dot(5)
        passover_time = rise_time(indiana_latitude, indiana_longitude)
        location_pin.write(passover_time)
    except RuntimeError as e:
        print("ERROR: problem loading graphics: " + str(e))
    if map is not None:
        print("Click map to exit...")
        map.exitonclick()

if __name__ == '__main__':
    main()
