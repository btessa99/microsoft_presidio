"""Replaces the PII text with function result."""
from typing import Dict
from anonymizer_functions import *


from presidio_anonymizer.operators import Operator, OperatorType
from presidio_anonymizer.entities import InvalidParamException

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
from presidio_anonymizer.services.validators import validate_parameter


class Geocoordinates(Operator):

    FUNCTION = "function"
    LOCATION2 = "location2"
    RADIUS = "radius"
    RADIUS2 = "radius2"
    VARIANCE = "variance"
    VARIANCE2 = "variance2"
 

    def operate(self, text: str = None, params: Dict = None) -> str:

        function = params.get(self.FUNCTION)
        if(not function):
            return "<GEO_COORDINATES>"
        else:
            l1,l2 = 0,0

        if(function == "calculate_coordinates"):
            l1,l2 = calculate_coordinates(self,text,params.get(self.RADIUS))
        elif(function == "within_a_circle"):
            l1,l2 = within_a_circle(self,text,params.get(self.RADIUS))
        elif(function == "donut_masking"):
            l1,l2 = donut_masking(self,text,params.get(self.RADIUS),params.get(self.RADIUS2))
        elif(function == "standard_gaussian"):
            l1,l2 = standard_gaussian(self,text,float(params.get(self.VARIANCE)))
        else:
            l1,l2 = bimodal_gaussian(self,text,float(params.get(self.VARIANCE)),params.get(self.LOCATION2),params.get(self.VARIANCE2))

        if(l1 == 0):
            return str(l2)
        elif(l2 == 0):
            return str(l1)
        else:
            return str(l1) + "," + str(l2)

    def validate(self, params: Dict) -> None:

        function = params.get(self.FUNCTION)
 
        if(function):

            #validate_parameter
            if(function == "calculate_coordinates" or function == "within_a_circle" or function == "donut_masking" ):
                if(not params.get(self.RADIUS) or params.get(self.RADIUS) <= 0 ):
                    raise InvalidParamException("Invalid Radius")

                if(function == "donut_masking"):
                    if(not params.get(self.RADIUS2) or params.get(self.RADIUS2) <= 0 or params.get(self.RADIUS2) <= params.get(self.RADIUS)):
                        raise InvalidParamException("Invalid External Radius")

            elif( function == "standard_gaussian" or function == "bimodal_gaussian"):
                if(not params.get(self.VARIANCE) or params.get(self.VARIANCE) <= 0):
                    raise InvalidParamException("Invalid Variance")

                if(function == "bimodal_function"):

                    if(not params.get(self.CITY)):
                        raise InvalidParamException("Second Location not specified")

                    if(not params.get(self.VARIANCE2) or float(params.get(self.VARIANCE2)) <= 0 ):
                         raise InvalidParamException("Invalid Second Variance")
            
            else:
                  raise InvalidParamException("Unknown function")






    def operator_name(self) -> str:
        """Return operator name."""
        return "geocoordinates"

    def operator_type(self) -> OperatorType:
        """Return operator type."""
        return OperatorType.Anonymize

 