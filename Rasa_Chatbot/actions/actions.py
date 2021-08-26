# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions




from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker , FormValidationAction
from rasa_sdk.events import SlotSet, EventType,UserUtteranceReverted, ConversationPaused
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from datetime import date,datetime,timedelta
import json

global recipient_email
recipient_email = "mata.khalili@nokia-bell-labs.com"

global user_name
user_name = "there"

global outlook_free_time 
outlook_free_time = "4 pm"

global final_date
final_date = (date.today() + timedelta(days=10)) #assume that it's withtin 10 days to deliver the parcel

global locations
locations = {'chappe':[], 'curie':['E', 'D', 'B', 'C'],'shannon':[], 
             'pascal':[], 'laplace':['East','West'],'torricelli':[], 
             'ritchie':[], 'copernic':['G','H', 'EBC'], 'bourseul':[],
             'galilee':[], 'montgomerie':[], 'huygens':[], 'newton':['F','B'] }


class AppointmentInfoForm(Action):
    def name(self) -> Text:
        return "user_details_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        required_slots = ["language","confirm_time","recipient","another_day","date", "time","location", "entrance"]

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
        Appointment_data= {'Recipient':recipient,
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
        
        return [] 


class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_details_form"

    async def validate_language(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        allowed_languages=['english','french','anglais','francais','en','fr']
        language = value.lower()
        if language in allowed_languages:
            if language == "english" or language == "anglais" or language == "en":
                return {"language":"en"}
            else:
                return {"language":"fr"}
        else:
            dispatcher.utter_message(text="Supported languages are English and French only")
            return {"language":None }
        
    async def validate_confirm_time(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value:
            Date = date.today().strftime('%Y-%m-%d')
            return {"recipient":recipient_email,"date":Date,"time": "4 pm","confirm_time": True,"another_day": False}
        else:
            return {"recipient":recipient_email,"another_day": False,"confirm_time": False }
        
        
    async def validate_date(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        Format = '%Y-%m-%d'
        if value=="Today":
            Date = date.today().strftime(Format)
            return {"date":Date}
        elif value == "Tomorrow":
            Date = (date.today() + timedelta(days=1)).strftime(Format)
            return {"date":Date}
        elif value == "Another day":
            return {"another_day": True,"date":None}
        elif value == "Another Person":
            return {"time": "Not specified yet","date": "Not specified yet",
                    "location": "Not specified yet", "entrance":"Not specified yet","recipient":None}
        else:
            # return {"date":value}
            # if tracker.get_slot("another_day"):
              try:
                Date = datetime.strptime(value, Format).date() 
                Today=date.today()
                if Date >= Today and Date <= final_date: # to make sure that the date is within the allowed period
                    return {"date":value}
                else:
                    if tracker.get_slot("language") == "en":
                       dispatcher.utter_message(text="Please enter a valid date ,date should be between "+Today.strftime('%Y-%m-%d')+" and "+final_date.strftime('%Y-%m-%d'))
                    else:
                       dispatcher.utter_message(text="Veuillez entrer une date valide, la date doit être comprise entre "+Today.strftime('%Y-%m-%d')+" et "+final_date.strftime('%Y-%m-%d'))
                    return {"date":None}
              except:
                try:
                    Format = '%d-%m-%Y'
                    Date = datetime.strptime(value, Format).date() 
                    Today=date.today()
                    if Date >= Today and Date <= final_date: # to make sure that the date is within the allowed period
                      return {"date":value}
                    else:
                      if tracker.get_slot("language") == "en":
                        dispatcher.utter_message(text="Please enter a valid date ,date should be between "+Today.strftime('%Y-%m-%d')+" and "+final_date.strftime('%Y-%m-%d'))
                      else:
                        dispatcher.utter_message(text="Veuillez entrer une date valide, la date doit être comprise entre "+Today.strftime('%Y-%m-%d')+" et "+final_date.strftime('%Y-%m-%d'))
                      return {"date":None}
                except:   
                  try:
                    Format = '%d/%m/%Y'
                    Date = datetime.strptime(value, Format).date() 
                    Today=date.today()
                    if Date >= Today and Date <= final_date: # to make sure that the date is within the allowed period
                      return {"date":value}
                    else:
                      if tracker.get_slot("language") == "en":
                        dispatcher.utter_message(text="Please enter a valid date ,date should be between "+Today.strftime('%Y-%m-%d')+" and "+final_date.strftime('%Y-%m-%d'))
                      else:
                        dispatcher.utter_message(text="Veuillez entrer une date valide, la date doit être comprise entre "+Today.strftime('%Y-%m-%d')+" et "+final_date.strftime('%Y-%m-%d'))
                      return {"date":None}
                  except:   
                    if tracker.get_slot("language") == "en":
                      dispatcher.utter_message(text="Please enter a valid date in the following format: "+Format)
                    else:
                      dispatcher.utter_message(text="Veuillez saisir la date au format suivant: "+ Format) 
                    return {"date":None}
                 
            
            
    def validate_time(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if tracker.get_slot("language") == "en":
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
                try:
                   time = datetime.strptime(value, "%I %p")
                   final_time= datetime.strftime(time, "%H:%M")
                   return{"time":final_time}
                except:
                     try:
                       time = datetime.strptime(value, "%I%p")
                       final_time= datetime.strftime(time, "%H:%M")
                       return{"time":final_time}
                     except:
                        try:
                            time = datetime.strptime(value, "%I:%M")
                            final_time= datetime.strftime(time, "%H:%M")
                            return{"time":final_time}
                        except:
                            if tracker.get_slot("language") == "en":
                               dispatcher.utter_message(text="Please enter a valid time (e.g 3:00 PM)")
                            else:
                               dispatcher.utter_message(text="Veuillez entrer une heure valide (e.g 3:00 PM)") 
                            return{"time":None}      
        else:
            try:
              x = value.index('h')
              if x==len(value)-1:
                time= value[0:x]+':'+'00'
              else:
                time = value[0:x]+ ':' + value[x+1:len(value)]
              return({"time":time})
            except:
              return({"time":value})  
        
    async def validate_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `location` value."""
        
        # If the building isn't exist
        print(f"location given = {slot_value}")
        
        building = slot_value.lower()
        
        if building in locations:
            
            if len(locations.get(building))>0:
               return{"location": slot_value}
            else:
              return {"entrance":"main","location": slot_value}
        else:
            buildings= ','.join([str(elem) for elem in locations])
            if tracker.get_slot("language") == "en":
                 dispatcher.utter_message(text="That's not valid Building. \nYou should choose one of the following: \n"+buildings)
            else:
                 dispatcher.utter_message(text="Ce n'est pas un bâtiment valide. \nVous devez choisir l'une des options suivantes: \n"+buildings)
            return {"location": None}
        

    def validate_entrance(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        try:
         Entrances= locations.get(tracker.get_slot("location").lower())
         entrances = ','.join([str(elem) for elem in Entrances])
         if value in Entrances:
             return {"entrance": value}
         else:
            if tracker.get_slot("language") == "en":
                dispatcher.utter_message(text="That's not valid Entrance. \nYou should choose one of the following: \n"+entrances)
            else:
                dispatcher.utter_message(text="Ce n'est pas une entrée valide. \n Vous devez choisir l'un des éléments suivants : \n"+entrances)
            return {"entrance": None}
        except:
            return {"entrance": None}
                
        
class ActionCustomFallback(Action):

    def name(self) -> Text:
        return "action_custom_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(template="utter_custom")
        
        return[UserUtteranceReverted()]  # to consider it a fallback action
    

    

   
