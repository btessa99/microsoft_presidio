
# COORDINATES ANONYMIZATION

The following functions were implemented with the help of **GeoPy**, a Python client useful for geocoding web services since it provides means not only to locate the coordinates of an address, a city or a country but also to do the reverse operation and measure distances.

Let's now introduce the functions:

- `find_coordinates(location)` 

Given a location in the form of a string , it returns its latitude and longitude in decimal degrees.

- `wrap(latitude,longitude)`

This function is called if either or both the input parameters are out of range need to be put in range. 

The correct values of the inputs in decimal degrees are returned.

- `calculate_coordinates(*args)`

Generates a new point on a circle around the original location, passed the form of a string or latitude and longitude together with the radius of the circle.

- `within_a_circle(*args)`

Generates a new point within a circle around the original location 

A `calculate_coordinates(*args)`is used to 

- `donut_masking(*args)`

Generates a new point on a circular crown around the original location

- `standard_gaussian(*args)`

Generates a point on a standard gaussian whose peak is the original location

- `bimodal_gaussian(*args)`

Generates a new point on the same bimodal gaussian distribution as the one passed as argument.


# INSTALLATION

  Anonymizer and Working Enviroment:

  `$ pip3 install --upgrade pip`

  `$ pip3 install presidio-anonymizer`

  `$ pip3 install spacy numpy`

  `$ python3 -m spacy download en_core_web_lg`
  
  Geopy:
  
  `$ pip3 install geopy`
  
  Now that the set up is complete!
  
  # SOME EXAMPLES
  
  
  
















