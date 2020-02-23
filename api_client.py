#!/usr/bin/env python
import requests
import configparser

class FoodTruckFinder(object):
    """
    API Client class
    """
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.baseurl = config['DEFAULT']['BASE_URL']
        self.apptoken = config['DEFAULT']['APP_TOKEN']
        self.offset = 0 #keep track of pagination

    def getData(self, currDay, currTime, dataLimit, orderBy, fieldList, pageDir):
        """
        Function to Retrieve Data for the specific problem
        """

        #generate where clause to find food trucks open at the current time
        whereClause = "start24<'" + currTime + "'and end24>'" + currTime +"'"

        self.offset += pageDir*dataLimit
        result = self.getAPIData(day=currDay, where=whereClause, fields=fieldList, order=orderBy, limit=dataLimit, offset=self.offset)

        return result
        
    def getAPIData(self, **kwargs):
        """
        Function for general API call
        named parameters are used to filter the results
        Returns: Data as JSON and Boolean for success of data retrieval
        """
        requestUrl = self.baseurl
        appToken = self.apptoken
        requestUrl = requestUrl 
        firstParam = True
        if len(kwargs) > 0:
            filterString = ""
            for a in kwargs:
                if firstParam:
                    firstParam = False
                else:
                    filterString = filterString + "&"
                if a == "day":
                    #filter by day of the week 
                    filterString = filterString + "dayofweekstr=" + kwargs[a]
                elif a == "where":
                    #filter by where clause 
                    filterString = filterString + "$where=" + kwargs[a]
                elif a == "query":
                    #use query format to filter result 
                    filterString = filterString + "$query=" + kwargs[a]
                elif a == "offset":
                    #offset result for pagination 
                    filterString = filterString + "$offset=" + str(kwargs[a])
                elif a == "limit":
                    #limit number of results returned 
                    filterString = filterString + "$limit=" + str(kwargs[a])
                elif a == "order":
                    #the field on which the result is ordered
                    filterString = filterString + "$order=" + kwargs[a]
                elif a == "fields":
                    #fields to be retrieved with API call. Used as select statement
                    if len(kwargs[a])==1:
                        filterString = filterString + "$select=" + kwargs[a]
                    else:
                        filterString = filterString + "$select=" + ",".join(kwargs[a])    
            requestUrl = requestUrl + "?" + "$$app_token=" + appToken + "&" + filterString

        response = requests.get(requestUrl)
        data = None
        if response.status_code == 200:
            data = response.json()
        else:
            #print("ERROR: Error retrieving data. Please try agin.")
            return {'data':data, 'response':False}

        return {'data':data, 'response':True}
