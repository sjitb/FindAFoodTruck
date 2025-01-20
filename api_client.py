#!/usr/bin/env python
import requests
import configparser
import logging

from typing import Dict, List, Any, Optional
from urllib.parse import urlencode
import requests
import logging
from requests.exceptions import RequestException
from pathlib import Path
import os

class FoodTruckFinder:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self._base_url = config['DEFAULT']['BASE_URL']
        self._app_token = config['DEFAULT']['APP_TOKEN']
        self._session = requests.Session()
        self._session.headers.update({
            "X-App-Token": self._app_token
        })
        self._max_retries = 3
        self._timeout = 10
        self._page_size = 10

    def _build_params(self, select_fields: List[str], **kwargs) -> Dict[str, str]:
        """Build query parameters for API request"""
        params = {
            "$select": ",".join(select_fields)
        }
        
        # Handle time-based filtering
        if 'day' in kwargs and 'time' in kwargs:
            time_val = kwargs.pop('time')
            params.update({
                "dayofweekstr": kwargs.pop('day'),
                "$where": f"start24<='{time_val}' AND end24>'{time_val}'"
            })
        
        # Handle pagination and sorting
        if 'order_by' in kwargs:
            params["$order"] = kwargs.pop('order_by')
            
        if 'offset' in kwargs:
            params["$offset"] = kwargs.pop('offset')
            params["$limit"] = self._page_size
            
        # Add remaining parameters
        params.update(kwargs)
        return params

    def _make_request(self, params: Dict[str, str]) -> Dict[str, Any]:
        """Make HTTP request with retries"""
        for attempt in range(self._max_retries):
            try:
                response = self._session.get(
                    self._base_url,
                    params=params,
                    timeout=self._timeout
                )
                response.raise_for_status()
                return {
                    'data': response.json(),
                    'response': True
                }
            except RequestException as e:
                logging.error(f"Request failed (attempt {attempt + 1}/{self._max_retries}): {str(e)}")
                if attempt == self._max_retries - 1:
                    return {
                        'data': None,
                        'response': False,
                        'error': str(e)
                    }
                continue

    def get_data(self, select_fields: List[str], **kwargs) -> Dict[str, Any]:
        """
        Fetch data from the API with the given parameters
        
        Args:
            select_fields: List of fields to select
            **kwargs: Additional query parameters
            
        Returns:
            Dict containing response data and status
        """
        try:
            params = self._build_params(select_fields, **kwargs)
            return self._make_request(params)
        except Exception as e:
            logging.exception("Unexpected error occurred")
            return {
                'data': None,
                'response': False,
                'error': str(e)
            }

    def __repr__(self) -> str:
        return f"APIClient(base_url={self._base_url})"
