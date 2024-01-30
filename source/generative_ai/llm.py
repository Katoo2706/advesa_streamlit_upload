def llm_model():
    import streamlit as st
    from langchain.llms import OpenAI

    st.title("🔗 Generative AI Quickstart App")

    st.write("---")

    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

    def generate_response(input_text):
        llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
        st.info(llm(input_text))

    with st.form("my_form"):
        text = st.text_area("Enter text:", "Tell me a joke?")
        submitted = st.form_submit_button("Submit")
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
        elif submitted:
            generate_response(text)