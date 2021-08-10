# Rasa Integration with Microsoft Teams
To integrate the Rasa chatbot on Microsoft Teams, firstly we will have to create and application on MS teams so that we can setup and install our app on MS teams to talk to the bot.
 
## CREATING AN APP FOR MICROSOFT TEAMS:

### link for video to show the steps in details: 

https://www.youtube.com/watch?v=JiACbrwBQ1A&t=1223s

1. Firstly make sure that you have MS teams installed on your system. Then open MS teams and login through the Microsoft credentials. Once you are logged in you can see the “Apps” icon on the bottom left on the application, just click on it.

2. In the search bar, search for the “App Studio” and click on it. Then a pop up window will open asking you to create it or to open it if you have already created it before.

3. Now, a new window will appear, go to “Manifest editor” and select “Create a new app”.

4. Now fill the app details as shown here in the images.

![App Details](https://github.com/ayaallaa/Delivery-Chatbot/blob/main/Rasa_Chatbot/images/App%20details1.png?raw=true)
![App Details](https://github.com/ayaallaa/Delivery-Chatbot/blob/main/Rasa_Chatbot/images/App%20details2.png?raw=true)

5. Now, go to Bots and setup the endpoint for the rasa chatbot which is alive and ready to talk to. Here you will get the app_id and app_password(after generating), that you need to setup in the credentials.yml file of the rasa chatbot. After you will add the credentials you will have to rerun the rasa application to take the changes to effect.

6. Here you have to setup the endpoint, and the endpoint should be the SSL certified, and it will be of this format,

   ``https://<domain-name>/webhooks/botframework/webhook ``

   - We will use **ngrok** as a local server [ngrok Docs](https://ngrok.com/docs).

     - to expose a web server on port 5005 of your local machine to the internet 

       `` ngrok http 5005 `` 

       **_Note_**: 5005 is the same port number that ' Rasa ' server uses. 
      
       it will start like the folowing image:

![ngrok](https://github.com/ayaallaa/Delivery-Chatbot/blob/main/Rasa_Chatbot/images/ngrok.jpeg?raw=true)
       
       we will take the https url and put it in the endpoint adress like the following: 
       
       `` https://9412c649e0fe.ngrok.io/webhooks/botframework/webhook ``

7. Once you have added the endpoint, just verify it. If it is verified successfully that means you chatbot alive and have established the successful connection and we are good to go.

8. Now go to Test and distribute. Here on the right side you will get the description. If it is empty that means everything is proper and now you can download the app and install it.

9. Now Click on download to download the app.

10. Once you have downloaded the app, now go to apps again and you will notice and option “Upload a custom app“, click on it and select “Upload for my org“. Now select the file that you just downloaded to install it.

11. It will install the app and take you inside the app. So here you are, you have successfully setup the application successfully.

12. Here you can now talk to the bot that you just setup.

In the above steps we have successfully setup everything that is needed to integrate the rasa chatbot to MS teams. 


## Add the credentials to the Rasa chatbot:

Now add the credentials of botframework to the rasa chatbot. To do that go to Rasa project and open credentials.yml and add the microsoft credentails in the given way.

``` 
botframework:
     app_id: "<app-id-you-get-for-bot>"
     app_password: "<app-password-you-get-for-bot>" 
```

## Start the chatbot:

Now everything should be done it's time to stert our chatbot by starting 

* Rasa server :

    `` rasa run --model models --enable-api --cors "*" ``

* Actions server in another terminal: 
    
    `` rasa run actions ``

**_Note_**: **ngrok** should be runing too.


## To use the DeliveryBot App:

* Open MS_Teams

* Apps --> app studio --> import an existing app.

**_Note_**: use personal account if this is not working while using Nokia account if it's not allowed

* Import the DeliveryBot zip --> go to ``Bots``

* Edit the endpoint address like in step 6 as mentioned above & make sure it's running & correct. 

* Complete the same steps from 7 till the end.

* Train Rasa chatbot 

* Run the Rasa server& the actions server as mentioned above.

* Start to say Hi to the bot.
