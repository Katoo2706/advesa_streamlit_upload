import pandas as pd
import polars as pl
import numpy as np


def get_file_to_db(path, target_conn):
    mapping_df = pd.read_csv(path,
                             header=None,
                             names=["first_ip", "last_ip", "continent_code", "country_code", "region_name", "city",
                                    "lat", "lon"])

    converted_ip_address = mapping_df.loc[mapping_df["first_ip"].str.len() == 7]

    target_conn.batch_insert(
        dataframe=converted_ip_address,
        schema="streamlit",
        table="mapping_ip",
        if_exists="append"
    )

    target_conn.execute_query(
        """
        ALTER TABLE geodata.mapping_ip
        ADD CONSTRAINT unique_ip_range UNIQUE("first_ip", "last_ip");
        """
    )


def merge_dict_df(dataframes_dict: dict):
    """
    This method will process multiple csv file as a dictionary and concat all into 1 file
    :param dataframes_dict:
    :return:
    """
    # Concatenate all DataFrames into a single DataFrame
    final_dataframe = pd.concat(dataframes_dict.values(), ignore_index=True)

    # Add a new column "file_name" to mark the source file
    final_dataframe['file_name'] = [file_name for file_name in dataframes_dict.keys() for _ in
                                    range(len(dataframes_dict[file_name]))]

    return final_dataframe


def map_customers(source_conn, dataframe, email_col: str):
    country_code_data = source_conn.batch_fetch_data(
        f"""
            SELECT 
                "email" as "{email_col}",
                "date_created",
                "store_name"
            FROM streamlit.customers_list_cb_ha;
        """
    )

    dataframe[email_col] = dataframe[email_col].str.strip()

    country_code_df = pd.json_normalize(country_code_data)

    cb_customers = country_code_df.loc[country_code_df["store_name"] == "CB"].rename(
        columns={
            "store_name": "is_customer_CB",
            "date_created": "date_created_CB"
        }
    )

    ha_customers = country_code_df.loc[country_code_df["store_name"] == "HA"].rename(
        columns={
            "store_name": "is_customer_HA",
            "date_created": "date_created_HA"
        }
    )

    final_df = dataframe.merge(
        cb_customers,
        on=email_col,
        how='left'
    ).merge(
        ha_customers,
        on=email_col,
        how='left'
    )
    final_df["is_customer_CB"] = np.where(
        final_df["is_customer_CB"] == 'CB',
        True,
        False
    )

    final_df["is_customer_HA"] = np.where(
        final_df["is_customer_HA"] == 'HA',
        True,
        False
    )

    # use polars to map with customers clv
    customers_clv_data = source_conn.batch_fetch_data(
        f"""
            SELECT
                email as "{email_col}", 
                first_order_date,
                store_name, order_total_cad, order_count
            FROM streamlit.clv_by_customers_ha_cb;
            """
    )

    customers_clv_ha = pl.from_records(customers_clv_data).filter(pl.col("store_name") == "HA")
    customers_clv_ha = customers_clv_ha.rename(
        {
            "order_total_cad": "HA_order_total_cad",
            "order_count": "HA_order_count",
            "first_order_date": "HA_first_order_date"
        }
    ).select([email_col, "HA_order_total_cad", "HA_order_count", "HA_first_order_date"])

    customers_clv_cb = pl.DataFrame(customers_clv_data).filter(pl.col("store_name") == "CB")
    customers_clv_cb = customers_clv_cb.rename(
        {
            "order_total_cad": "CB_order_total_cad",
            "order_count": "CB_order_count",
            "first_order_date": "CB_first_order_date"
        }
    ).select([email_col, "CB_order_total_cad", "CB_order_count", "CB_first_order_date"])

    final_pl_df = pl.from_pandas(final_df)

    final_pl_df = final_pl_df.join(
        customers_clv_ha,
        on=email_col,
        how="left"
    ).join(
        customers_clv_cb,
        on=email_col,
        how="left"
    )

    df = final_pl_df.to_pandas()
    return df

