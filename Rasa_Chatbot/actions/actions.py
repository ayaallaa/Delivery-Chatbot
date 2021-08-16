# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions




from typing import Any, Text, Dict, List, Union
from datetime import date,datetime
from rasa_sdk import Action, Tracker , FormValidationAction
from rasa_sdk.events import SlotSet, EventType,UserUtteranceReverted, ConversationPaused
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from datetime import date,timedelta
import json
    
global user_name
user_name = "Hager"

global outlook_free_time 
outlook_free_time = "4 pm"

class AppointmentInfoForm(Action):
    def name(self) -> Text:
        return "user_details_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        required_slots = ["confirm_exercise","recipient","date","confrim_another_day", "time","location", "entrance"]

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
        
        recipient=tracker.get_slot("recipient")
        date =tracker.get_slot("date")
        time=tracker.get_slot("time")
        building=tracker.get_slot("location")
        entrance= tracker.get_slot("entrance")
        
        dispatcher.utter_message(response="utter_details_thanks",
                                  Recipient=recipient,
                                  Date =date,
                                  Time=time,
                                  Location=building,
                                  Entrance= entrance)
        
        # try to add data to json file in the following format
        output=[]
        Appointment_data= {'Recipant':recipient,
                           'Date':date,
                           'Time':time,
                           'Building':building,
                           'Entrance':entrance}
        output.append(Appointment_data)
        json_output = json.dumps(output, indent = 6)

        # Writing to Output.json in a file
        with open("Appointment_details.json", "w") as outfile:
          outfile.write(json_output)
        return [ConversationPaused()]
        
class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_greet",
                                 name=user_name)
        
        return[UserUtteranceReverted()]  # to consider it a fallback action


class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_details_form"


    async def validate_confirm_time(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value:
            Date = date.today().strftime('%Y-%m-%d')
            return {"recipient":user_name,"date":Date,"time": "4pm","confirm_time": True}
        else:
            # dispatcher.utter_message(buttons = [
            #         {"payload": '/Date{{"date":"Today"}}', "title": "Today"},
            #         {"payload": '/Date{{"date":"Another Day"}}', "title": "Another Day"},])
            return {"recipient":user_name,"confirm_time": False }
        
        
    async def validate_date(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value=="Today":
            Date = date.today().strftime('%Y-%m-%d')
            return {"date":Date}
        elif value == "Tomorrow":
            Date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
            return {"date":Date}
        elif value == "Another day":
            dispatcher.utter_message(text="Please enter a valid date in the following format %Y-%m-%d")
            return {"date":None}
        elif value == "Another Person":
            return {"time": "Not specified yet","date": "Not specified yet",
                    "location": "Not specified yet", "entrance":"Not specified yet","recipient":None}
        else:
            try:
               Date = datetime.strptime(value, '%Y-%m-%d').date()
               return {"date":Date}
            except:
               dispatcher.utter_message(text="Please enter a valid date in the following format %Y-%m-%d")
               return {"date":None}
            
            
    def validate_time(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        try:
          time = datetime.strptime(value, "%I:%M %p")
          final_time= datetime.strftime(time, "%H:%M")
          return{"time":final_time}
        except:
            try:
               time = datetime.strptime(value, "%I:%M%p")
               final_time= datetime.strftime(time, "%H:%M")
               return{"time":final_time}
            except:
               dispatcher.utter_message(text="please enter valid time")
               return{"time":None}      
        
        
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
        
        building = slot_value.lower()
        
        if building in self.locations:
            
            if len(self.locations.get(building))>0:
               if building == 'curie':
                     dispatcher.utter_message(buttons = [
                     {"payload": "/Entrance{'entrance':'E'}", "title": "E","type": "postBack"},
                     {"payload": "/Entrance{'entrance':'B'}", "title": "B","type": "postBack"},
                     {"payload": "/Entrance{'entrance':'C'}", "title": "C","type": "postBack"},
                     {"payload": "/Entrance{'entrance':'D'}", "title": "D","type": "postBack"},])
               elif building == 'laplace':
                   dispatcher.utter_message(buttons = [
                     {"payload": "/Entrance{'entrance':'East'}", "title": "East","type": "postBack"},
                     {"payload": "/Entrance{'entrance':'West'}", "title": "West","type": "postBack"},
                     ])
               elif building == 'copernic':
                   dispatcher.utter_message(buttons = [
                     {"payload": "/Entrance{'entrance':'G'}", "title": "G","type": "postBack"},
                     {"payload": "/Entrance{'entrance':'H'}", "title": "H","type": "postBack"},
                     {"payload": "/Entrance{'entrance':'EBC'}", "title": "EBC","type": "postBack"},
                     ])
               elif building == 'newton':
                   dispatcher.utter_message(buttons = [
                     {"payload": "/Entrance{'entrance':'F'}", "title": "F","type": "postBack"},
                     {"payload": "/Entrance{'entrance':'B'}", "title": "B","type": "postBack"},
                     ])
            #   return{"location": slot_value}
            else:
              return {"entrance":"main","location": slot_value}
        else:
            dispatcher.utter_message(text="That's not valid Building. \nYou should choose one of the following: \n['Chappe', 'Curie', 'Shannon', 'Pascal', 'Laplace', 'Torricelli','Ritchie', 'Copernic', \n'Bourseul', 'Galilee', 'Montgomerie', 'Huygens', 'Newton'].")
            return {"location": None}
        

    def validate_entrance(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        Entrances= self.locations.get(tracker.get_slot("location").lower())
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
    

    

   
