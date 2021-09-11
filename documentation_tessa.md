
#DOCUMENTATION
##Anonymizer functions

The following functions were implemented with the help of **GeoPy**, a Python client useful for geocoding web services since it provides means not only to locate the coordinates of an address, a city or a country but also to do the reverse operation and measure distances.

Let's now introduce the functions:

**find_coordinates(location)**

location: the name of a city (eg : London) or an address (eg : "175 5th Avenue NYC")

Given the location, it returns the pair (latitude,longitude) in decimal degrees.
In order to accomplish that the function geolocator.geocode is used,
where geolocator is an instance of the *Nominatim class*.
This function can throw a GeocoderTimedOut exception if the server does not give a response to the coordinates request.
The issue can be easily solved by calling the function again until the coordinates are given-


**wrap(latitude,longitude)**

latitude,longitude : latitude and longitude in decimal degrees.

This function is called whether one of the two parameters(or both) is out of range and its needs to be put in range.
For the latitude what needs to be done is to simply add +- 360 to the value until it comes in to range.
For the latitude value we need to flip the longitude whenever the latitude crosses a pole.
Firstly we need to calculate where in which quadrant the point is located and its distance from the pole (displacement).
The pole is 90 if the latitude is positive and -90 otherwise

1st quadrant: the latitude value is already in range so we put latitude = displacement 
2nd quadrant: we need to set the new latitude as 90 minus the displacement
and flip the longitude by adding 180 degrees
3rd quadrant: we need to flip the longitude again and then set the latitude as -displacement
4th quadrant: the new latitude is the displacent minus the pole

The last thing to be done is to fix the longitude value and the return the in range coordinates.


**calculate_coordinates(*args)**

The purpose of this function is to find a new point on a circle whose center is a location passed as an argument and so is the radius.
The displacement is randomly generated thanks to random.uniform(0,2 x math.pi)

The number of the arguments is variable and the function can have to formats:

*calculate_coordinates(latitude,longitude,radius)*
where the radius is in kilometers and the latitude and longitude are in decimal degrees
or:
*calculate_coordinates(location,radius)* where location is the name of a city (eg : London) or an address (eg : "175 5th Avenue NYC") and the radius is in kilometers

If the function is in the second format, which can be easily understood by the number of arguments passed , we have to avail of the function find_coordinates to retrieve the correct latitude and longitude.

Once having found the coordinates, we need to create a new instance of the class *geopy.Point* which locates a point on the surface on Earth 

start = geopy.Point(start_latitude, start_longitude)

and then we can find the new point according to the Great Circle Navigation Formulae by using the function 
distance.destination(point=start, bearing=random_displacement)
where distance is a general distance object initialized with the value of the radius passed as an argument.

The coordinates of the new points in decimal degrees are returned.


**within_a_circle(*args)**

This function find a new point inside a circle whose center is a location passed as an argument and so is the radius.
The displacement is randomly generated thanks to random.uniform(0,2 x math.pi)

The number of the arguments is variable and the function can have to formats:

*within_a_circle(latitude,longitude,radius)* where the radius is in kilometers and the latitude and longitude are in decimal degrees
or:
*within_a_circle(location,radius)* where location is the name of a city (eg : London) or an address (eg : "175 5th Avenue NYC") and the radius is in kilometers

The idea behind this function is that since the purpose is to find a new point inside the circle, we can still find that point on a concentric circle whose radius is smaller than the one passed and argument.
This can be done by randomly generating a new radius 
newRadius = oldRadius x random.random()
and then pass the original location and this newly generated radius to the calculate_coordinates() function, which will return the coordinates of the new point in decimal degrees 

**donut_masking(*args)**

This function find a new point inside a circular crown delimited by two radiuses passed as arguments around a location passed as argument as well. 
The displacement is randomly generated thanks to random.uniform(0,2 x math.pi)

The number of the arguments is variable and the function can have to formats:

*donut_masking(latitude,longitude,internal_radius,external_radius)* where the radiuses are in kilometers with external_radius > internal_radius and the latitude and longitude are in decimal degrees
or:
*donut_masking(location,internal_radius,external_radius)* where location is the name of a city (eg : London) or an address (eg : "175 5th Avenue NYC") and the radius  radiuses are in kilometers with external_radius > internal_radius

The idea behind this function is the same as in the within_a_circle() funcion.
To find a point in the circular crown, we can generate a new radius so that   internalRadius < newRadius < externalRadius
and then pass the original location and this newly generated radius to the calculate_coordinates() function, which will return the coordinates of the new point in decimal degrees 


**standard_gaussian(*args)**

This function generates a new point on the same gaussian distribution as the one passed as argument.

The number of the arguments is variable and the function can have to formats:

*standard_gaussian(latitude,longitude,variance)* where the variance is a positive number and the latitude and longitude are in decimal degrees
or:
*standard_gaussian(location,variance)* where location is the name of a city (eg : London) or an address (eg : "175 5th Avenue NYC") and the variance is a positive number

If the function is in the second format, which can be easily understood by the number of arguments passed , we have to avail of the function find_coordinates to retrieve the correct latitude and longitude. 

The new location is found by using the numpy.random.normal() function which selects a random point on a gaussian distrubution whose peak is the pair (latitude,longitude) and the variance is the one passed as argument.

Once having found the new point, we need to make sure its latitude and longitude are in the correct range before returning them in decimal degrees. 
If not, the issue can be easily solved by calling the wrap() function passing the new coordinates as argument.

**bimodal_gaussian(*args)**

This function generates a new point on the same bimodal gaussian distribution as the one passed as argument.

The number of the arguments is variable and the function can have to formats:

*bimodal_gaussian(latitude1,longitude1,variance1,latitude2,longitude2,variance2)* where variance1 and variance2 are positive numbers and latitude1, latitude2, longitude1 and longitude2 are in decimal degrees
or:
*bimodal_gaussian(location1,variance1,location2,variance2)* where location1 and loaction2 are the names of a city (eg : London) or an address (eg : "175 5th Avenue NYC") and variance1 and variance2 are positive numbers

Since a bimodal gaussian is a mixture of two different normal distributions, the idea behind the function is to choose one of the two distrubutions and avail of the standard_gaussian() function to calculate the new point.
If the first one is chosen, we pass as arguments either location1,variance1 or latitude1,longitude1,variance1 depending on the format, if not locationr,variancer or latitude2,longitude2,variance2

















