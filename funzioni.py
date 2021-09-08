import random
import math
from geopy import location
from geopy.geocoders import Nominatim
import geopy
import geopy.distance
from geopy.units import kilometers, radians
import numpy
from numpy.core.numerictypes import ScalarType





# Latitude and longitude must be in decimal degrees and radius in meters.

def find_coordinates(location):

    geolocator = Nominatim(user_agent="my_request")
    try:
        location = geolocator.geocode(location)
    except:
        return find_coordinates(location)
     
    return location.latitude, location.longitude



# Chooses a random point on a circle around the original location identified by the pair (lat,lon)
def calculate_coordinates(*args): 

    start_latitude,start_longitude,radius = 0,0,0

    if(len(args) == 2):
        radius = args[1]
        start_latitude,start_longitude = find_coordinates( args[0] )
    else:
         start_latitude,start_longitude,radius = args[0],args[1],args[2]
        

    start = geopy.Point(start_latitude, start_longitude)
    distance =geopy.distance.distance(kilometers = radius)


    # Select random displacement
    random_displacement = random.uniform(0,2*math.pi)

    # Calculate new latidude and longitude according to the Great Circle Navigation Formulae
    dest = distance.destination(point=start, bearing=random_displacement)

    end = geopy.Point(dest.latitude,dest.longitude)
    print('distance: ',geopy.distance.distance(start, end).km)

    # Return a tuple (latitude,longitude)
    return dest.latitude,dest.longitude

#chooses a radius smaller than the one passed as argument and uses the function calculate_coordinates() to 
#find a new pair of latitude and longitude. Since the purpose of the function is to find a new location inside a circle,
#and the calculate_coordinates function finds a new location on the circle, if  new the randomly generated radius is smaller than the one passed
#as argument, then we'll eventually find a point inside the circle.
def within_a_circle(*args):

    new_radius = 0

    if(len(args) == 2):
        old_radius = args[1]
        while(new_radius == 0):  #the new radius cannot be 0
            new_radius = old_radius * random.random()
        return calculate_coordinates(args[0],new_radius)
    else:
        old_radius = args[2]
        while(new_radius == 0):
            new_radius = old_radius * random.random()
        return calculate_coordinates(args[0],args[1],new_radius)
            

# chooses a random radius between the internal and external one and pass it to the calculate_coordinates function
# the same logic used in the function within_a_circle is used.
def donut_masking(*args):

    if(len(args) == 3):
        new_radius = args[1]
        while(new_radius == args[1]): #the new radius can't be the same as the internal one
         new_radius = random.uniform(args[1], args[2])
        return calculate_coordinates(args[0],new_radius)
    else:
        new_radius = args[2]
        while(new_radius == args[2]): #the new radius can't be the same as the internal one
            new_radius = random.uniform(args[2], args[3])
        return calculate_coordinates(args[0],args[1],new_radius)
        



def standard_gaussian(*args):
     
    lat,lon,variance = 0,0,0

    if(len(args) == 2):
        lat,lon= find_coordinates(args[0])
        variance= args[1]
    else:
        lat,lon,variance = args[0],args[1],args[2]


    #choose a random point in the new gaussian function
    X = numpy.random.normal((lat, lon),variance,size=(1,2))

    latitude,longitude = X[0][0],X[0][1]

    if(latitude < -90.0 or latitude > 90.0 or longitude < -180.0 or longitude > 180.0):
        latitude,longitude = wrap(latitude,longitude)

    return latitude,longitude

# a bimodal gaussian is a mixture of two different normal distributions.
#The idea is to choose randomly one of the two distrubutions and avail of the standard_gaussian function
def bimodal_gaussian(*args):
    toss = random.choice( (1, 2) )
    if toss == 1: 
        if(len(args) == 4):
            standard_gaussian(args[0],args[1])
        else:
            standard_gaussian(args[0],args[1],args[2])
        
    else:
        if(len(args) == 4):
            standard_gaussian(args[2],args[2])
        else:
            standard_gaussian(args[3],args[4],args[5])

def wrap(latitude,longitude):


  #longitude wrapping simply requires adding +- 360 to the value until it comes
  #in to range.
  #for the latitude values we need to flip the longitude whenever the latitude
  #crosses a pole.
    

    quadrant = math.floor( abs( latitude  ) / 90) % 4 + 1

    pole = 90

    if(latitude < 0):
        pole = -90

    displacement = latitude % 90

    if(quadrant == 1):
        latitude = displacement

    elif(quadrant == 2):
        latitude = pole - displacement
        longitude = longitude + 180

    elif(quadrant == 3):
        latitude = displacement * (-1)
        longitude = longitude + 180

    else:
        latitude = displacement - pole

    longitude = (longitude + 180) % 360 - 180

    return latitude,longitude
