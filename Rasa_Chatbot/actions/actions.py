# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions



from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from bof.fuzz import Process


class Actionlocation(Action):

    def name(self) -> Text:
        return "action_choose_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        entities=tracker.latest_message['entities']
        print(entities)
        
        
        
        for e in entities:
            
            entrance = ''
            if e['entity'] =='location':
                location=e['value']
            if location == 'curie' or location == 'laplace' or location == 'copernic':
                 entrance = ', please choose entrance'
                
            message = 'Building is ' + location + entrance
            
        dispatcher.utter_message(text=message)

        return []
    
# class Actionlocation(Action):

#     def name(self) -> Text:
#         return "action_choose_location"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        

#         # p = Process()
        
#         m=tracker.latest_message.text
        
        
#         # locations = {'Chappe':[], 'Curie':['E', 'D', 'B', 'C'],'Shannon':[], 
#         #              'Pascal':[], 'Laplace':['East','West'],'Torricelli':[], 
#         #              'Ritchie':[], 'Copernic':['G','H', 'EBC'], 'Bourseul':[],
#         #              'Galilee':[], 'Montgomerie':[], 'Huygens':[], 
#         #              'Newton':['F','B'] }

#         # e=p.extractOne(m, [*locations],score_cutoff=1)

#         # print(e)
#         # print(locations[e[0]])

            
#         dispatcher.utter_message(text=m)

#         return []
