import requests
import json


def authenticate(client_id, client_secret):
    url = "https://api.citivelocity.com/markets/cv/api/oauth2/token"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json"
    }
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
        'scope': '/api'
    }

    # For proxy support, add: proxies=proxies
    response = requests.post(url, data=payload, headers=headers)

    # Check if the request was successful
    response.raise_for_status()

    # Return the JSON response as a dictionary
    if response.status_code != 200:
        raise Exception(f"Authentication failed: {response.status_code} - {response.text}")
    try:
        response_data = response.json()
    except json.JSONDecodeError:
        raise Exception("Failed to parse JSON response from authentication")

    if 'access_token' not in response_data:
        raise Exception("Access token not found in response. Check your client credentials.")

    return response.json()


def get_tag_listings(access_token, client_id, category, sub_category, *optional_values, search_pattern=None, proxies=None):
    """
    Get tag listings from CitiVelocity API.
    
    Args:
        access_token (str): OAuth2 access token obtained from authenticate()
        client_id (str): Client ID for the API
        category (str): Main category for the tag (e.g., 'EQUITY')
        sub_category (str): Sub-category for the tag (e.g., 'DELTAONE')
        *optional_values: Any number of additional values to append to the prefix
        search_pattern (str, optional): Regex pattern to filter results
        proxies (dict, optional): Dictionary of proxies if needed
        
    Returns:
        dict: JSON response from the API
    """
    url = "https://api.citivelocity.com/markets/analytics/chartingbe/rest/external/authed/taglisting"
    
    # Construct the base prefix
    prefix_parts = [category, sub_category]
    prefix_parts.extend(optional_values)
    
    # Construct the payload
    payload = {
        "prefix": ".".join(prefix_parts)
    }
    
    # Add regex if search_pattern is provided
    if search_pattern:
        payload["regex"] = search_pattern
    
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
        'authorization': f'Bearer {access_token}'
    }
    
    params = {
        'client_id': client_id
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers,
                                 params=params, proxies=proxies
        )
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        raise


