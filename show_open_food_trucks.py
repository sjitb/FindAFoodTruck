#!/usr/bin/env python

# Make sure to install requests before running:
# > pip install requests
# Documentation for the requests library can be found here: http://docs.python-requests.org/en/master/

import requests
from datetime import datetime
import os

#custom libraries
import utilities
from api_client import FoodTruckFinder



def main():
    """
    Driver function for CLI
    """

    print("Launching App")
    print("################ TIME TO FIND SOME FOOD TRUCKS ################")
    date = datetime.now()
    currDay = utilities.getWeekDay(date)
    currTime = utilities.getTime24(date)

    #fields to be displayed
    fieldList = ['applicant','location']
    #field by which the result is ordered.
    orderBy = 'applicant'

    pageDir = 0
    page = 1

    #get pagination info from user
    offset = input("How many food trucks do you want to see in a page: ")

    if offset.isdigit():
        offset = int(offset)
    else:
        print("Sorry, not a valid input")
        return

    #create an instance of the FoodTruckFinder class
    foodTruckClient = FoodTruckFinder()
    res = foodTruckClient.getData(currDay,currTime,offset,orderBy,fieldList,pageDir)

    while True:
        if res['response']:
            data = res['data']
            if len(data) == 0:
                print("\nEnd of List. Thanks!\n")
                break

            utilities.print_results(data)    

            if page == 1:
                userInput = input("See more results? (Y/N): ").lower()
                if userInput == "y" or userInput == "next":
                    userInput = "next"
                elif userInput == "n":
                    userInput = "exit"
                else:
                    userInput = input("Not a valid input. See more results? (Y/N): ").lower()
            else:
                userInput = input("Page:" + str(page) +"(next, prev, exit): ").lower()

            if userInput == "next":
                pageDir = 1
                page += 1
                res = foodTruckClient.getData(currDay,currTime,offset,orderBy,fieldList,pageDir)
            elif userInput == "prev":
                pageDir = -1
                page -= 1
                res = foodTruckClient.getData(currDay,currTime,offset,orderBy,fieldList,pageDir)
            elif userInput == "exit":
                break
            else:
                userInput = input("Not a valid input. Go to (next, prev, exit): ").lower()

        else:
            print("ERROR: Error retrieving data. Please try agin.")
            break
    return
if __name__ == "__main__":
    main()