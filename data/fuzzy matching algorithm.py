# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 14:11:24 2021

@author: haabdela
"""

from bof.fuzz import Process

p = Process()

locations = {'Chappe':[], 'Curie':['E', 'D', 'B', 'C'],'Shannon':[], 
             'Pascal':[], 'Laplace':['East','West'],'Torricelli':[], 
             'Ritchie':[], 'Copernic':['G','H', 'EBC'], 'Bourseul':[],
             'Galilee':[], 'Montgomerie':[], 'Huygens':[], 'Newton':['F','B'] }

e=p.extractOne("I would prefer the Curie", [*locations],score_cutoff=1)

print(e)
print(locations[e[0]])
