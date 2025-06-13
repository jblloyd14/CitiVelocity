import os
import requests
import pandas as pd
import json
from .utils import authenticate, get_timeseries, get_metadata, get_citi_ids, get_identifier_info, get_tag_listings, check_api_status

class API:
    token_url= "https://api.citivelocity.com/markets/cv/api/oauth2/token"
    
    def __init__(self, client_id=None, client_secret=None):
        """Initialize the API client.
        
        Args:
            client_id (str, optional): Citi API client ID. Defaults to CITI_CLIENT_ID environment variable.
            client_secret (str, optional): Citi API client secret. Defaults to CITI_CLIENT_SECRET environment variable.
            
        Raises:
            ValueError: If client credentials are not provided either as arguments or environment variables.
        """
        self.client_id = client_id or os.getenv('CITI_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('CITI_CLIENT_SECRET')
        
        if not all([self.client_id, self.client_secret]):
            raise ValueError(
                "Client credentials must be provided either as arguments or through "
                "CITI_CLIENT_ID and CITI_CLIENT_SECRET environment variables"
            )
            
        self.base_url = "https://api.citivelocity.com"
        self.token = None
        self._auth = authenticate(self.client_id, self.client_secret)


    def is_token_valid(self):
        """Check if the access token is still valid.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        now = int(pd.Timestamp.now().timestamp())
        return now - self._auth['consented_on'] < self._auth['expires_in']

    def timeseries(self, tags, start_date=None, end_date=None, frequency=None, start_time=None, end_time=None,
                   price_points="C", latest_only=False, pd_dataframe=True):
        """
        Get timeseries data for a given ticker and tags.

        :param tags: List of tags to retrieve data for.
        :param start_date: Start date for the data in 'YYYY-MM-DD' format. Defaults to None.
        :param end_date: End date for the data in 'YYYY-MM-DD' format. Defaults to None.
        :param frequency: Frequency of the data. One of 'DAILY', 'WEEKLY', 'MONTHLY', 'HOURLY'. Defaults to None.
        :param start_time: Start time for the data in 'HHMM' format. Defaults to None.
        :param end_time: End time for the data in 'HHMM' format. Defaults to None.
        :param price_points: Price points to return. 'C' for Close, 'OHLC' for Open/High/Low/Close. Defaults to 'C'.
        :param latest_only: If True, returns only the latest data point. Defaults to False.
        :param pd_dataframe: If True, returns a pandas DataFrame. Defaults to True.
        :return: A pandas DataFrame containing the requested timeseries data or a dictionary if pd_dataframe is False.

        Example:
        data = apit.timeseries(
            tags=['COMMODITIES.SPOT.SPOT_GOLD'],
            start_date='2022-01-01',
            end_date='2022-12-31',
            frequency='DAILY',
            start_time='0000',
            end_time='2359',
            price_points='OHLC')
        """
        if not self.is_token_valid():
            self._auth = authenticate(self.client_id, self.client_secret)

        data = get_timeseries(
            self._auth['access_token'],self.client_id, tags, start_date=start_date, end_date=end_date, frequency=frequency,
            start_time=start_time, end_time=end_time, price_points=price_points, latest_only=latest_only
        )
        if pd_dataframe:
            return pd.DataFrame(data)
        else:
            return data


    def metadata(self, tags, frequency="EOD"):
        """
        Get metadata for specified tags.

        :param tags: List of tags to retrieve metadata for. Defaults to None.
        :param frequency: Frequency of the data. Defaults to "EOD" "intraday" is the other option.
        :return: A dictionary containing the metadata for the specified tags.
        """
        if not self.is_token_valid():
            self._auth = authenticate(self.client_id, self.client_secret)

        data = get_metadata(self._auth['access_token'], self.client_id, tags=tags, frequency=frequency)

        return data