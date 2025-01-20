#!/usr/bin/env python

# Make sure to install requests before running:
# > pip install requests
# Documentation for the requests library can be found here: http://docs.python-requests.org/en/master/

from typing import Dict, List, Optional
from datetime import datetime
import logging

from api_client import FoodTruckFinder
import utilities

class FoodTruckDisplay:
    def __init__(self):
        self.client = FoodTruckFinder()
        self.page = 1
        self.page_size = 10

    def get_data(self, day: str, time: str, offset: int) -> Dict:
        order_by = "applicant"
        fields = ["applicant", "location", "start24", "end24"]
        return self.client.get_data(fields, day=day, time=time, offset=offset, order_by=order_by)

    def display_page(self, data: List[Dict]) -> None:
        if not data:
            print("\nNo results found.\n")
            return
        utilities.print_results(data)

    def run(self, day: str, time: str) -> None:
        offset = 0
        while True:
            response = self.get_data(day, time, offset)
            
            if not response['response']:
                print("Error fetching data")
                break

            data = response['data']
            if not data:
                print("\nEnd of List. Thanks!\n")
                break

            self.display_page(data)

            if self.page == 1:
                user_input = input("See more results? (Y/N): ").lower()
                if user_input == 'y':
                    self.page += 1
                    offset += self.page_size
                    continue
                break
            else:
                user_input = input(f"Page {self.page} - Enter 'next', 'prev', or 'exit': ").lower()
                if user_input == 'exit':
                    break
                elif user_input == 'next':
                    offset += self.page_size
                    self.page += 1
                elif user_input == 'prev' and self.page > 1:
                    offset -= self.page_size
                    self.page -= 1

def main():
    display = FoodTruckDisplay()
    date = datetime.now()
    currDay = utilities.getWeekDay(date)
    currTime = utilities.getTime24(date)
    display.run(currDay, currTime)

if __name__ == "__main__":
    main()