def get_identifier_info(access_token, client_id, citi_ids):
    """
    Convert Citi Equity Identifiers to other identifier types.
    
    :param access_token: OAuth2 access token obtained from authenticate()
    :param client_id: Client ID for the API
    :param citi_ids: List of Citi Equity Identifiers
        
    Returns:
        dict: JSON response containing identifier information
        
    Example:
        response = get_identifier_info(access_token, client_id, [306888, 56280, 92141])
        # Returns information for each ID including RIC, MIC, ETS, BBT, and ISIN
    """
    url = "https://api.citivelocity.com/markets/analytics/chartingbe/rest/external/authed/citiids/from"
    
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
        'authorization': f'Bearer {access_token}'
    }
    params = {
        'client_id': client_id
    }
    
    payload = {
        "ids": citi_ids
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting identifier info: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        raise


def get_citi_ids(access_token, client_id, queries):
    """
    Convert other identifier types to Citi Equity Identifiers.
    
    Args:
        access_token (str): OAuth2 access token obtained from authenticate()
        queries (list): List of query dictionaries with the following structure:
            [
                {
                    "productType": "STOCK" | "ETF" | "INDEX",
                    "identifier": str,
                    "identifierType": "RIC" | "BBT" | "ETS" | "ISIN",
                    "mic": str,  # Optional, see function docstring
                    "primaryOnly": bool  # Optional
                },
                ...
            ]
            
    Returns:
        dict: JSON response containing Citi IDs
        
    Example:
        queries = [
            {"productType": "STOCK", "identifier": "IBM.N", "identifierType": "RIC"},
            {"productType": "STOCK", "identifier": "IBM", "identifierType": "BBT", "mic": "XNYS"},
            {"productType": "STOCK", "identifier": "IBM", "identifierType": "BBT", "primaryOnly": True}
        ]
        response = get_citi_ids(access_token, queries)
    
    Note about MIC:
    Only works well for Stocks and ETFs. Must be one of the supported exchanges:
    ARCX, XAMS, XASE, XASX, XBRU, XCSE, XETR, XFRA, XHEL, XHKG, XJPX, XLIS,
    XLON, XNAS, XNCM, XNGS, XNMS, XNYS, XPAR, XSTO, XTKS
    """
    url = f"https://api.citivelocity.com/markets/analytics/chartingbe/rest/external/authed/citiids/to"
    
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
        'authorization': f'Bearer {access_token}'
    }
    
    payload = {
        "queries": queries
    }
    params = {
        'client_id': client_id
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting Citi IDs: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        raise


def get_timeseries(
    access_token,
    client_id,
    tags,
    start_date,
    end_date,
    frequency="DAILY",
    start_time=None,
    end_time=None,
    price_points="C",
    latest_only=False,

):
    """
    Fetch timeseries data from CitiVelocity API.
    
    Args:
        access_token (str): OAuth2 access token obtained from authenticate()
        client_id (str): Client ID for the API
        tags (list): List of data series tags to fetch (1-100 tags)
        start_date (str or int): Start date in YYYYMMDD format or as a date/datetime object
        end_date (str or int): End date in YYYYMMDD format or as a date/datetime object
        frequency (str, optional): Frequency of data. One of: 
                                'MONTHLY', 'WEEKLY', 'DAILY', 'HOURLY', 'MI10', 'MI01'.
                                Defaults to 'DAILY'.
        start_time (int, optional): Start time in HHMM format (for intraday frequencies)
        end_time (int, optional): End time in HHMM format (for intraday frequencies)
        price_points (str, optional): Price points to return. 'C' for Close, 'OHLC' for Open/High/Low/Close.
                                    Defaults to 'C'.
        latest_only (bool, optional): If True, return only the latest data point. Defaults to False.
        
    Returns:
        dict: JSON response containing the requested timeseries data
        
    Raises:
        requests.exceptions.RequestException: If the API request fails
        ValueError: If input validation fails
    """
    url = "https://api.citivelocity.com/markets/analytics/chartingbe/rest/external/authed/data"
    
    # Convert date objects to YYYYMMDD format if needed
    def format_date(d):
        import datetime
        if isinstance(d, (datetime.date, datetime.datetime)):
            return int(d.strftime('%Y%m%d'))
        elif isinstance(d, str):
            try:
                return int(d.replace('-', '').replace('/', ''))
            except ValueError:
                raise ValueError(f"Invalid date format: {d}. Use YYYYMMDD or date/datetime object.")
        return d
    
    # Prepare the request payload
    payload = {
        'startDate': format_date(start_date),
        'endDate': format_date(end_date),
        'tags': tags,
        'frequency': frequency.upper(),
        'pricePoints': price_points.upper(),
        'latestOnly': latest_only
    }
    
    # Add optional time parameters if provided
    if start_time is not None:
        payload['startTime'] = start_time
    if end_time is not None:
        payload['endTime'] = end_time
    
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
        'authorization': f'Bearer {access_token}'
    }
    params = {
        'client_id': client_id
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching timeseries data: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        raise



def get_metadata(access_token, client_id, tags, frequency="EOD"):
    """
    Fetch metadata for the given tags from CitiVelocity API.
    
    Args:
        access_token (str): OAuth2 access token obtained from authenticate()
        client_id (str): Client ID for the API
        tags (list): List of tags to fetch metadata for (1-1000 tags)
        frequency (str, optional): Frequency of data. Must be either 'EOD' or 'INTRADAY'. 
                                Defaults to 'EOD'. Note: modifiedTimes and endDate are only 
                                available for 'EOD' frequency.
                                
    Returns:
        dict: A dictionary containing metadata for the requested tags
        
    Example:
        metadata = get_metadata(
            access_token="your_access_token",
            tags=["COMMODITIES.SPOT.SPOT_GOLD"],
            frequency="EOD"
        )
    """
    if not tags or len(tags) == 0 or len(tags) > 1000:
        raise ValueError("Tags list must contain between 1 and 1000 items")
        
    if frequency not in ["EOD", "INTRADAY"]:
        raise ValueError("Frequency must be either 'EOD' or 'INTRADAY'")
    
    url = "https://api.citivelocity.com/markets/analytics/chartingbe/rest/external/authed/metadata"
    
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
        'authorization': f'Bearer {access_token}'
    }
    
    payload = {
        "tags": tags,
        "frequency": frequency
    }
    params = {
        'client_id': client_id
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        if hasattr(http_err, 'response') and http_err.response is not None:
            print(f"Response status code: {http_err.response.status_code}")
            print(f"Response content: {http_err.response.text}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        raise
