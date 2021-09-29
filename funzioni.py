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


def find_coordinates(location):
  
    """

    Returns the latitude and the longitude in decimal degrees
    :param location: a string representing the name of a city or an address in the form civic number, street, city

    """

    geolocator = Nominatim(user_agent="my_request")
    try:
        location = geolocator.geocode(location)
    except:
        return find_coordinates(location)
     
    return location.latitude, location.longitude




def calculate_coordinates(*args): 

    """
    Chooses a random point on a circle around the original location 
    args:
        case 2 parameters:
            a city or an address (string)
            radius in kilometers(float)

        case 3 parameters:
            latitude (float)
            longitude (float)
            radius in kilometers(float)

    """

    start_latitude,start_longitude,radius = 0,0,0

    if(len(args) == 2): #case 2. We need to find the coordinates of the location
        radius = args[1]
        print('here')
        start_latitude,start_longitude = find_coordinates( args[0] )
    else:
         start_latitude,start_longitude,radius = args[0],args[1],args[2]

    if(radius <= 0):
        raise Exception(' THE RADIUS MUST BE GREATER THAN 0')


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
    return dest.latitude,dest.longitude



def within_a_circle(*args):

    """
    Chooses a random point in a circle around the original location 
    args:
        case 2 parameters:
            a city or an address (string)
            radius in kilometers(float)

        case 3 parameters:
            latitude (float)
            longitude (float)
            radius in kilometers(float)

    """

    new_radius = 0

    if(len(args) == 2):
        old_radius = args[1]
        location = args[0]
    else:
        old_radius = args[2]
        lat = args[0]
        lon = args[1]

        """
        Finds a new radius smaller than the one passed as argument and calls the calculate_coordinates function to find the new point.
        This way the resulting point will be inside the circle
        
        """

        while(new_radius == 0 or new_radius == old_radius):  #the new radius cannot be 0
            new_radius = old_radius * random.random() #value of new radius
    if(len(args) == 2):
        return calculate_coordinates(location,new_radius)
    else:
        return calculate_coordinates(lat,lon,new_radius)




def donut_masking(*args):

    """
    Chooses a random point on a circular crown around the original location 
    args:
        case 2 parameters:
            a city or an address (string)
            internal radius in kilometers(float)
            external radius in kilometers(float)

        case 3 parameters:
            latitude (float)
            longitude (float)
            internal radius in kilometers(float)
            external radius in kilometers(float)

    """

    if(len(args) == 3):

        location = args[0]
        internal_radius = args[1] 
        external_radius = args[2]

    else:
        lat,lon = args[0],args[1]
        internal_radius = args[2] 
        external_radius = args[3]
        
    if(int(internal_radius )>=int(external_radius)):
            raise Exception('THE EXTERNAL RADIUS MUST BE GREATER THAN THE INTERNAL ONE')

    """

        Finds a new radius between the ones passed as arguments and calls the calculate_coordinates function to find the new point.
        This way the resulting point will be inside the circular crown     

    """


    new_radius =internal_radius
    while(new_radius == internal_radius or new_radius == external_radius ): #the new radius can't be the same as the internal or external one 
        new_radius = random.uniform(internal_radius, external_radius )

    if(len(args) == 2):
            return calculate_coordinates(location,new_radius)
    else:
        return calculate_coordinates(lat,lon,new_radius)


def standard_gaussian(*args):

    """
      Chooses a random point on a standard gaussian whose peak is the original location
       args:
        case 2 parameters:
            a city or an address (string)
            variance (float)

        case 3 parameters:
            latitude (float)
            longitude (float)
            variance (float)

    """
     
    lat,lon,variance = 0,0,0

    if(len(args) == 2):
        lat,lon= find_coordinates(args[0])
        variance= args[1]
    else:
        lat,lon,variance = args[0],args[1],args[2]


    if(lat <= -90 or lat >= 90):
        raise Exception('INVALID LATITUDE')

    if(lon <= -180 or lon >= 180):
       raise Exception('INVALID LONGITUDE')


    if(variance <= 0):
        raise Exception('THE VARIANCE MUST BE GREATER THAN ZERO')


    #choose a random point in the new gaussian function
    new_point = numpy.random.normal((lat, lon),variance,size=(1,2))

    latitude,longitude = new_point[0][0],new_point[0][1]

    if(latitude < -90.0 or latitude > 90.0 or longitude < -180.0 or longitude > 180.0):
        latitude,longitude = wrap(latitude,longitude)

    return latitude,longitude


def bimodal_gaussian(*args):

    """
    Chooses a random point on a standard gaussian whose peak is the original location
       args:
        case 4 parameters:
            a city or an address 1st location (string)
            variance 1st location (float)
            a city or an address 2nd location (string)
            variance 2nd location (float)

        case 5 parameters:
            case 5.1
                latitude 1st location (float)
                longitude 1st location (float)
                variance 1st location (float)
                a city or an address 2nd location (string)
                variance 2nd location (float)

            case 5.2
                a city or an address 1st location (string)
                variance 1st location (float)
                latitude 2nd location (float)
                longitude 2nd location (float)
                variance 2nd location (float)


        case 6 parameters:
            latitude 1st location (float)
            longitude 1st location(float)
            variance 1st location(float)
            latitude 2nd location (float)
            longitude 2nd location (float)
            variance 2nd location (float)

    """

    toss = random.choice( (1, 2) ) #randomly chooses one of the two standard distributions the bimodal gaussian is made of
    print(toss)

    if toss == 1: 
        if(len(args) == 4 or type(args[0])==str): # case 4 or 5.1
            return standard_gaussian(args[0],args[1]) #args[0] = location args[1] = variance
        else: # case 5.2 or 6
            return standard_gaussian(args[0],args[1],args[2]) #args[0] = latitude args[1] = longitude  args[2] = variance
        
    else:
        if(len(args) == 4): # case 4 
            return standard_gaussian(args[2],args[3]) #args[2] = location args[3] = variance
        elif(len(args) == 5):
            if(type(args[3])==str): #case 5.2
                return standard_gaussian(args[3],args[4]) #args[3] = location args[4] = variance
            else: #case 5.1. 
                return standard_gaussian(args[2],args[3],args[4]) #args[2] = latitude args[3] = longitude args[4] = variance
        else: #case 6
            return standard_gaussian(args[3],args[4],args[5]) #args[3] = latitude args[4] = longitude args[5] = variance

def wrap(latitude,longitude):


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

l1,l2 = within_a_circle(34,67,7)