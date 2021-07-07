# Rasa Delivery Chatbot
 
## Rasa Architecture:

![Rasa Architecture](https://github.com/ayaallaa/Delivery-Chatbot/blob/main/Rasa_Chatbot/images/rasa%20architecture.png?raw=true)

Rasa has two main components:

1. Rasa NLU (Natural Language Understanding): Rasa NLU is an open-source natural language processing tool for intent classification (decides what the user is asking), extraction of the entity from the bot in the form of structured data and helps the chatbot understand what user is saying.

2. Rasa Core: a chatbot framework with machine learning-based dialogue management which takes the structured input from the NLU and predicts the next best action using a probabilistic model like LSTM neural network rather than if/else statement. Underneath the hood,  it also uses reinforcement learning to improve the prediction of the next best action.

## Files: 

1. actions.py: This file is used for creating custom actions. In case you want to call an external server or fetch external API data, you can define your actions here.

2. config.yml: This file defines the configuration of the NLU and core model. If you are using any model outside the NLU model, you have to define the pipeline here.

3. credentials.yml: This file is used to store credentials for connecting to external services such as Facebook Messenger, Slack, etc

4. data/nlu.md: In this file, we define our intents (what the user could ask the bot to do? ).  These intents are then used in training the NLU model.

5. data/stories.md: Stories are the sample conversation between a user and bot in the form of intents, responses and actions. Rasa stories are a form of training data used to train the Rasa’s dialogue management models.

6. domain.yml: This file lists the different intent (the things which you expect from the user) with bot’s responses and actions which it can perform.

7. endpoints.yml: This defines the details for connecting channels like Slack, FB messenger, etc. for storing chats data in the online databases like Redis, etc.

8. models/<timestamps>.tar.gz: the initial model, all the trained models stored in the models folder. For retraining the model, we use rasa train command.


## Rasa Command lines:

https://rasa.com/docs/rasa/command-line-interface


## Getting Started: 

1. Install Rasa:

   How to Install Rasa: https://rasa.com/docs/rasa/user-guide/installation/

2. Train the model: (if anything changed in nlu,domain or stories files we should train the models again)

   ``rasa train``

3. Open a second terminal window and start the action server: (if anything changed in the actions file we should restart the action server only)

   ``rasa run actions``

4. Return to the first terminal window and start the assistant on the command line:

   ``rasa shell``
