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
        #     required_slots = ["confirm_exercise", "time","location"]
        
        required_slots = ["confirm_exercise", "time","location", "entrance"]
        # required_slots = ["time","location"]
        for slot_name in required_slots:

            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
              
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]
    
   
    
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
                                  Confirmed=tracker.get_slot("confirm_time"),
                                  Time=tracker.get_slot("time"),
                                  Location=tracker.get_slot("location"),
                                  Entrance= tracker.get_slot("entrance") )
        


class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_details_form"

    async def validate_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `location` value."""
        
        self.locations = {'chappe':[], 'curie':['E', 'D', 'B', 'C'],'shannon':[], 
             'pascal':[], 'laplace':['East','West'],'torricelli':[], 
             'ritchie':[], 'copernic':['G','H', 'EBC'], 'bourseul':[],
             'galilee':[], 'montgomerie':[], 'huygens':[], 'newton':['F','B'] }
        
        # If the building isn't exist
        print(f"location given = {slot_value}")
     
        if slot_value.lower() in self.locations:
            if len(self.locations.get(slot_value.lower()))>0:
              return{"location": slot_value}
            else:
              return {"entrance":"No entrance","location": slot_value}
        else:
            # dispatcher.utter_message(image="https://i.imgur.com/nGF1K8f.jpg")
            dispatcher.utter_message(text="That's not valid Building. \nYou should choose one of the following: \n['Chappe', 'Curie', 'Shannon', 'Pascal', 'Laplace', 'Torricelli','Ritchie', 'Copernic', \n'Bourseul', 'Galilee', 'Montgomerie', 'Huygens', 'Newton'].")
            return {"location": None}
        

    async def validate_confirm_time(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value:
            return {"time": "10 am","confirm_time": True}
        else:
            return {"confirm_time": False }
        
    def validate_entrance(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        Entrances= self.locations.get(tracker.get_slot("location"))
        if value in Entrances:
            return {"entrance": value}
        else:
            dispatcher.utter_message(text="That's not valid Entrance. \nYou should choose one of the following: \n{Entrances}.")
            return {"entrance": None}
        
        
        
class ActionCustomFallback(Action):

    def name(self) -> Text:
        return "action_custom_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(template="utter_custom")
        
        return[UserUtteranceReverted()]  # to consider it a fallback action

   
