import os
import requests
import pandas as pd
import json
from .utils import authenticate, get_timeseries, get_metadata, get_citi_ids, get_identifier_info, get_tag_listings

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
            
        self.base_url = "https://api.citelocity.com"
        self.token = None
        self._auth = authenticate(self.client_id, self.client_secret)


        def is_token_valid(self):
            """Check if the access token is still valid.

            Returns:
                bool: True if the token is valid, False otherwise.
            """
            now = int(pd.Timestamp.now().timestamp())
            return now - self._auth['consented_on'] < self._auth['expires_in']

    def get_etf_vol_data(self, ticker, vol_type, strikes=None, tenors=None, start_date=None, end_date=None):
        """
        Get equity volatility data.

        Args:
            ticker (str): Equity ticker symbol.
            vol_type (str): Type of volatility data to retrieve.
            strikes (list, optional): List of strike prices. Defaults to None.
            tenors (list, optional): List of tenors. Defaults to None.
            start_date (str, optional): Start date for the data in 'YYYY-MM-DD' format. Defaults to None.
            end_date (str, optional): End date for the data in 'YYYY-MM-DD' format. Defaults to None.

        Returns:
            pd.DataFrame: DataFrame containing the requested volatility data.
        """

        # Create tags
        return get_timeseries(self._auth, ticker, vol_type, strikes=strikes, tenors=tenors,
                              start_date=start_date, end_date=end_date)
