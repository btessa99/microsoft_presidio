
from random import uniform
from re import X
import unittest
from funzioni import *
import geopy.distance
from geopy.point import Point
import numpy


class TestSum(unittest.TestCase):

    def test_calculate_coordinates(self):

        print('Testing function calculate_coordinates')

        for i in range (0,10):

               
            lat = uniform(-90,90)
            #print('latitude: ',lat)

            lon = uniform(-180,180)
            #print('latitude: ',lon)

            radius = random.random() * 10
            #print('radius: ',radius)

            l1,l2 = calculate_coordinates(self,lat,lon,radius)
            p1 = Point(lat,lon)
            p2 = Point(l1,l2)
            distance =geopy.distance.great_circle(p1,p2).kilometers
            #print()
            
            assert round(distance,0) == round(radius,0), 'The distance does not equal the raius'



    def test_within_a_circle(self):

        print('Testing function within_a_circle')

        for i in range (0,10):
    
            #print('Testing function within_a_circle. Test N ' ,i+1)
               
            lat = uniform(-90,90)
            #print('latitude: ',lat)

            lon = uniform(-180,180)
            #print('latitude: ',lon)

            radius = random.random() * 10
            #print('radius: ',radius)

            location = str(lat) + "," + str(lon)

            l1,l2 = within_a_circle(self,location,radius)
            p1 = Point(lat,lon)
            p2 = Point(l1,l2)
            distance =geopy.distance.great_circle(p1,p2).kilometers
            #print('with ', radius)
            #print()

            assert distance < radius , 'The distance is not lower than the radius'


    def test_donut_masking(self):

        print('Testing function donut_masing')
 
        for i in range (0,10):
        
               
            lat = uniform(-90,90)
            #print('latitude: ',lat)

            lon = uniform(-180,180)
            #print('latitude: ',lon)

            int_radius = random.random() * 10
            #print('internal radius: ',int_radius)

            ext_radius = int_radius + random.random() * 10
            #print('external radius: ',ext_radius)

            location = str(lat) + "," + str(lon)

            l1,l2 = donut_masking(self,location,int_radius,ext_radius)
            p1 = Point(lat,lon)
            p2 = Point(l1,l2)
            distance =geopy.distance.great_circle(p1,p2).kilometers

            #print()

            assert distance < ext_radius and distance > int_radius , 'The distance is not in between the internal and radius'
        



if __name__ == '__main__':
    unittest.main()