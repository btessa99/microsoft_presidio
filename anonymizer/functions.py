from logging import raiseExceptions
import random
import math
from geopy import location
from geopy.geocoders import Nominatim
import geopy
import geopy.distance
from geopy.units import kilometers, radians
import numpy
from numpy.core.numerictypes import ScalarType
import re
from random import uniform


def find_coordinates(self,location):
  
    """

    Returns the latitude and the longitude in decimal degrees
    :param location: a string representing the name of a city or an address in the form civic number, street, city

    """

    geolocator = Nominatim(user_agent="my_request")
    try:
        location = geolocator.geocode(location)
    except:
        return find_coordinates(self,location) #request again the location if a timeOut is received

    if(not location): #location not recognized
       return 0,0
        
    return location.latitude, location.longitude


def from_dms_to_dd (self,coordinate_dms):
    """
    Converts a coordinate from decimal minutes seconds format to decimal degree
    :param: coordinate_dms: the latitude or longitude to convert

    """
    only_numbers_coordinates = [float(s) for s in re.findall(r'-?\d+\.?\d*', coordinate_dms)]
    coordinate_dd = 0
    for i in range(0,len(only_numbers_coordinates)):
        coordinate_dd = coordinate_dd + only_numbers_coordinates[i]/(60**i)

    return coordinate_dd



def calculate_coordinates(self,*args): 

    

    """
    Chooses a random point on a circle around the original location 
    args:
        case 2 parameters:
            a city or an address (string) 
            radius in kilometers(float)

        case 3 parameters:
            latitude (float/integer)
            longitude (float/integer)
            radius in kilometers(float/integer)

    """

    start_latitude,start_longitude,radius = 0,0,0

    if(len(args) == 2):
        start_latitude,start_longitude = get_dd_coordinates(self,args[0])
        radius = args[1]
    else:
        radius = args[2]
        if(type(args[1]) == float):
            start_latitude,start_longitude = float(args[0]),float(args[1])

            if(start_latitude <= -90 or start_latitude >= 90):
                raise Exception('INVALID LATITUDE')
    

            if(start_longitude <= -180 or start_longitude >= 180):
                raise Exception('INVALID LONGITUDE')

        

    start = geopy.Point(start_latitude, start_longitude) #create a new geodetic point representing the original location

    distance =geopy.distance.great_circle(kilometers = radius) #set the distance between the two points


    # Select random displacement
    random_displacement = random.uniform(0,2*math.pi) #random bearing 

    # Calculate new latidude and longitude according to the Great Circle Navigation Formulae
    dest = distance.destination(point=start, bearing=random_displacement)

    # Return the pair (latitude,longitude) representing the new point
    if(start_longitude == 0):
        direction = "N"
        if(dest.latitude < 0):
            direction = "S"
        return str(abs(dest.latitude))+direction,0
    elif(start_latitude == 0):
        direction = "E"
        if(start_longitude < 0):
            direction = "W"
        return 0,str(abs(dest.longitude))+direction
    else:
        return dest.latitude,dest.longitude



def within_a_circle(self,location,radius):

    """
    Chooses a random point in a circle around the original location 
    :param location: a string representing a pair of coordinates separated by a comma, a city name or an address
    :param radius: integer or float representing the radius of the circle
    """

    lat,lon = 0,0

    if "," in location:
        lat,lon = location.split(",")

    new_radius = 0
    old_radius = radius


    """
    Finds a new radius smaller than the one passed as argument and calls the calculate_coordinates function to find the new point.
    This way the resulting point will be inside the circle
    
    """

    while(new_radius == 0 or new_radius == old_radius):  #the new radius cannot be 0
        new_radius = old_radius * random.random() #value of new radius


    if(lon == 0):
        return calculate_coordinates(self,location,new_radius)
    else:
        return calculate_coordinates(self,lat,lon,new_radius)




def donut_masking(self,location,internal_radius,external_radius):

    """
    Chooses a random point on a circular crown around the original location 

    :param location: a string representing a pair of coordinates separated by a comma, a city name or an address
    :param internal_radius: integer or float representing the internal radius of the circlular crown
    :param external_radius: integer or float representing the external radius of the circlular crown

    """

    
    lat,lon = 0,0

    if "," in location:       #check if location represents a couple of coordinates or a city/address
        lat,lon = location.split(",")

    """

        Finds a new radius between the ones passed as arguments and calls the calculate_coordinates function to find the new point.
        This way the resulting point will be inside the circular crown     

    """

    new_radius =internal_radius
    while(new_radius == internal_radius or new_radius == external_radius ): #the new radius can't be the same as the internal or external one 
        new_radius = random.uniform(internal_radius, external_radius )

    if(lon == 0):
        return calculate_coordinates(self,location,new_radius)
    else:
        return calculate_coordinates(self,lat,lon,new_radius)

