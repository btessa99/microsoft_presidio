
# COORDINATES ANONYMIZATION

The following functions were implemented with the help of **GeoPy**, a Python client useful for geocoding web services since it provides means not only to locate the coordinates of an address, a city or a country but also to do the reverse operation and measure distances.

Let's now introduce the functions:

- #### `find_coordinates(location)` 

    Given a location in the form of a string , it returns its latitude and longitude in decimal degrees.

- #### `wrap(latitude,longitude)`

    This function is called if either or both the input parameters are out of range need to be put in range. 

    The normalisation of the longitude requires adding or subtracting 360 to the value until it's normalised while the latitude requires flipping the longitude whenever it           crosses a pole.

    The correct values of the inputs in decimal degrees are returned.

- #### `calculate_coordinates(*args)`

    Generates a new point on a circle around the original location, passed the form of a string or latitude and longitude together with the radius of the circle.
    First, creates a new geodetic point representing the original location and sets the distance between the two points.

    Afterwards, selects a random bearing and finally calculates a new latidude and longitude according to the Great Circle Navigation Formulae.

    The function returns the two coordinates in decimal degrees.

- #### `within_a_circle(*args)`

    Generates a new point within a circle around the original location.
    
    After having randomly generated a new radius smaller than the one passed as argument,the calculate_coordinates() function is called to find the new coordinates; this way         the resulting point will be inside the circle.
    
    The function returns the two coordinates in decimal degrees.

- #### `donut_masking(*args)`

    Generates a new point on a circular crown around the original location.
    
    Just like in the previously described function, the idea behind this is to generate randomly a new radius, smaller than the external one and greater than the internal one,       and then call the calculate_coordinates() function to get the coordinates of a point inside the circlular crown.
    
    The function returns the two coordinates in decimal degrees.

- #### `standard_gaussian(*args)`

   Generates a point on a standard gaussian whose peak is the original location.
   
   It simply chooses a random point in the gaussian and returns its coordinated in decimal degrees.

- #### `bimodal_gaussian(*args)`

    Generates a new point on the same bimodal gaussian distribution as the one passed as argument.
    
    Since a bimodal is composed of two standard distributions, the idea is to randomly choose one and call the standard_gaussian() function to find the new coordinates and           return them.


 ## INSTALLATION

 #### Working Enviroment:

`$ pip install presidio_analyzer`

`$ pip install presidio_anonymizer`

`$ python -m spacy download en_core_web_lg`

 #### Analyzer Entity Recognizer set up:


 #### Anonymizer PII Operator set up:

 #### Geopy:

`$ pip3 install geopy`
