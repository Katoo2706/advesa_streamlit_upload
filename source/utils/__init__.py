import streamlit as st

from .render_svg import render_svg
from .file_uploader import upload_csv
from .transformation import (map_customers, merge_dict_df)
from .emails import Emails


def send_upload_file(receiver, username, subject, file_url: str, folder_url: str):
    html_body = f"""\
                        <html>
                          <head>
                            <style>
                              body {{
                                background-color: #ffffff;
                                margin: 0;
                                padding: 20px;
                              }}
                              .whiteboard {{
                                background-color: #ffffff;
                                padding: 20px;
                                border: 1px solid #dddddd;
                                border-radius: 5px;
                                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                                margin-bottom: 20px;
                              }}
                              .footer {{
                                text-align: center;
                                font-size: 12px;
                                color: #888888;
                              }}
                            </style>
                          </head>
                          <body>
                            <div class="whiteboard">
                              <img src="https://advesa.com/wp-content/uploads/2022/05/AdvesaDigital_Logo_RGB_Colour.png" alt="Advesa Digital Logo" style="display: block; margin: 0 auto; width: 200px;">
                              <p style="text-align: center;">Hi {username}, thanks for submitting the data</p>
                              <p style="text-align: center;"><b>Please download your processed data via below url.</b></p>
                              <p style="text-align: center; font-size: 18px; font-weight: bold;"><a href="{file_url}">Download file</a></p>
                              <p style="text-align: center;">Otherwise, see all the submitted data via this url: <a href="{folder_url}">Go to folder</a></p>
                              <p style="text-align: center;">Have a nice day!</p>
                            </div>
                            <div class="footer">
                              Copyright by advesadigital @2024, contact: <a href="mailto:quan.ngo@advesa.com">quan.ngo@advesa.com</a>
                            </div>
                          </body>
                        </html>
                    """

    return Emails(
        sender_email=st.secrets["SENDER_EMAIL"],
        app_password=st.secrets["APP_PASSWORD"]
    ).send_email(receiver, subject, body=html_body)