def get_dd_coordinates(self,location):

    start_longitude,start_latitude = 0,0

    if "," in location:       #check if location represents a couple of coordinates or a city/address
        lat,lon = location.split(",")
        if(type(lat) != float): #pair of coordinates in DMS format
            start_latitude,start_longitude = from_dms_to_dd(self,lat),from_dms_to_dd(self,lon)

    elif(("º" in location ) or ("°" in location) or ("°" in location) or ("˚" in location)): #single latitude or longitude expressed with coordinates in DMS format
        if("N" in location or "S" in location):
            start_latitude = from_dms_to_dd(self,location)
        else:
            start_longitude = from_dms_to_dd(self,location)
            
    elif("." in location): # a single coordinate in DD is given
        if("N" in location ): #single latitude
            start_latitude = location.strip('N') 
        elif( "S" in location):
            start_latitude = float(location.strip('S')) * (-1)

        elif( "E" in location):
             start_longitude = location.strip('E') 
            
        else:
            start_longitude = float(location.strip('W')) * (-1)

    else:
        start_latitude,start_longitude = find_coordinates(self,location)

    return start_latitude,start_longitude


def standard_gaussian(self,location,variance):

    """
      Chooses a random point on a standard gaussian whose peak is the original location

      :param location: a string representing a pair of coordinates separated by a comma, a city name or an address
      :param variance: an integer representing the variance of the gaussian

    """
       
    lat,lon = get_dd_coordinates(self,location)

 
    if(float(lat) <= -90 or float(lat) >= 90):
        raise Exception('INVALID LATITUDE')

    if(float(lon) <= -180 or float(lon) >= 180):
       raise Exception('INVALID LONGITUDE')


    #choose a random point in the new gaussian function
    new_point = numpy.random.normal((float(lat), float(lon)),variance,size=(1,2))

    latitude,longitude = new_point[0][0],new_point[0][1]

    #if(latitude < -90.0 or latitude > 90.0 or longitude < -180.0 or longitude > 180.0):
        #latitude,longitude = wrap(self,latitude,longitude)

    if(lon == 0):
        direction = "N"
        if(latitude < 0):
            direction = "S"
        return str(abs(latitude))+direction,0
    elif(lat == 0):
        direction = "E"
        if(lon < 0):
            direction = "W"
        return 0,str(abs(longitude))+direction

    else:
        return latitude,longitude


def bimodal_gaussian(self,location1,variance1,location2,variance2):

    """
    Chooses a random point on a bimodal gaussian whose peaks are the original locations
    
      :param location1: a string representing a pair of coordinates separated by a comma, a city name or an address
      :param variance1: an integer representing the variance of the gaussian

      :param location2: a string representing a pair of coordinates separated by a comma, a city name or an address
      :param variance2: an integer representing the variance of the gaussian
      
    """

    toss = random.choice( (1, 2) ) #randomly chooses one of the two standard distributions the bimodal gaussian is made of

    print(toss)
    if toss == 1: 
        return standard_gaussian(self,location1,variance1)
    else:
        return standard_gaussian(self,location2,variance2)
        

def wrap(self,latitude,longitude):


  #longitude wrapping simply requires adding +- 360 to the value until it comes
  #in to range.
  #for the latitude values we need to flip the longitude whenever the latitude
  #crosses a pole.
    
    
    quadrant = math.floor( abs( latitude  ) / 90) % 4 + 1 #quadrant 

    pole = 90 #north pole

    if(latitude < 0):
        pole = -90 #south pole

    displacement = latitude % 90 #normalized latitude

    if(quadrant == 1):
        latitude = displacement

    elif(quadrant == 2):   #flip the longitude and set the new latitude as the distance from the pole
        latitude = pole - displacement
        longitude = longitude + 180

    elif(quadrant == 3): #flip both latitude and longitude
        latitude = displacement * (-1)
        longitude = longitude + 180

    else: #set the new latitude as the distance from the pole
        latitude = displacement - pole 

    longitude = (longitude + 180) % 360 - 180 #fix the longitude

    return latitude,longitude
