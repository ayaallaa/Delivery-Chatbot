# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 21:38:22 2021

@author: haabdela
"""

import requests
import msal
import atexit
import os.path


TENANT_ID = 'f05a8c02-3d7d-48e8-becf-46e3f63aead9'
CLIENT_ID = 'ec91ff6b-dffd-4a7b-a8ed-f200b27d4340'


AUTHORITY = 'https://login.microsoftonline.com/' + TENANT_ID
ENDPOINT = 'https://graph.microsoft.com/v1.0'

SCOPES = [
    'Files.ReadWrite.All',
    'Sites.ReadWrite.All',
    'User.Read',
    'User.ReadBasic.All',
    'Calendars.Read'
]

cache = msal.SerializableTokenCache()

if os.path.exists('token_cache.bin'):
    cache.deserialize(open('token_cache.bin', 'r').read())

atexit.register(lambda: open('token_cache.bin', 'w').write(cache.serialize()) if cache.has_state_changed else None)

app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)

accounts = app.get_accounts()
result = None
if len(accounts) > 0:
    result = app.acquire_token_silent(SCOPES, account=accounts[0])

if result is None:
    flow = app.initiate_device_flow(scopes=SCOPES)
    if 'user_code' not in flow:
        raise Exception('Failed to create device flow')

    print(flow['message'])

    result = app.acquire_token_by_device_flow(flow)
auth_token = 'EwCIA8l6BAAU6k7+XVQzkGyMv7VHB/h4cHbJYRAAAU8YC1iCZNu3r8OFBb9wA+FWfAafzGabBBxsK9sL6o9ns9XTwLu8u2cCoO67nDqub0NQUSOzVhcgrrGWpRLt5Dlas50Be4w/RGKf2CvmNt1PpnwM8Ts4ifbDRmzAGPsbSAuuagjFB7LR/6hSyhssGqPTUhu8/fXgJLHk1FJuBe8dSmVuEo4CiC3CKANyeaZcj4AaD56ByWwLdugqd+AlyTIgo+3tbEjEwZ6+lKlUQwgYY1tcmL6I8sBnLuxFPjfTIwGjMSsN9ySEmO17axrbut2CQvezWpWveOYk2R4aoStZiIFUYu6bA2Y6B/MZxMfvfWOLfS80KTKEfLG1iiwfoGsDZgAACFtoCmiOoMazWALcR+rXt39AK0bTXDKcCCE+m3RWc2p0wHNi2KtnQwYnYqh8NNDqku+eh1re6p2+HW+kcro4Bc9RsU/4DYEZzsZ/ebRY0FiQx7BAlbeBE0rwk6L0kkLnzVeCC1Ss+H4wRU2u6GkkJgqQlzmFcrnKyMQToNQ1pqyGSyT7GqECTFs58UpLiF4bJfKtN++Koc4JydSPNr5pDvmxd1jhirg9+IJjMbrEX0GK4+rmrGy28TdgMxE+R3Q/PEyWm+b1BS2TvTKjdp5C3VbenywRXySovdLGwfrczq4+69QxzV5kiKo+jCQFKs4Ns4XXScgXYqDa7EieIY7P11wBYwoynuHYqi35HO9h0uRiFXnXWsv4tjjll1J9lX7n4GboGkH5ipVaatIdxvhFbZgg+geP7FMJMGCnp26OfSrlu/I5kYfoqWHS69sz+QcLQNfS8h3BLHTrB+6WpSCa0X6+P8+k1HdPQvlu3MKA8NE9979Sj1fP7JK6F+RedCiGza3c66pOpFrZFUO7vpthSQYhhp5LTGhJsGkXQunTjyUYrOsxUU0Coxo+rehxn+z9XJJlKMslKxAovP2zpkit6VqPnRRmvpea4SMHcX+D6EWSrRuE23lqdig16yt/ba6TKsUTa8MYctMKhAfQ8Rr8MFiFTPZByufR3S8UfhGBILtCvxitocOEYoDBzyKXnhTeK3pSJ6MrMKsQn4wpNdr6x/lIwvfeO3IbYb6a6luray9UotzMIS9CH9AnTkhy3CFVLMFyd+vtPXwgF85wz/2+Hg76ah6kC2ma9rmUr/Nrla3kPvqaAg=='
if 'access_token' in result:
    result = requests.get(f'{ENDPOINT}/me/calendars', headers={'Authorization': 'Bearer ' + auth_token})
    result.raise_for_status()
    print(result.json())

else:
    raise Exception('no access token in result')