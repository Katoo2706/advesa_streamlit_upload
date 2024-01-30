# Streamlit for marketing team

Instructions: [Instructions on Confluence.](https://advesagroup.atlassian.net/wiki/spaces/_/pages/2006319230?atlOrigin=eyJpIjoiMjJmYTFlMjM4MjBhNGJkMGJjMzI3ODkxZjUwY2ExMmEiLCJwIjoiYyJ9)
App URL: https://advesamarketing.streamlit.app/

### Input data
- KingSumo exported contestants file

### The returned data includes extra columns:
- _city: City name
- _country_code: Country code (2)
- _country: Country name
- _latitude, _longitude: Latitude + longitude
- is_customer_CB: Does the customer belong to our CB shop?
- is_customer_HA: Does the customer belong to our HA shop?
- file_name: The file name.
- clv from each customer.
- number of orders from each customer.

## Start

Requirement
```bash
python3.10 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
```

Run app / port 8501 as default
```bash
streamlit run app.py
```

