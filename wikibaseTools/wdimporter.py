import requests
import simplejson as json
from wikibaseTools.core import EntityEditor
from wikibaseTools.auth import Authenticator
from glob import glob
import os


class WDImporter():
    """[summary]
    """

    def __init__(self, apiUrl, csrfToken):
        self.editor = EntityEditor(apiUrl, csrfToken)
        print("WARNING: Before calling `importWikiDataProperty()`, please make sure you have a CLEAN wikibase instance.")
        self.apiUrl = apiUrl
        self.csrfToken = csrfToken

    @staticmethod
    def extractID(jsonPath):
        return int(os.path.basename(jsonPath).split(".")[0][1:])

    def importWikiDataProperty(self, jsonDir: str = "data/wikidataProperties") -> bool:
        """import the wikidata properties stored as json files in a local folder.

        :param jsonDir: directory of json files, defaults to "data/wikidataProperties"
        :type jsonDir: str, optional
        :return whether importing is successful or not
        :rtype: bool
        """
        editor = EntityEditor(apiUrl=self.apiUrl, csrfToken=self.csrftoken)
        jsons = glob(os.path.abspath(jsonDir) + "/*.json")
        jsonIDs = set([WDImporter.extractID(js) for js in jsons])
        maxID = max(jsonIDs)

        # create properties if not existed there. Use default, set datatype to be string.

        for i in range(1, maxID+1):
            if i in jsonIDs:
                with open(os.path.abspath(jsonDir)+"/P"+str(i) + ".json") as f:
                    prop = json.load(f)
                if not editor.checkExistence("P"+str(i)):
                    # need to create new entities until P{i-1} is created
                    # then create entity P{i} according to the ideal datatype
                    if not editor.checkExistence("P"+str(i-1)):
                        while "P"+str(i-1) != editor.createEntity(entityType="property", dataType="string"):
                            continue
                    # create property P{i}

                    idealDataType = prop["entities"]["P"+str(i)]["datatype"]
                    if idealDataType in ["math","wikibase-lexeme","wikibase-form","wikibase-sense"]:
                        print("Error create entity with id {}, will create a plain one with string dataType.".format(i))
                        idealID = editor.createEntity(
                            entityType="property", dataType="string")
                        assert("P"+str(i) == idealID)
                    else:
                        idealID = editor.createEntity(
                            entityType="property", dataType=idealDataType)
                        assert("P"+str(i) == idealID)
                else:
                    # the property Pi exists but the dataType has to match
                    # if dataType not agree, through warning
                    idealDataType = prop["entities"]["P"+str(i)]["datatype"]
                    existedDataType = editor.getDataType("P"+str(i))
                    if idealDataType != existedDataType:
                        print("Datatype of existed property P{} {} doesn't match wikidata property {}".format(
                            i, existedDataType, idealDataType))
                editor.clearEntity("P"+str(i))

                # create basics: labels, descriptions, aliases
                # api.php?action=wbeditentity&id=Q42&data={"labels":[{"language":"no","value":"Bar","add":""}]}
                try:
                    dataDict = {
                        "labels": [{"language": "en", "value": prop["entities"]["P"+str(i)]["labels"]["en"]["value"]}],
                        "descriptions": {"en": {"language": "en", "value": prop["entities"]["P"+str(i)]["descriptions"]["en"]["value"]}}
                    }
                except:
                    print("Error building labels/descriptions for id {}".format(i))
                try:
                    res = editor.writeStatement(
                        entityID="P"+str(i), dataDict=dataDict, checkExistence=False)
                except:
                    print("Error writing labels/descriptions for id {}: ".format(i), res)

    def importWikiDataPropertyClaims(self, propertyID: str, jsonDir: str = "data/wikidataProperties") -> bool:
        """import Properties of WikiDataProperties. If the string is 
        :param propertyID: , defaults to None
        :type propertyID: str, optional
        :return: whether importing is successful or not
        :rtype: bool
        """
        pass
