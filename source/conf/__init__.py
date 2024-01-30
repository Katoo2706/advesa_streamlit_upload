import streamlit as st
from .pg_connection import PGDatabaseConnection

try:
    # Data mart connection
    DM_PG_HOST = st.secrets["DATAMART_PG_HOST"]
    DM_PG_USER = st.secrets["DATAMART_PG_USER"]
    DM_PG_PASSWORD = st.secrets["DATAMART_PG_PASSWORD"]
    DM_PG_PORT = st.secrets["DATAMART_PG_PORT"]
    DM_PG_ECOMMERCE = st.secrets["DATAMART_PG_DB"]

    DatamartClient = PGDatabaseConnection(dbname=DM_PG_ECOMMERCE,
                                          user=DM_PG_USER,
                                          password=DM_PG_PASSWORD,
                                          host=DM_PG_HOST,
                                          port=DM_PG_PORT)
except Exception as e:
    print(f"Error connecting to Datamart: {e}")
    DatamartClient = None
