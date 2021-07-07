import requests



ENDPOINT = 'https://graph.microsoft.com/v1.0'

def Find_First_Suggestions_time (auth_token):
    result = requests.post(f'{ENDPOINT}/me/findMeetingTimes', headers={'Authorization': 'Bearer ' + auth_token})
    item_info = result.json()
    if 'meetingTimeSuggestions' in item_info:
        response= item_info['meetingTimeSuggestions'][1]['meetingTimeSlot']['start']

    else:
          raise Exception('no access token in meetingTimeSuggestions')
    
    return response



def ALL_Suggestions_time (auth_token):
    result = requests.post(f'{ENDPOINT}/me/findMeetingTimes', headers={'Authorization': 'Bearer ' + auth_token})
    item_info = result.json()
    response2=[]
    if 'meetingTimeSuggestions' in item_info:
        for i in range (0,5):
            response2.append(item_info['meetingTimeSuggestions'][i]['meetingTimeSlot']['start'])

    else:
          raise Exception('no access token in meetingTimeSuggestions')
    
    return response2





### findMeetingTime

access_token='eyJ0eXAiOiJKV1QiLCJub25jZSI6InRBblBReS1RX2JGMWhOcUwzZV9WbFc1T0diSkFFcUMweU5EWGZVQXdMVTAiLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyIsImtpZCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC81ZDQ3MTc1MS05Njc1LTQyOGQtOTE3Yi03MGY0NGY5NjMwYjAvIiwiaWF0IjoxNjI1MzA5ODAxLCJuYmYiOjE2MjUzMDk4MDEsImV4cCI6MTYyNTMxMzcwMSwiYWNjdCI6MCwiYWNyIjoiMSIsImFjcnMiOlsidXJuOnVzZXI6cmVnaXN0ZXJzZWN1cml0eWluZm8iLCJ1cm46bWljcm9zb2Z0OnJlcTEiLCJ1cm46bWljcm9zb2Z0OnJlcTIiLCJ1cm46bWljcm9zb2Z0OnJlcTMiLCJjMSIsImMyIiwiYzMiLCJjNCIsImM1IiwiYzYiLCJjNyIsImM4IiwiYzkiLCJjMTAiLCJjMTEiLCJjMTIiLCJjMTMiLCJjMTQiLCJjMTUiLCJjMTYiLCJjMTciLCJjMTgiLCJjMTkiLCJjMjAiLCJjMjEiLCJjMjIiLCJjMjMiLCJjMjQiLCJjMjUiXSwiYWlvIjoiQVNRQTIvOFRBQUFBa01Wek9xM0RxdjZpRUhhUFFlMllsRWxORnZyYWNWYjMzbGdPeXdWUWFlbz0iLCJhbXIiOlsicHdkIiwicnNhIl0sImFwcF9kaXNwbGF5bmFtZSI6IkdyYXBoIGV4cGxvcmVyIChvZmZpY2lhbCBzaXRlKSIsImFwcGlkIjoiZGU4YmM4YjUtZDlmOS00OGIxLWE4YWQtYjc0OGRhNzI1MDY0IiwiYXBwaWRhY3IiOiIwIiwiZGV2aWNlaWQiOiJlZWI5MzdhMC00ZDM5LTRiNWYtYTVmNC1jODkxYzQwYmIyMzkiLCJmYW1pbHlfbmFtZSI6IkFsYWFlbGRpbiIsImdpdmVuX25hbWUiOiJBeWEiLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIxOTcuNDkuMTc4LjIxMiIsIm5hbWUiOiJBbGFhZWxkaW4sIEF5YSAoRVhUIC0gRUcpIiwib2lkIjoiMjFlYmYzMmYtYzkyYy00ZmM3LThiNTAtMmUxNmEzMTAwMTQwIiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTE1OTMyNTEyNzEtMjY0MDMwNDEyNy0xODI1NjQxMjE1LTM0NzA1MTYiLCJwbGF0ZiI6IjMiLCJwdWlkIjoiMTAwMzIwMDEzQjJGOTJGRCIsInJoIjoiMC5BUkFBVVJkSFhYV1dqVUtSZTNEMFQ1WXdzTFhJaTk3NTJiRklxSzIzU05weVVHUVFBRUUuIiwic2NwIjoiQ2FsZW5kYXJzLlJlYWRXcml0ZSBvcGVuaWQgcHJvZmlsZSBVc2VyLlJlYWQgZW1haWwiLCJzaWduaW5fc3RhdGUiOlsiZHZjX21uZ2QiLCJkdmNfZG1qZCIsImttc2kiXSwic3ViIjoiWkhfRFpBWmNROFlYNnBvY1FHd1VDY2Y4TDM0UjZyeXFVVUNtVjZlWUtyTSIsInRlbmFudF9yZWdpb25fc2NvcGUiOiJFVSIsInRpZCI6IjVkNDcxNzUxLTk2NzUtNDI4ZC05MTdiLTcwZjQ0Zjk2MzBiMCIsInVuaXF1ZV9uYW1lIjoiYXlhLmFsYWFlbGRpbi5leHRAbm9raWEuY29tIiwidXBuIjoiYXlhLmFsYWFlbGRpbi5leHRAbm9raWEuY29tIiwidXRpIjoiMmlTb3RNaDE3RVdrSHNZUi1jTm9BQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc19zdCI6eyJzdWIiOiJkNGx4ZTNGYjdqS0xDU1Q0dzVIYW5pSjlFQnduYy1JUWlqdGVnTkRTNFFjIn0sInhtc190Y2R0IjoxNDI0ODExNTU1fQ.cGlnLzsSQfT3uEqe_7saeBqPjkRctwaOkyBTHRytX0_SSwqeJWZKjlOu7NUgCp3GHkzMso5f613OMhYMuQ9r4M2WFX3mGTpUD-Y0d84MDAwSkqwDrmrvMVNnysPFMFq2IFbbszgQjg2wzM8-dPHtLLTapeFH7Lykxpi9KXMHcbqHsznlvmaBgCrkj2VRWiHHGG1gGsOeqRUZvSqPAHUI8w4T3bwtJDXPfd-IijjMmsD7_Lo13gZWSsLJMo-2vGnWMSzkg6TL9xFIHqjGA0nOu5LkptqUz49XPN_qgK8VFumbRm9LCmPHL3vl0ue-qTDu9Bcs-ClG9Q2dpXrr4hVWQA'


first_time=Find_First_Suggestions_time(access_token)
print(first_time)



ALL_Suggustion=ALL_Suggestions_time(access_token)
print(ALL_Suggustion)



