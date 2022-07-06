# rasa_chatbot_master
Welcome to the Backend of our food consulting chatbot which is called Liefy.

Install rasa on your local machine:
rasa install

To get start please train your own model on your local machine with: 
rasa train

After u can activate the RASA SDK Action Server for using customized python code from our action.py and dataImport.py file:
rasa run actions ("--debug" in case u want to see more details)

Also enable Rasa Core Server to communicate with our FE:
rasa run --cors "*" --enable-api



