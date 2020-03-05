# -*- coding: utf-8 -*-

"""
This module contains the authentication module.
User should obtain permissions by applying for a bot in the `special pages`-> `bot password` page of the wikibase homepage. After approval or self-approval, put the username and password in the .crendentials.json file.
"""

import requests
import json


class Authenticator():
    def __init__(self):
        """A very simple class
        """
        pass

    def authenticate(self, endpointUrl: str = "http://localhost:8181", resourceUrl: str = "/w/api.php", credentialPath: str = "./.crendentials.json") -> str:
        """authenticate() performs the authentication sequence using the credentials in the .credentials.json file. This function returns the CSRF token which should be placed in the `token` field for editing interactions with wikibase endpoints. 

        :param endpointUrl: defaults to "http://localhost:8181"
        :type endpointUrl: str, optional
        :param resourceUrl: defaults to "/w/api.php"
        :type resourceUrl: str, optional
        :param credentialPath: defaults to "./.crendentials.json"
        :type credentialPath: str, optional
        :return: csrfToken: This token required for editing operations
        :rtype: str
        """
        with open(credentialPath, 'rt') as crendentials:
            data = json.load(crendentials)
        username = data["username"]
        password = data["password"]
        apiUrl = endpointUrl + resourceUrl

        # get login token
        parameters = {
            'action': 'query',
            'meta': 'tokens',
            'type': 'login',
            'format': 'json'
        }
        data = requests.get(url=apiUrl, params=parameters).json()
        loginToken = data['query']['tokens']['logintoken']

        # perform a secure login for the session
        parameters = {
            'action': 'login',
            'lgname': username,
            'lgpassword': password,
            'lgtoken': loginToken,
            'format': 'json'
        }
        r = requests.post(apiUrl, data=parameters)

        # get a CSRF (edit) token
        parameters = {
            "action": "query",
            "meta": "tokens",
            "format": "json"
        }
        data = requests.get(url=apiUrl, params=parameters).json()
        csrfToken = data["query"]["tokens"]["csrftoken"]
        return csrfToken
