import streamlit as st


def render_svg(img_url, width, sidebar: bool):
    """Renders the given svg string."""

    import base64
    b64 = base64.b64encode(img_url.encode('utf-8')).decode("utf-8")
    html = f'<img width={width} src="data:image/svg+xml;base64,%s"/>' % b64
    if sidebar:
        st.sidebar.write(html, unsafe_allow_html=True)
    else:
        st.write(html, unsafe_allow_html=True)
