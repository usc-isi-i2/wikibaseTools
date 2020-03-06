
import requests
import simplejson as json


class EntityEditor:
    """`EntityEditor` is the central class. It interacts with a wikibase instance. 

    :return: [description]
    :rtype: [type]
    """

    def __init__(self, apiUrl, csrfToken):
        self.apiUrl = apiUrl
        self.csrfToken = csrfToken
        self.session = requests.Session()

    def createEntity(self, entityType: str = "item", dataType: str = '') -> str:
        """Create an entity with the appending-only design pattern of Wikibase. If there are total N items/properties in wikibase instance, this function will create (N+1)-th item or property and return the id, either Q{N+1} or P{N+1}. This function does NOTHING to the label, descriptions, etc., which is the responsiblity of `writeStatement()` method.

        :param: entityType: the type of entity, can be either `item` or `property`, defaults to `item`
        :type: entityType: str
        :param: dataType: type of property entity. Check https://www.wikidata.org/wiki/Help:Data_type.
        :type: dataType: str
        :return: id of entity just created
        :rtype: str
        """
        parameters = {
            'action': 'wbeditentity',
            'format': 'json',
            'new': entityType,
            'token': self.csrfToken,
        }
        if entityType == "property":
            if dataType == '':
                print("Data type for property entity must be provided.")
                raise
            parameters["data"] = json.dumps({"datatype": dataType})
        else:
            parameters["data"] = json.dumps({})
        r = self.session.post(self.apiUrl, data=parameters).json()
        print(r)
        if 'error' in r:
            return "error"
        else:
            return r["entity"]["id"]

    def checkExistence(self, entityID: str) -> bool:
        """Check the existence of a SINGLE entity.

        :param entityID: Qxxx or Pxxx
        :type entityID: str
        :return: If exists, return True
        :rtype: bool
        """
        parameters = {
            'action': 'wbgetentities',
            'format': 'json',
            'props': "info",
            "ids": entityID,
            'redirects': "yes"
        }
        res = self.session.get(self.apiUrl, params=parameters).json()
        if 'missing' in res["entities"][entityID]:
            return False
        return True

    def writeStatement(self, entityID: str, dataDict={}, checkExistence: bool = True) -> bool:
        """write a statement
        
        :param entityID: [description]
        :type entityID: str
        :param dataDict: [description], defaults to {}
        :type dataDict: dict, optional
        :param checkExistence: [description], defaults to True
        :type checkExistence: bool, optional
        :return: [description]
        :rtype: bool
        """        
        if checkExistence:
            if not self.checkExistence(entityID):
                print("No entity with ID {} exists.".format(entityID))
                return False

    def deleteEntity(self, entityID: str, asAdmin: bool = False) -> bool:
        """delete an entity from a wikibase where the user has administrator privilege

        :param entityID: Qxxx or Pxxx
        :type entityID: str
        :param asAdmin: whether the user has administrator privilege, defaults to False
        :type asAdmin: bool, optional
        :return: deletion successful or not
        :rtype: bool
        """
        if not asAdmin:
            print("Administrator previliage required.")
            return False
        parameters = {
            'action': 'delete',
            'format': 'json',
            'token': self.csrfToken,
            "title": "item:" + entityID if entityID.startswith("Q") else "property:"+entityID
        }
        res = self.session.post(self.apiUrl, data=parameters)
        return res.status_code == 200
