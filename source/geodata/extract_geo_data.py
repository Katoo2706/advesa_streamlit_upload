# !pip install maxminddb-geolite2
# !pip install ip2geotools
import pandas as pd


class GetGeoData:
    def __init__(self) -> None:
        pass

    # @staticmethod
    # def ip2_extract_demo(ip):
    #     from ip2geotools.databases.noncommercial import DbIpCity

    #     geo = DbIpCity.get(ip, api_key = 'free').__dict__
    #     return geo if geo is not None else None

    @staticmethod
    def api_ip(ip):
        import json
        import urllib.request
        try:
            GEO_IP_API_URL = 'http://ip-api.com/json/'

            # Creating request object to GeoLocation API
            req = urllib.request.Request(GEO_IP_API_URL + ip)
            # Getting in response JSON
            response = urllib.request.urlopen(req).read()

            # Loading JSON from text to object
            json_response = json.loads(response.decode('utf-8'))

            # Print country
            return {
                '_city': json_response['city'],
                '_country_code': json_response['countryCode'],
                '_country': json_response['country'],
                '_latitude': json_response['lat'],
                '_longitude': json_response['lon']
            }

        except Exception as e:
            print(e)

    @staticmethod
    def geolite_extract_demographic(ip):
        from geolite2 import geolite2

        geo = geolite2.reader()
        try:
            x = geo.get(ip)
            return x if x is not None else None
        except Exception as e:
            print(e)
            return None

    # not change the self data
    @classmethod
    def get_demographic_dataframe(cls, dataframe, ip_column: str):
        # 1. use geolite
        dataframe['geodata'] = dataframe[ip_column].apply(cls.geolite_extract_demographic)

        dataframe = pd.concat(
            [
                dataframe.drop(columns=["geodata"]),
                pd.json_normalize(dataframe["geodata"])[[
                    'city.names.en',
                    'registered_country.iso_code',
                    'registered_country.names.en',
                    'location.latitude',
                    'location.longitude']]
            ], axis=1  # by col
        ).rename(
            columns={
                'city.names.en': '_city',
                'registered_country.iso_code': '_country_code',
                'registered_country.names.en': '_country',
                'location.latitude': '_latitude',
                'location.longitude': '_longitude'
            }
        )

        # 2. use ip2
        dataframe_2 = dataframe[dataframe['_country'].isnull()].reset_index(drop=True)
        dataframe_2['geo_data'] = dataframe_2[ip_column].apply(cls.api_ip)
        dataframe_2 = pd.concat(
            [
                dataframe_2.drop(columns=[
                    'geo_data',
                    '_city',
                    '_country_code',
                    '_country',
                    '_latitude',
                    '_longitude'
                ]),
                pd.json_normalize(dataframe_2['geo_data'])[[
                    '_city',
                    '_country_code',
                    '_country',
                    '_latitude',
                    '_longitude']]
            ], axis=1  # by col
        )

        final_df = pd.concat(
            [
                dataframe.loc[dataframe['_country'].notnull()],
                dataframe_2
            ], axis=0
        ).reset_index(drop=True)

        return final_df
