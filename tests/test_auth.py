'''
Test the authentication module in ./scripts/ directory.

'''

import requests
from wikibaseTools.auth import Authenticator


class TestTestAuth:
    """Test authentication module.
    """

    def test_auth(self):
        """Test the Authenticator() can successfully obtain a non-null csrf token. The .crendentials2.json file must exist to perform the test.
        """
        testAuth = Authenticator()
        csrfToken, _ = testAuth.authenticate(
            "https://test.wikidata.org", "/w/api.php", ".credentials2.json")
        assert (len(csrfToken) > 0)
