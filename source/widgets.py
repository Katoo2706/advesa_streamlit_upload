import time

import streamlit as st
from source.utils import (upload_csv, render_svg, merge_dict_df, map_customers, send_upload_file)
from source.generative_ai import llm_model
from source.geodata import GetGeoData
from source.conf import DatamartClient
from source.gdrive import upload_file_from_memory


# Function to run in the background

def process_upload_file(dataframe):
    processed_df = GetGeoData.get_demographic_dataframe(dataframe=dataframe, ip_column="IP")

    processed_df = map_customers(
        source_conn=DatamartClient,
        dataframe=processed_df,
        email_col="Email")

    return processed_df


def __home__(username, email):
    st.title("📤 Upload Giveaway files from Kingsumo")
    st.write("---")

    st.write(f"#### Hello {username},")

    instruction_html = """
        <p style="font-family: 'Helvetica Neue', sans-serif; font-size: 16px; color: auto; line-height: 1.6;">
            &nbsp 👉 Click "Browse files" and upload the CSV files.<br>
            &nbsp 👉 Data to return: Columns to mark CB's customers or HA's customer & geo-data.
        </p>
    """

    st.write(instruction_html, unsafe_allow_html=True)

    ga_df = upload_csv(title="Please upload Give away files from King Sumo (can upload multiple files):",
                       accept_multiple=True)
    if ga_df:
        st.success(f"Upload files successfully, number of files: {len(ga_df['data'])}. "
                   f"Data will be sent via your emails in the new few minutes! 😊")

        if 'PROCESS_DATA' not in st.session_state:
            st.session_state["PROCESS_DATA"] = True
        if st.session_state["PROCESS_DATA"]:
            df = merge_dict_df(ga_df['data'])

            processed_df = process_upload_file(df)

            upload_file = upload_file_from_memory(data=processed_df,
                                                  file_name=ga_df['name'],
                                                  folder_id=st.secrets["GDRIVE_FOLDER_ID"])

            send_upload_file(receiver=email,
                             username=username,
                             subject="🎁 Data submission on Advesa - Marketing tool",
                             file_url=upload_file.get('url'),
                             folder_url="https://drive.google.com/drive/folders/1AMI0rikBnYBF9d7k_517lPOsMWN-b8i1")

            st.session_state["PROCESS_DATA"] = False

            st.experimental_rerun()


def __generative_ai__(username):
    if username == 'kato':
        return llm_model()
    else:
        return st.info("Updating..")


def __body__(username, email):
    def page_home():
        __home__(username, email)

    def page_generative_ai():
        __generative_ai__(username)

    page_names_to_funcs = {
        "🏠 Home": page_home,
        "📚 Plugin": page_generative_ai
    }

    render_svg(open("./media/logo.svg").read(), width=200, sidebar=True)
    st.sidebar.write("#")
    page_nav = st.sidebar.selectbox("Navigators",
                                    page_names_to_funcs.keys())  # Display a select box in the sidebar

    # to choose a demo
    page_names_to_funcs[page_nav]()
