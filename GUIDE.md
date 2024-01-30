# GOOGLE DRIVE API

### Manage files and folders
[Document](https://developers.google.com/drive/api/reference/rest/v3)


# Create Oauth 2 token for external
### Step 1: Enable Google Drive API in the project.

### Step 2: Go to manage / API / credentials / OAuth consent screen
- App name
- User support email
- Email addresses


### Step 3: Go to Credentials
- Application type: Web application
- Name: Web client 1
- URIs 1: https://developers.google.com/oauthplayground (without / in the end)


### Step 4: Go to play grounds and get the token
- Url: https://developers.google.com/oauthplayground/
- Fill as below to get: Authorization code, Refresh token, Access Token
![authorize.png](media%2Fauthorize.png)


### Other wise, we dont need the authorization flow, we need to create a client id in Credentials
Desktop App => Copy Client ID, Client Secret
- For the first time, the system will need the privilege to get the data
- Quick start with python: [Python guide](https://developers.google.com/drive/api/quickstart/python)

# Docs in Google to upload fiels
[Google docs](https://developers.google.com/drive/api/guides/manage-uploads)

# Google API PYTHON CLIENT
[Docs](https://github.com/googleapis/google-api-python-client/blob/main/docs/README.md)

# LLM MODELS
https://streamlit.io/generative-ai


# Mapping dataset
[Country code](https://public.opendatasoft.com/explore/dataset/countries-codes/export/): `delimiter=";"`

[IP and Postal code](https://www.serviceobjects.com/blog/free-zip-code-and-postal-code-database-with-geocoordinates/)
```
mapping_df['filter_valid_ip']=mapping_df['first_ip'].str.split('.').str.len()

mapping_df = mapping_df.loc[mapping_df['filter_valid_ip'] == 4]
```
