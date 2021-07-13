# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 14:11:24 2021

@author: hager abdelazim
"""

from bof.fuzz import Process

p = Process()

locations = {'Chappe':[], 'Curie':['E', 'D', 'B', 'C'],'Shannon':[], 
             'Pascal':[], 'Laplace':['East','West'],'Torricelli':[], 
             'Ritchie':[], 'Copernic':['G','H', 'EBC'], 'Bourseul':[],
             'Galilee':[], 'Montgomerie':[], 'Huygens':[], 'Newton':['F','B'] }

# e=p.extractOne("I would prefer the Curie", [*locations],score_cutoff=1)

# print(e)
# print(locations[e[0]])

print(locations.keys())
print(locations.values()) 

Building = 'Curie'

if Building in locations:   #to check if the building exists
  print ("Key exists")
  print(locations.get(Building))
  print(len(locations.get(Building)))
else:
  print ("Key does not exist")
  
# OR

# if locations.has_key(Building):   ## has_key removed from python 3
#   print ("Key exists")
# else:
#   print ("Key does not exist")
  


'''
Dict_Functions:
--------------
clear() 	--> Removes all the elements from the dictionary
copy()  	--> Returns a copy of the dictionary
fromkeys()	--> Returns a dictionary with the specified keys and value
get()	    --> Returns the value of the specified key
items()	    --> Returns a list containing a tuple for each key value pair
keys()	    --> Returns a list containing the dictionary's keys
pop()	    --> Removes the element with the specified key
popitem()   -->	Removes the last inserted key-value pair
setdefault()-->	Returns the value of the specified key. If the key does not exist: 
                insert the key, with the specified value
update()	--> Updates the dictionary with the specified key-value pairs
values()	--> Returns a list of all the values in the dictionary
'''
