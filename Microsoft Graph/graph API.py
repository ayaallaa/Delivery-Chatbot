# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 01:36:02 2021

@author: haabdela
"""

from pprint import pprint
from ms_graph.client import MicrosoftGraphClient
from configparser import ConfigParser

# Specify your scopes when you want access certain resources.
scopes = [
    'Calendars.ReadWrite',
    'Files.ReadWrite.All',
    'User.ReadWrite.All',
    'Notes.ReadWrite.All',
    'Directory.ReadWrite.All',
    'User.Read.All',
    'Directory.Read.All',
    'Directory.ReadWrite.All',
    'offline_access',
    'openid',
    'profile'
]

# Initialize the Parser.
config = ConfigParser()

# Read the file.
config.read('config/config.ini')

# Get the specified credentials.
client_id = config.get('graph_api', '6da88b9d-58db-42fb-9528-96f04bf83302')
client_secret = config.get('graph_api', 'c50c43bf-27f7-43d9-a432-64a2cc116ecc')
redirect_uri = config.get('graph_api', 'https://localhost/MicrosoftGraph')

# Initialize the Client.
graph_client = MicrosoftGraphClient(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scopes,
    credentials='config/ms_graph_state.jsonc'
)

# Login to the Client.
graph_client.login()


# Grab the User Services.
user_services = graph_client.users()

# List the Users.
pprint(user_services.list_users())


# Grab the Drive Services.
drive_services = graph_client.drives()

# List the Root Drive.
pprint(drive_services.get_root_drive())