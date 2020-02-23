#!/usr/bin/env python
import requests

class FoodTruckFinder(object):
    """
    API Client class
    """
    def __init__(self):
        self.baseurl = "http://data.sfgov.org/resource/bbb8-hzi6.json"
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
        request_url = self.baseurl
        first_param = True
        if len(kwargs) > 0:
            filter_string = ""
            for a in kwargs:
                if first_param:
                    first_param = False
                else:
                    filter_string = filter_string + "&"
                if a == "day":
                    #filter by day of the week 
                    filter_string = filter_string + "dayofweekstr=" + kwargs[a]
                elif a == "where":
                    #filter by where clause 
                    filter_string = filter_string + "$where=" + kwargs[a]
                elif a == "query":
                    #use query format to filter result 
                    filter_string = filter_string + "$query=" + kwargs[a]
                elif a == "offset":
                    #offset result for pagination 
                    filter_string = filter_string + "$offset=" + str(kwargs[a])
                elif a == "limit":
                    #limit number of results returned 
                    filter_string = filter_string + "$limit=" + str(kwargs[a])
                elif a == "order":
                    #the field on which the result is ordered
                    filter_string = filter_string + "$order=" + kwargs[a]
                elif a == "fields":
                    #fields to be retrieved with API call. Used as select statement
                    if len(kwargs[a])==1:
                        filter_string = filter_string + "$select=" + kwargs[a]
                    else:
                        filter_string = filter_string + "$select=" + ",".join(kwargs[a])    
            request_url = request_url + "?" + filter_string

        print(request_url)
        response = requests.get(request_url)
        data = None
        if response.status_code == 200:
            data = response.json()
        else:
            #print("ERROR: Error retrieving data. Please try agin.")
            return {'data':data, 'response':False}

        return {'data':data, 'response':True}
