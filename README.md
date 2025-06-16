from importlib.metadata import metadata

# CitiVelocity Python Client

A Python client for interacting with the CitiVelocity API.
this package does not offer functionality for intraday bulk exporter or intraday streaming

## Installation

You can install the package using pip:

I would recommend putting your client_id and client_secret in your environment variables
under CITI_CLIENT_ID and CITI_CLIENT_SECRET respectively, the api will automatically
pick those up for authentication.

```bash
pip install git+https://github.com/jblloyd14/citivelocity.git --upgrade --no-cache-dir
```

For development installation:

```bash
git clone https://github.com/jblloyd14/citivelocity.git
cd citivelocity
pip install -e .
```

## Usage
I would recommend putting your client_id and client_secret in your environment variables
under CITI_CLIENT_ID and CITI_CLIENT_SECRET respectively, the api will automatically
pick those up for authentication, else pass them when instantiating the API class.
```python
import citivelocity
cva = citivelocity.API(client_id='your_client_id', client_secret='your_client_secret')

spy_df = cva.timeseries(["EQUITY.EQIVOL.ETF.SPY.P.EQIVOL_SPOT.STRIKE_100.3M.CITI"], start_date='2025-03-31',
                        end_date='2025-06-13', frequency='DAILY', pd_dataframe=True)
print(spy_df.head())

|    |        x |        c | tag                                                    |
|---:|---------:|---------:|:-------------------------------------------------------|
|  0 | 20250331 | 0.XXXXX  | EQUITY.EQIVOL.ETF.SPY.P.EQIVOL_SPOT.STRIKE_100.3M.CITI |
|  1 | 20250401 | 0.XXXXX  | EQUITY.EQIVOL.ETF.SPY.P.EQIVOL_SPOT.STRIKE_100.3M.CITI |
|  2 | 20250402 | 0.XXXXX  | EQUITY.EQIVOL.ETF.SPY.P.EQIVOL_SPOT.STRIKE_100.3M.CITI |
|  3 | 20250403 | 0.XXXXX  | EQUITY.EQIVOL.ETF.SPY.P.EQIVOL_SPOT.STRIKE_100.3M.CITI |
|  4 | 20250404 | 0.XXXXX  | EQUITY.EQIVOL.ETF.SPY.P.EQIVOL_SPOT.STRIKE_100.3M.CITI |


metadata = .metadata(["EQUITY.EQIVOL.ETF.SPY.P.EQIVOL_SPOT.STRIKE_100.3M.CITI"])

print(metadata)
{'body':
    {'EQUITY.EQIVOL.ETF.SPY.P.EQIVOL_SPOT.STRIKE_100.3M.CITI': 
         {'description': 'SPY.P, 3M Spot Moneyness, 100',
          'modifiedTimes': [
              '2025-06-12T06:23:12Z[GMT]', 
              '2025-06-11T07:02:18Z[GMT]',
              '2025-06-10T06:57:07Z[GMT]',
              '2025-06-07T06:16:51Z[GMT]',
              '2025-06-06T06:29:09Z[GMT]'],
          'startDate': 20110103,
          'endDate': 20250611,
          'intraday': False}
     }, 
 'status': 'OK'
 }
```



## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
