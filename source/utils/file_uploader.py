from typing import Any
from datetime import datetime

import streamlit as st
import pandas as pd


def upload_csv(title: str, accept_multiple: bool = False) -> dict[str, Any] | None:
    """

    :param title: Title of the function
    :param accept_multiple: Boolean: Accept multiple file
    :return: Dictionary contain:
        - 'name': "file-now" if 1 file or "{number_of_file}-files-{now}"
        - 'data': Data
    """
    files = st.file_uploader(label=title,
                             type=['csv'],
                             accept_multiple_files=accept_multiple)

    dict_files = {}
    a = 0
    if files:
        with st.spinner("In progress:"):
            for file in files:
                a += 1
                if accept_multiple:
                    try:
                        dataframe = pd.read_csv(file)  # read csv
                        dict_files[f"{a}_{file.name}"] = dataframe
                    except Exception as e:
                        st.warning(f"Invalid file: {e}")
                        return

        tz_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if len(files) == 1:
            return {
                'name': f"{files[0].name}_{tz_now}.csv",
                'data': dict_files
            }
        else:
            return {
                'name': f"{len(files)}_files_{tz_now}.csv",
                'data': dict_files
            }
