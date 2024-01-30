import psycopg2
from sqlalchemy import create_engine


class PGDatabaseConnection:
    """
    Connection to Cloud Postgres Data mart
    """

    def __init__(self, dbname, user, password, host, port):
        """
        Constructor for the DatabaseConnection class.
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect_to_db(self):
        """
        Connect to the Postgres database and return a connection object.
        """
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return conn
        except psycopg2.Error as e:
            print(e)
            return None

    def execute_query(self, query, values=None):
        """
        Execute a query on the connected Postgres database.
        """
        with self.connect_to_db() as conn:
            cur = conn.cursor()
            cur.execute(query, values) if values else cur.execute(query)

    def fetch_data(self, query, values=None):
        """
        Fetch one data from the connected Postgres database.
        """
        with self.connect_to_db() as conn:
            cur = conn.cursor()
            if values:
                cur.execute(query, values)
            else:
                cur.execute(query)
            result = cur.fetchone()
        return result

    def batch_fetch_data(self, query) -> dict:
        """
        Fetch all data from the connected Postgres database.
        """
        with self.connect_to_db() as conn:
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()

        col_names = [desc[0] for desc in cur.description]
        data = [dict(zip(col_names, row)) for row in rows]
        return data

    def batch_insert(self, dataframe, schema: str, table: str, if_exists: str, chunksize: int = None,
                     index: bool = False):
        """
        Insert dataframe to Postgres database
        """
        with self.connect_to_db() as conn:
            engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)

            dataframe.to_sql(name=table, schema=schema, con=engine, chunksize=chunksize, index=index,
                             if_exists=if_exists)

            conn.commit()

    def batch_upsert_dataframe(self, dataframe, unique_columns: list, schema: str, table: str):
        """
        Perform a batch upsert using the provided DataFrame.
        """
        df_columns = dataframe.columns
        update_columns = [column for column in df_columns if column not in unique_columns]

        # Convert DataFrame to a list of records
        records = dataframe.to_dict(orient='records')

        # Build the SQL query for batch upsert
        sql_query = f"""
            INSERT INTO {schema}.{table}({', '.join(f'"{col}"' for col in df_columns)})
            VALUES ({', '.join('%({})s'.format(col) for col in df_columns)})
            ON CONFLICT ({', '.join(f'"{col}"' for col in unique_columns)}) DO UPDATE
            SET {', '.join(f'"{col}" = EXCLUDED."{col}"' for col in update_columns)}
        """

        # Perform the batch upsert
        with self.connect_to_db() as conn:
            cur = conn.cursor()
            for record in records:
                cur.execute(sql_query, record)
            conn.commit()
