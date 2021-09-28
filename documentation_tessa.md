
# COORDINATES DOCUMENTATION

The following functions were implemented with the help of **GeoPy**, a Python client useful for geocoding web services since it provides means not only to locate the coordinates of an address, a city or a country but also to do the reverse operation and measure distances.

Let's now introduce the functions:

- `find_coordinates(location)` 

Given the location, it returns the pair (latitude,longitude) in decimal degrees.

- `wrap(latitude,longitude)`

This function is called whether one of the two parameters(or both) is out of range and its needs to be put in range.

- `calculate_coordinates(*args)`

Generates a new point on a circle around the original location

- `within_a_circle(*args)`

Generatse a new point within a circle around the original location

- `donut_masking(*args)`

Generates a new point on a circular crown around the original location

- `standard_gaussian(*args)`

Generates a point on a standard gaussian whose peak is the original location

- `bimodal_gaussian(*args)`

Generates a new point on the same bimodal gaussian distribution as the one passed as argument.


# INSTALLATION

  Working Enviroment:

  `$ pip3 install --upgrade pip`

  `$ pip3 install presidio-anonymizer`

  `$ pip3 install spacy numpy`

  `$ python3 -m spacy download en_core_web_lg`
  
  Geopy:
  
    `$ pip3 install geopy`
  
  
  
















