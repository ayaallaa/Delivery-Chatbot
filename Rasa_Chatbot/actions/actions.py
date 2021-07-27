# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions




from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker , FormValidationAction
from rasa_sdk.events import SlotSet, EventType,UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

# class Actionlocation(Action):

#     def name(self) -> Text:
#         return "action_choose_location"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         entities=tracker.latest_message['entities']
#         print(entities)
        
#         # locations = {'Chappe':[], 'Curie':['E', 'D', 'B', 'C'],'Shannon':[], 
#         #               'Pascal':[], 'Laplace':['East','West'],'Torricelli':[], 
#         #               'Ritchie':[], 'Copernic':['G','H', 'EBC'], 'Bourseul':[],
#         #               'Galilee':[], 'Montgomerie':[], 'Huygens':[], 
#         #               'Newton':['F','B'] }
        
        
        
#         for e in entities:
            
#             if e['entity'] =='location':
#                 location=e['value'].lower()
                
#             if location == 'curie' or location == 'laplace' or location == 'copernic':
#                  entrance = ', please choose entrance'
                
#             message = 'Building is ' + location + entrance
            
#             print("Building: ",tracker.get_slot('location'))
#             print(tracker.latest_message['text'])
#         dispatcher.utter_message(text=message)

#         return []
    

class AppointmentInfoForm(Action):
    def name(self) -> Text:
        return "user_details_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
       
        # outlook_free_time = "10 am"
        
        # SlotSet("requested_slot", "confirm_exercise")
        # if tracker.get_slot('confirm_time') == True:
        #       required_slots = ["confirm_time","location"]
        # else:
        #    required_slots = ["confirm_exercise", "time","location"]
        
        # required_slots = ["confirm_exercise", "time","location"]
        required_slots = ["time","location"]
        for slot_name in required_slots:

            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
              
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]
    
    # @staticmethod
    # def required_slots(tracker):

    #       if tracker.get_slot('confirm_time') == True:
    #         return ["confirm_time", "location"]
    #       else:
    #         return ["confirm_exercise", "time",
    #           "location"]
        
    # def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        
    #       return {
    #         "confirm_time": [
    #             self.from_intent(intent="affirm", value=True),
    #             self.from_intent(intent="deny", value=False)
    #                  ]
            # "time": [
            #     self.from_entity(entity="time")
            # ],
            # "location": [
            #     self.from_entity(entity="location")
            # ]
            # }
     
    #  def submit(
    #     self,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: Dict[Text, Any],
    # ) -> List[Dict]:

    #     confirm_time = tracker.get_slot("confirm_time")
    #     time = tracker.get_slot("time")
    #     location = tracker.get_slot("location")

    #     dispatcher.utter_message("Thanks, your answers have been recorded!")
    #     return []
    
class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_details_thanks",
                                  Time=tracker.get_slot("time"),
                                  Location=tracker.get_slot("location"))
        


class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_details_form"

    def validate_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `location` value."""
        
        locations = {'chappe':[], 'curie':['E', 'D', 'B', 'C'],'shannon':[], 
             'pascal':[], 'laplace':['East','West'],'torricelli':[], 
             'ritchie':[], 'copernic':['G','H', 'EBC'], 'bourseul':[],
             'galilee':[], 'montgomerie':[], 'huygens':[], 'newton':['F','B'] }
        
        # If the building isn't exist
        print(f"location given = {slot_value}")
        if slot_value.lower() in locations:
            return {"location": slot_value}
        else:
            dispatcher.utter_message(text="That's not valid Building. \nYou should choose one of the following: \n['Chappe', 'Curie', 'Shannon', 'Pascal', 'Laplace', 'Torricelli','Ritchie', 'Copernic', \n'Bourseul', 'Galilee', 'Montgomerie', 'Huygens', 'Newton'].")
            return {"location": None}
        

    # async def validate_confirm_time(
    #     self,
    #     value: Text,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: Dict[Text, Any],
    # ) -> Dict[Text, Any]:
    #     if value:
    #         return {"confirm_time": True}
    #     else:
    #         return {"time": "None", "confirm_time": False }
        
        
        
class ActionCustomFallback(Action):

    def name(self) -> Text:
        return "action_custom_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(template="utter_custom")
        
        return[UserUtteranceReverted()]  # to consider it a fallback action

   
