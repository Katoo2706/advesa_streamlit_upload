import streamlit as st
from pymongo import MongoClient
from .pg_connection import PGDatabaseConnection


def get_postgres_connection():
    try:
        # Data mart connection
        DM_PG_HOST = st.secrets["DATAMART_PG_HOST"]
        DM_PG_USER = st.secrets["DATAMART_PG_USER"]
        DM_PG_PASSWORD = st.secrets["DATAMART_PG_PASSWORD"]
        DM_PG_PORT = st.secrets["DATAMART_PG_PORT"]
        DM_PG_ECOMMERCE = st.secrets["DATAMART_PG_DB"]

        return PGDatabaseConnection(dbname=DM_PG_ECOMMERCE,
                                    user=DM_PG_USER,
                                    password=DM_PG_PASSWORD,
                                    host=DM_PG_HOST,
                                    port=DM_PG_PORT)
    except Exception as e:
        print(f"Error connecting to Datamart: {e}")
        return None


def get_mongo_connection(database):
    try:
        MONGO_URI = st.secrets["MONGO_ATLAS_URI"]
        return MongoClient(MONGO_URI)[database]
    except Exception as e:
        print(f"Error connecting to Mongo Atlas: {e}")


DatamartClient = get_postgres_connection()
MongoConnection = get_mongo_connection(database='hrm')
