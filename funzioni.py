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

    if(radius <= 0):
        print(' THE RADIUS MUST BE GREATER THAN 0')
        return 0,0

    if(start_latitude <= -90 or start_latitude >= 90):
        print('INVALID LATITUDE')
        return 0,0

    if(start_longitude <= -180 or start_longitude >= 180):
        print('INVALID LONGITUDE')
        return 0,0


    start = geopy.Point(start_latitude, start_longitude)
    distance =geopy.distance.great_circle(kilometers = radius)


    # Select random displacement
    random_displacement = random.uniform(0,2*math.pi)

    # Calculate new latidude and longitude according to the Great Circle Navigation Formulae
    dest = distance.destination(point=start, bearing=random_displacement)

    end = geopy.Point(dest.latitude,dest.longitude)

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
        while(new_radius == 0 or new_radius == old_radius):  #the new radius cannot be 0
            new_radius = old_radius * random.random()
        return calculate_coordinates(args[0],new_radius)
    else:
        old_radius = args[2]
        while(new_radius == 0 or new_radius == old_radius):
            new_radius = old_radius * random.random()
        return calculate_coordinates(args[0],args[1],new_radius)
            

# chooses a random radius between the internal and external one and pass it to the calculate_coordinates function
# the same logic used in the function within_a_circle is used.
def donut_masking(*args):

    if(len(args) == 3):
        if(int(args[1])>=int(args[2])):
             print('THE EXTERNAL RADIUS MUST BE GREATER THAN THE INTERNAL ONE')
             return 0,0
        new_radius = args[1]
        while(new_radius == args[1] or new_radius == args[2] ): #the new radius can't be the same as the internal or external one 
         new_radius = random.uniform(args[1], args[2])
        return calculate_coordinates(args[0],new_radius)
    else:
        if(args[2]>=args[3]):
             print('THE EXTERNAL RADIUS MUST BE GREATER THAN THE INTERNAL ONE')
             return 0,0
        new_radius = args[2]
        while(new_radius == args[2] or new_radius == args[3]): #the new radius can't be the same as the internal or external one 
            new_radius = random.uniform(args[2], args[3])
        return calculate_coordinates(args[0],args[1],new_radius)
        


def standard_gaussian(*args):
     
    lat,lon,variance = 0,0,0

    if(len(args) == 2):
        lat,lon= find_coordinates(args[0])
        variance= args[1]
    else:
        lat,lon,variance = args[0],args[1],args[2]


    if(lat <= -90 or lat >= 90):
        print('INVALID LATITUDE')
        return 0,0

    if(lon <= -180 or lon >= 180):
        print('INVALID LONGITUDE')
        return 0,0

    if(variance <= 0):
        print('THE VARIANCE MUST BE GREATER THAN ZERO')
        return 0,0


    #choose a random point in the new gaussian function
    X = numpy.random.normal((lat, lon),variance,size=(1,2))

    latitude,longitude = X[0][0],X[0][1]

    if(latitude < -90.0 or latitude > 90.0 or longitude < -180.0 or longitude > 180.0):
        latitude,longitude = wrap(latitude,longitude)

    print(latitude,longitude)

    return latitude,longitude

# a bimodal gaussian is a mixture of two different normal distributions.
#The idea is to choose randomly one of the two distrubutions and avail of the standard_gaussian function
def bimodal_gaussian(*args):
    toss = random.choice( (1, 2) )
    print(toss)
    if toss == 1: 
        if(len(args) == 4 or type(args[0])==str):
            return standard_gaussian(args[0],args[1])
        else:
            return standard_gaussian(args[0],args[1],args[2])
        
    else:
        if(len(args) == 4):
            return standard_gaussian(args[2],args[3])
        elif(type(args[3])==str):
            return standard_gaussian(args[3],args[4])
        elif(len(args) == 5):
            return standard_gaussian(args[2],args[3],args[4])
        else:
            return standard_gaussian(args[3],args[4],args[5])


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

"""""
l1,l2 = calculate_coordinates(51.50085578008017, -0.12472204631096782,6)

l1,l2 = calculate_coordinates('London',6)

l1,l2 = donut_masking(51.50085578008017, -0.12472204631096782,10,16)

l1,l2 = donut_masking('Berlin',10,16)

l1,l2 = within_a_circle(51.50085578008017, -0.12472204631096782,6)

l1,l2 = within_a_circle('Athens',6)

l1,l2 = bimodal_gaussian(44.0510268315349, 10.059425432817703,0.5,'Carrara',0.5)

l1,l2 = bimodal_gaussian('London',0.5,'Wembley',0.5)

l1,l2 = bimodal_gaussian(45.647777165237784, -74.37118024765526,0.7,45.64964117345706, -74.09120131874,0.7)

l1,l2 = standard_gaussian('Marina di Carrara',0.01)

l1,l2 = standard_gaussian(37.794932, 23.879845,0.6)

l1,l2 = calculate_coordinates('175 5th Avenue NYC',9)

l1,l2 = calculate_coordinates('9 Via Sant\'Andrea MI',9)

l1,l2 = bimodal_gaussian('Carrara',0.5,44.0510268315349, 10.059425432817703,0.5)

l1,l2 = within_a_circle('13 Rue de Rivoli FR',6)

l1,l2 = donut_masking('13 Rue de Rivoli FR',10,10)

l1,l2 = donut_masking('13 Rue de Rivoli FR',10,5)

l1,l2 = donut_masking('13 Rue de Rivoli FR',10,10)

l1,l2 = within_a_circle('Athens',-6)

l1,l2 = bimodal_gaussian('Carrara',0.5,44.0510268315349, 10.059425432817703,0.5)

l1,l2 = bimodal_gaussian(44.0510268315349, 10.059425432817703,0.5,'Carrara',0.5)

l1,l2 = bimodal_gaussian('Massa',0.5,'Carrara',0.5)

l1,l2 = bimodal_gaussian(90, 120.2323,0.5,90,34.45764,0.5)

l1,l2 = within_a_circle(-170,-245,6)

l1,l2 = donut_masking(90.1,56,20,10)

"""





