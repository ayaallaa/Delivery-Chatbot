# Microsoft Delivery Chatbot

This bot project was created using the Core Bot with Azure Language Understanding template, and contains support for a base set of conversational flows.


## Start building the bot

Composer can help guide you through getting started building your bot.
1. Download Composer
2. Prerequisites
  Before you get started, you need to install
  - nodejs
  - .NET Core SDK
 
 the great resource to gett start is the **[guided tutorial](https://docs.microsoft.com/en-us/composer/tutorial/tutorial-introduction)** in Microsoft Bot framework Composer documentation.
### Create Dialogs

The bot is built from a series of components called dialogs. Each dialog encapsulates some bot functionality, such as sending a response, prompting a user for text, making an HTTP request, or maybe all of these.

### create Triggers

In Bot Framework Composer, each dialog includes one or more event handlers called triggers. Each trigger contains one or more actions. Actions are the instructions that the bot will execute when the dialog receives any event that it has a trigger defined to handle. Once a given event is handled by a trigger.

### Add language understanding data 

Language understanding (LU) is used by a bot to understand language naturally and contextually to determine what to do next in a conversation flow. In Bot Framework Composer, the process is achieved through setting up recognizers and providing training data in the dialog so that the intents and entities contained in the message can be captured. These values will then be passed on to triggers which define how the bot responds using the appropriate actions.


## Publish your bot to Azure from Composer

Composer can help you provision the Azure resources necessary for your bot, and publish your bot to them. To get started, create a publishing profile from your bot settings page in Composer . Make sure you only provision the optional Azure resources you need!
How to publish the bot : Publish a bot to Azure(https://docs.microsoft.com/en-us/composer/how-to-publish-bot?tabs=v2x)

## Connect with your users

the bot comes pre-configured to connect to  Web Chat and DirectLine channels, but there are many more places can connect the bot to - including Microsoft Teams, Telephony,  Facebook, Outlook and more.
How to connect the bot to microsoft: Connect a bot to Microsoft Teams(https://docs.microsoft.com/en-us/azure/bot-service/channel-connect-teams?view=azure-bot-service-4.0)

