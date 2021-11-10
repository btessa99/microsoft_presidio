
# COORDINATES ANONYMIZATION

The Anonymizer module can be extended by creating a new PII Operator, which is in its turn an extention of the abstract class Operator.

By default, it transorms the coordinates into the string <GEO_COORDINATES> but, if specified, can put into practise more sophosticated anonymisations thanks to functions implemented with the help of **GeoPy**, a Python client useful for geocoding web services since it provides means not only to locate the coordinates of an address, a city or a country but also to do the reverse operation and measure distances.

Let's now describe them:

- #### `find_coordinates(self,location)` 

    Given a location in the form of a string representing a city name or an address , it returns its latitude and longitude in decimal degrees.
    
- #### `get_dd_coordinates(self,location)`

    Given a locations return its coordinates in decimal degrees.
    
- #### `from_dms_to_dd(self,coordinate_dms)`
    
    Converts a coordinate from decimal minutes seconds format to decimal degrees
    The parameter coordinate_dms is the latitude or longitude to convert

- #### `wrap(self,latitude,longitude)`

    This function is called if either or both the input parameters are out of range need to be put in range. 

    The normalisation of the longitude requires adding or subtracting 360 to the value until it's normalised while the latitude requires flipping the longitude whenever it           crosses a pole.

    The correct values of the inputs in decimal degrees are returned.

- #### `calculate_coordinates(self,*args)`

    Possible values of args:
    
    case 2 parameters:
        a city or an address (string)
        radius in kilometers(float)

    case 3 parameters:
        latitude (float/integer if it's in decimal degrees or string if it's in decimal minutes seconds)
        longitude float/integer if it's in decimal degrees or string if it's in decimal minutes seconds)
        radius in kilometers(float/integer)
        

    Generates a new point on a circle around the original location, passed the form of a string or latitude and longitude together with the radius of the circle.
    First, creates a new geodetic point representing the original location and sets the distance between the two points.

    Afterwards, selects a random bearing and finally calculates a new latidude and longitude according to the Great Circle Navigation Formulae.

    The function returns the two coordinates in decimal degrees.

- #### `within_a_circle(self,location,radius)`

    location: a string representing a pair of coordinates separated by a comma, a city name or an address
    radius: integer or float representing the radius of the circle

    Generates a new point within a circle around the original location.
    
    After having randomly generated a new radius smaller than the one passed as argument,the calculate_coordinates() function is called to find the new coordinates; this way         the resulting point will be inside the circle.
    
    The function returns the two coordinates in decimal degrees.

- #### `donut_masking(self,location,internal_radius,external_radius)`

    location: a string representing a pair of coordinates separated by a comma, a city name or an address
    internal_radius: integer or float representing the internal radius of the circlular crown
    external_radius: integer or float representing the external radius of the circlular crown

    Generates a new point on a circular crown around the original location.
    
    Just like in the previously described function, the idea behind this is to generate randomly a new radius, smaller than the external one and greater than the internal one,       and then call the calculate_coordinates() function to get the coordinates of a point inside the circlular crown.
    
    The function returns the two coordinates in decimal degrees.

- #### `standard_gaussian(self,location,variance)`

  location: a string representing a pair of coordinates separated by a comma, a city name or an address
  variance: an integer representing the variance of the gaussian

  Generates a point on a standard gaussian whose peak is the original location.

  It simply chooses a random point in the gaussian and returns its coordinated in decimal degrees.

- #### `bimodal_gaussian(self,location1,variance1,location2,variance2)`
    
    
  location: a string representing a pair of coordinates separated by a comma, a city name or an address
  variance: an integer representing the variance of the gaussian


  location: a string representing a pair of coordinates separated by a comma, a city name or an address
  variance: an integer representing the variance of the gaussian

    Generates a new point on the same bimodal gaussian distribution as the one passed as argument.

    Since a bimodal is composed of two standard distributions, the idea is to randomly choose one and call the standard_gaussian() function to find the new coordinates and           return them.
    
    
If only the latitude or longitude is given as a input to one of the functions, the single anonymized coordinate in DMS is returned


 ## INSTALLATION

 #### Working Enviroment:

`$ pip install presidio_anonymizer`

`$ pip install numpy`

`$ python -m spacy download en_core_web_lg`

`$ python -m spacy download it_core_news_sm`

`$ git clone https://github.com/btessa99/microsoft_presidio.git`

`$ pip3 install geopy`
    
## AN EXAMPLE
    
Let's supposed we have this text to anonimyze:

`The city center lies approximately on latitude 7° 30' N and longitude 30° 54' E. the humid lowland rain forest region with two distinctive seasons`

and we want to replace the coordinates with a latiude and a longitude of a point 2 km distant from that city.

Then this could be simply done by adding the following snippet in our code:

        anonymized_results = anonymizer.anonymize(
            text,
            analyzer_results,            
            operators={"GEO_COORDINATES": OperatorConfig("geocoordinates",{ 
                "function" : "calculate_coordinates",
                "radius" : 3}        
        )})

Where the parameter analyzer_results are he results we received from the analyzer.

The output of the anonimyzation will be:

 `The city center lies approximately on latitude 45.52546737261428,12.624420050010388 and longitude 45.88088086665235,9.342043850962508. the humid lowland rain forest region with two distinctive seasons`
 
 Another example could be:
 
    text = `Born Napoleone di Buonaparte on the island of Corsica not long after its annexation by the Kingdom of France, Napoleon's modest family descended from minor Italian nobility`

Then we would need to write:

        
        anonymized_results = anonymizer.anonymize(
            text,
            analyzer_results,            
            operators={"LOCATION": OperatorConfig("geocoordinates",{ 
                "function" : "calculate_coordinates",
                "radius" : 3.5}        
        )})
        
And the output would be:

`Born <PERSON> on the island of 42.21497975066536,9.07137801261379 not long after its annexation by 47.124156925535814,-1.2649809338908713, Napoleon's modest family descended from minor <NRP> nobility`
    
    
    
## PARAMETERS FOR EACH FUNCTION:

- #### calculate_coordinates:

"function" : "calculate_coordinates"
"radius" : an integer or a float
                
- #### within_a_circle:

"function" : "within_a_circle"
"radius" : an integer or a float
                
- #### donut_masking:

"function" : "donut_masking"
"radius" : internal radius. An integer or a float
"radius2" : external radius. An integer or a float
                
- #### standard_gaussian:

"function" : "standard_gaussian"
"variance" : an integer or a float
                
- #### bimodal_gaussian:

"function" : "bimodal_gaussian"
"variance" : an integer or a float
"location2" : a string representing a pair of coordinates separated by a comma, a city name or an address
"variance2" : an integer or a float


    
    
