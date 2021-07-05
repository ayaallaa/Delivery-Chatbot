# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 14:49:17 2021

@author: hager abdelazim
"""

import requests
import logging
import sys
import json
import datetime

from urllib.parse import urlencode, quote, parse_qs

import time

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

logger.addHandler(ch)


# The HTTP timeout for querying the MS Graph API
GRAPH_QUERY_TIMEOUT = 60

# Base URL of the MS Graph API
API_BASE_URL = "https://graph.microsoft.com/v1.0"


# Sends an HTTP request to the MS Graph API end point located at url.
# Requires a value MS Graph auth token.
#
#   url: Service endpoint relative to API_BASE_URL
#   token: A valid MS Graph API auth token
#   get_params: Options GET parameters included in the URL
#   additional_headers: Additional headers included in the request
#
# Returns complete response or throws exception if an error occurred
#
def make_msgraph_request(endpoint, auth_token, get_params={}, additional_headers={}, api_url=API_BASE_URL):

    try:
        headers = {
            'Authorization': auth_token,
            'Accept': 'application/json'
        }

        headers.update(additional_headers)

        query = "{0}/{1}?{2}".format(api_url, endpoint, urlencode(get_params))

        response = requests.get(query, headers=headers, timeout=GRAPH_QUERY_TIMEOUT)

        if response:
            response_json = response.json()

            return response_json
        else:
            error_msg = "make_msgraph_request - MS Graph API HTTP error {0}: {1}".format(
                response.status_code, json.dumps(json.loads(response.text)))

            logger.error(error_msg)
            raise Exception(error_msg)

    except requests.exceptions.ReadTimeout:
        error_msg = "make_msgraph_request - MS Graph query timed out: {0}".format(endpoint)

        logger.error(error_msg)
        raise Exception(error_msg)

    except requests.exceptions.ConnectTimeout:
        error_msg = "make_msgraph_request - MS Graph query connection timed out: {0}".format(endpoint)

        logger.error(error_msg)
        raise Exception(error_msg)

    except Exception as e:
        error_msg = "make_msgraph_request - MS Graph query ({0}) encountered an exception: {1}".format(endpoint, str(e))

        logger.error(error_msg)
        raise Exception(error_msg)


# Attributes that are included in a message query result (if available)
MESSAGE_QUERY_ATTRIBUTES = "sentDateTime," \
                           "subject," \
                           "uniqueBody," \
                           "from," \
                           "toRecipients," \
                           "ccRecipients," \
                           "webLink," \
                           "conversationId," \
                           "id"


# Maximum number of messages returned from a message query
MAX_MESSAGE_RESULTS = 500

# Attributes that are included in a calendar query result (if available)
CALENDAR_QUERY_ATTRIBUTES = "organizer," \
                            "subject," \
                            "lastModifiedDateTime," \
                            "body," \
                            "start," \
                            "attendees," \
                            "webLink," \
                            "seriesMasterId," \
                            "id"

# Maximum number of calendar events returns from a calendar query
MAX_CALENDAR_RESULTS = 500

# Range of dates to search for a calendar event in
CALENDAR_DAY_RANGE = 31

# Attributes that are included in a OneDrive query result (if available)
ONEDRIVE_QUERY_ATTRIBUTES = "name," \
                            "description," \
                            "size," \
                            "lastModifiedDateTime," \
                            "webUrl," \
                            "createdBy," \
                            "lastModifiedBy," \
                            "id"

# Maximum number of results returned in a OneDrive query
MAX_ONEDRIVE_RESULTS = 500


CONTACTS_QUERY_ATTRIBUTES = "categories," \
                            "companyName," \
                            "department," \
                            "displayName," \
                            "emailAddresses," \
                            "jobTitle," \
                            "manager," \
                            "profession," \
                            "title," \
                            "id"

MAX_CONTACT_RESULTS = 500


PEOPLE_QUERY_ATTRIBUTES = "id"

MAX_PEOPLE_RESULTS = 500


ONENOTE_PAGE_ATTRIBUTES = "id," \
                          "self," \
                          "title," \
                          "lastModifiedDateTime"


ONENOTE_SECTION_ATTRIBUTES = "id," \
                             "self," \
                             "displayName," \
                             "lastModifiedDateTime," \
                             "createdBy," \
                             "lastModifiedBy"

MAX_ONENOTE_SECTION_RESULTS = 200

ONENOTE_NOTEBOOK_ATTRIBUTES = "id," \
                              "self," \
                              "lastModifiedDateTime," \
                              "createdBy," \
                              "lastModifiedBy," \
                              "displayName"

MAX_ONENOTE_NOTEBOOK_RESULTS = 200

USER_DATA_PROJECTION = "id,skills,interests,aboutMe,pastProjects,schools,responsibilities"


# Determines if the subject line or body text of a calendar event
# includes the given query term (full query term matching, its assumed
# query is lowercase)
def accept_calendar_event_query_result(result, query):

    if 'subject' in result:
        subject = result['subject'].lower()

        if query in subject:
            return True

    if 'uniqueBody' in result:
        unique_body = result['uniqueBody']

        if 'content' in unique_body:
            body_content = unique_body['content']

            if query in body_content:
                return True

    return False


# Determines if the title of the given OneNote page
# contains the given query term (assumed to be lower
# case)
def accept_onenote_page_result(result, query):

    if 'title' in result:
        title = result['title'].lower()

        if query in title:
            return True

    return False


# Class with methods for accessing data out of the MS Graph API.
# The complete response from the MS Graph API is returned.
class MSGraphDataAccessor:

    def __init__(self):
        pass

    # Searches for messages that include the given query term.
    # This includes sent, received, and draft messages.
    def message_query(self, auth_token, query_term):

        url = "me/messages"

        query_args = {
            "$search": '"{0}"'.format(query_term),
            "$select": MESSAGE_QUERY_ATTRIBUTES,
            "$top": MAX_MESSAGE_RESULTS
        }

        response = make_msgraph_request(
            auth_token=auth_token,
            endpoint=url,
            get_params=query_args
        )

        return response

    # Returns inbox messages received in the last 24 hours
    def get_todays_received_messages(self, auth_token):

        url = "me/mailFolders/inbox/messages"

        now = datetime.datetime.utcnow()
        date_from = now - datetime.timedelta(days=1)

        query_args = {
            "$filter": "receivedDateTime gt {0}".format(datetime.datetime.strftime(date_from, "%Y-%m-%dT%H:%M:%SZ")),
            "$select": MESSAGE_QUERY_ATTRIBUTES,
            "$top": MAX_MESSAGE_RESULTS
        }

        response = make_msgraph_request(
            auth_token=auth_token,
            endpoint=url,
            get_params=query_args
        )

        return response

    #
    # Returns MAX_MESSAGE_RESULTS most recent emails
    # from the user's inbox
    #
    def get_inbox(self, auth_token):

        url = "me/mailFolders/inbox/messages"

        query_args = {
            "$select": MESSAGE_QUERY_ATTRIBUTES,
            "$top": MAX_MESSAGE_RESULTS
        }

        response = make_msgraph_request(
            auth_token=auth_token,
            endpoint=url,
            get_params=query_args
        )

        return response

    # Searches for calendar events that include the provided query term.
    # Since MS Graph API does not yet support querying for calendar
    # events, all events in a two month range are returned and
    # a filter is applied to make sure results include the specified
    # query term.
    def calendar_query(self, auth_token, query_term):

        query_term = query_term.lower()

        url = "me/calendarView"

        date_today = datetime.datetime.utcnow()

        date_from = date_today - datetime.timedelta(days=CALENDAR_DAY_RANGE)
        date_to = date_today + datetime.timedelta(days=CALENDAR_DAY_RANGE)

        query_args = {
            "startdatetime": datetime.datetime.strftime(date_from, "%Y-%m-%dT%H:%M:%SZ"),
            "enddatetime": datetime.datetime.strftime(date_to, "%Y-%m-%dT%H:%M:%SZ"),
            "$select": CALENDAR_QUERY_ATTRIBUTES,
            "$top": MAX_CALENDAR_RESULTS
        }

        response = make_msgraph_request(
            auth_token=auth_token,
            endpoint=url,
            get_params=query_args
        )

        filtered_results = []

        for result in response['value']:
            if accept_calendar_event_query_result(result, query_term):
                filtered_results.append(result)

        response['value'] = filtered_results

        return response

    # Returns all calendar events that occurred in the last 6 hours or occur in the
    # next 18 hours
    def get_todays_calendar_events(self, auth_token):

        url = "me/calendarView"

        date_today = datetime.datetime.utcnow()
        date_from = date_today - datetime.timedelta(hours=6)
        date_to = date_today + datetime.timedelta(hours=18)

        query_args = {
            "startdatetime": datetime.date.strftime(date_from, "%Y-%m-%dT%H:%M:%SZ"),
            "enddatetime": datetime.date.strftime(date_to, "%Y-%m-%dT%H:%M:%SZ"),
            "$select": CALENDAR_QUERY_ATTRIBUTES,
            "$top": MAX_CALENDAR_RESULTS
        }

        response = make_msgraph_request(
            auth_token=auth_token,
            endpoint=url,
            get_params=query_args
        )

        return response

    # Queries a user's one drive folders for the given query_term
    def query_one_drive(self, auth_token, query_term):

        url = "me/drive/search(q='{0}')".format(quote(query_term))

        query_args = {
            "$select": ONEDRIVE_QUERY_ATTRIBUTES,
            "$top": MAX_ONEDRIVE_RESULTS
        }

        response = make_msgraph_request(
            auth_token=auth_token,
            endpoint=url,
            get_params=query_args
        )

        return response

    # Queries a user's contacts (the people they explicitly added to their
    # contacts list)
    def contacts_query(self, auth_token, query_term):

        url = "me/contacts"

        query_args = {
            "$search": '"{0}"'.format(query_term),
            "$select": CONTACTS_QUERY_ATTRIBUTES,
            "$top": MAX_CONTACT_RESULTS
        }

        response = make_msgraph_request(
            auth_token=auth_token,
            endpoint=url,
            get_params=query_args
        )

        return response

    # Queries the people closely related to the person identified by the given
    # auth token
    def people_query(self, auth_token, query_term):

        url = "me/people"

        query_args = {
            "$search": '"{0}"'.format(query_term),
            "$select": PEOPLE_QUERY_ATTRIBUTES,
            "$top": MAX_PEOPLE_RESULTS
        }

        response = make_msgraph_request(
            auth_token=auth_token,
            endpoint=url,
            get_params=query_args
        )

        return response

    # Returns max_results people who are closely related to the
    # given MS Graph API user, according to the MS Graph API
    def get_related_people(self, auth_token, max_results=50):

        url = "me/people"

        query_args = {
            "$select": PEOPLE_QUERY_ATTRIBUTES,
            "$top": max_results
        }

        response = make_msgraph_request(
            auth_token=auth_token,
            endpoint=url,
            get_params=query_args
        )

        return response

    # Queries for a user's onenote pages (max 100, due to API limits).
    # Only pages with titles that contain the given query term
    # are returned.
    def onenote_page_query(self, auth_token, query_term):

        query_term = query_term.lower()

        url = "me/onenote/pages"

        query_args = {
            "$select": ONENOTE_PAGE_ATTRIBUTES,
            "$expand": "parentSection",
            "$top": 100  # API Limit as of 2017
        }

        response = make_msgraph_request(
            auth_token=auth_token,
            endpoint=url,
            get_params=query_args
        )

        filtered_results = []

        for result in response['value']:
            if accept_onenote_page_result(result, query_term):
                filtered_results.append(result)

        response['value'] = filtered_results

        return response

    # Queries for a user's onenote sections. Filtering based on a query_term is
    # applied later by a data set builder, as a given section is included if
    # one of its pages is included in the result set.
    def onenote_sections_query(self, auth_token, query_term):

        url = "me/onenote/sections"

        query_args = {
            "$select": ONENOTE_SECTION_ATTRIBUTES,
            "$expand": "parentNotebook",
            "$top": MAX_ONENOTE_SECTION_RESULTS
        }

        response = make_msgraph_request(
            auth_token=auth_token,
            endpoint=url,
            get_params=query_args
        )

        return response

    # Queries for a user's onenote sections. Filtering based on a query_term is
    # applied later by a data set builder, as given notebook is included if one of
    # its sections is in the result set.
    def onenote_notebook_query(self, auth_token, query_term):

        url = "me/onenote/notebooks"

        query_args = {
            "$select": ONENOTE_NOTEBOOK_ATTRIBUTES,
            "$top": MAX_ONENOTE_NOTEBOOK_RESULTS
        }

        response = make_msgraph_request(
            auth_token=auth_token,
            endpoint=url,
            get_params=query_args
        )

        return response

    def get_drive_item_details(self, auth_token, drive_id, item_id):

        url = "/drives/{0}/items/{1}/".format(drive_id, item_id)

        response = make_msgraph_request(
            auth_token=auth_token,
            endpoint=url
        )

        return response

    def get_user_data(self, user_id: str, auth_token: str):
        url = "users/{0}".format(user_id)

        args = {
            "$select": USER_DATA_PROJECTION
        }

        response = make_msgraph_request(
            endpoint=url,
            auth_token=auth_token,
            get_params=args
        )

        return response

    def get_all_nokia_users(self, auth_token: str):

        done = False
        max_query_results = 100

        get_params = {
            "$top": max_query_results,
            "$expand": "manager"
        }

        retries = 0

        all_results = []

        while done is False:
            end_point = "users"

            response = make_msgraph_request(
                endpoint=end_point,
                auth_token=auth_token,
                get_params=get_params,
                api_url="https://graph.microsoft.com/beta/"
            )

            if 'error' in response:
                if response['code'] == 'InternalServerError':
                    if retries < 3:
                        time.sleep(2)
                        retries += 1
                        continue
                    else:
                        raise Exception("Failed to load users")

            retries = 0

            parsed_results = []

            for value in response['value']:
                result = self.parse_detailed_result(value)

                if result is not None:
                    parsed_results.append(result)

            if '@odata.nextLink' in response:
                link = response['@odata.nextLink']

                query_string = parse_qs(link)

                skip_token = query_string['$skiptoken'][0]

                get_params = {
                    "$top": max_query_results,
                    "$skiptoken": skip_token,
                    "$expand": "manager"
                }

            else:
                done = True

            all_results += parsed_results

            print("get_all_nokia_users() - # results: {0}".format(len(all_results)))

        return all_results

    def parse_detailed_result(self, result):

        if 'id' not in result:
            return None

        if 'displayName' not in result:
            return None

        if 'userPrincipalName' not in result:
            return None

        user_id = result['id']

        display_name = result['displayName']
        main_email = result['userPrincipalName']

        unique_email_addresses = set()
        unique_email_addresses.add(main_email)

        if 'proxyAddresses' in result:
            unique_email_addresses = unique_email_addresses.union(
                self.parse_proxy_addresses(result['proxyAddresses'])
            )

        email_address_list = list(unique_email_addresses)

        department = result.get('department', None)
        company = result.get('companyName', None)
        job_title = result.get('jobTitle', None)
        manager = result.get('manager', None)

        manager_id = None

        if manager is not None and 'id' in manager:
            manager_id = manager['id']

        city = result.get("city", None)
        country = result.get("country", None)

        user_doc = {
            '_id': user_id,
            'displayName': display_name,
            'primaryEmail': main_email,
            'emailAddresses': email_address_list,
            'department': department,
            'company': company,
            'jobTitle': job_title,
            'managerId': manager_id,
            'city': city,
            'country': country
        }

        return user_doc

    def parse_proxy_addresses(self, proxy_addresses: list):

        email_addresses = set()

        for proxy_address in proxy_addresses:
            lower_proxy_address = proxy_address.lower()

            if lower_proxy_address.startswith("smtp"):
                lower_email_address = lower_proxy_address[5:]

                email_addresses.add(lower_email_address)

        return email_addresses

