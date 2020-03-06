from wikibaseTools.auth import Authenticator
from wikibaseTools.core import EntityEditor
from random import randint
import pytest


class TestTestCore:
    def test_creation(self):
        """test creation of entities on wikidata test instance. This function will create a new entity on wikidata every time you test it.
        """

        authenticator = Authenticator()
        csrftoken, apiurl = authenticator.authenticate(
            "https://test.wikidata.org",
            "/w/api.php",
            ".credentials2.json")
        editor = EntityEditor(apiUrl=apiurl, csrfToken=csrftoken)

        newID = editor.createEntity(entityType="item")
        assert(len(newID) > 1 and newID.startswith("Q"))

        newID = editor.createEntity(entityType="property", dataType="string")
        assert(len(newID) > 1 and newID.startswith("P"))

    def test_checkExistence(self):
        """use one valid and some invalid (supposed) ids and test them against https://test.wikidata.org.
        """
        authenticator = Authenticator()
        csrftoken, apiurl = authenticator.authenticate(
            "https://test.wikidata.org",
            "/w/api.php",
            ".credentials2.json")
        editor = EntityEditor(apiUrl=apiurl, csrfToken=csrftoken)
        existed = ["403"]
        for ID in existed:
            assert(editor.checkExistence(entityID="P"+str(ID)))
            assert(editor.checkExistence(entityID="Q"+str(ID)))
        nonexisted = [randint(100000000, 200000000) for i in range(1)]
        for ID in nonexisted:
            assert(not editor.checkExistence(entityID="P"+str(ID)))
            assert(not editor.checkExistence(entityID="Q"+str(ID)))

    @pytest.mark.skip(reason="Can only run with local settings.")
    def _test_deleteEntity(self):
        """test entity deletion. Please run it at local environment only
        """
        authenticator = Authenticator()
        csrftoken, apiurl = authenticator.authenticate(
            endpointUrl="http://localhost:8181",
            resourceUrl="/w/api.php",
            credentialPath=".credentials.json")
        editor = EntityEditor(apiUrl=apiurl, csrfToken=csrftoken)
        assert(editor.deleteEntity("Q10000", asAdmin=True))
