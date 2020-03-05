'''
Test the scripts in ./scripts/ directory.

'''

import requests
import pytest


class TestTestScripts:

    def test_wikidata(self):
        """Ping the official wikidata instance.
        """
    url = "https://www.wikidata.org/wiki/Special:EntityData/P31.json"
    res = requests.get(url)
    assert(res.status_code == 200)
