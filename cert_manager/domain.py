# -*- coding: utf-8 -*-
"""Define the cert_manager.domain class."""

import logging
from ._endpoint import Endpoint
from urllib.parse import urlencode # python3
from collections import OrderedDict

LOGGER = logging.getLogger(__name__)


class Domain(Endpoint):
    """Query the Sectigo Cert Manager REST API for Domains"""

    def __init__(self, client, api_version="v1"):
        """Initialize the class.

        :param object client: An instantiated cert_manager.Client object
        :param string api_version: The API version to use; the default is "v1"
        """
        super(Domain, self).__init__(client=client, endpoint="/domain", api_version=api_version)

    def list(self, page=0, results=200):
        """Return a list of domains from Sectigo.

        :param page pagination number
        :param results number of results per page (max 200)

        :return list: A list of dictionaries representing the domains
        """

        query_string = urlencode(OrderedDict(size=results,position=page))
        url = self._api_url + '?' + query_string

        result = self._client.get(url)

        return result.json()

    def create(self, domain, active=True):
        """Add a domain to the Sectigo account
        """
        url = self._api_url
        data = {
            "name": domain, "description": "created by REST API", "active": active,
            "delegations":[{"orgId":6125,"certTypes":["SSL"]}]
        }
        result = self._client.post(url, data=data)
