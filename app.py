import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
from source.widgets import __body__
from partials import __footer__

# config page
st.set_page_config(page_title="Advesa tools",
                   page_icon="./media/favicon.png",
                   layout="wide")

__login__obj = __login__(auth_token="courier_auth_token",
                         company_name="Advesa",
                         width=200, height=250,
                         logout_button_name='Logout', hide_menu_bool=False,
                         hide_footer_bool=False,
                         lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = __login__obj.build_login_ui()
username = __login__obj.get_username()
email = __login__obj.get_email()

if LOGGED_IN:
    __body__(username, email)
    __footer__()
