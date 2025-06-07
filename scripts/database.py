import pandas as pd
from sqlalchemy import create_engine
from scripts.config import DB_CONFIG

class PodcastDB:
    """Handles PostgreSQL connection and data uploads."""

    def __init__(self, db_config=DB_CONFIG):
        """
        Initialize with DB credentials.
        """
        self.config = db_config

    def create_connection(self):
        """
        Create and return a database connection.

        Returns:
            sqlalchemy.engine.Connection
        """
        try:
            db_params = f"{self.config['user']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['database']}"
            engine = create_engine(f"postgresql+psycopg2://{db_params}")
            return engine.connect()
        except Exception as e:
            raise RuntimeError(f"Failed to connect to database: {e}")

    def upload_to_db(self, df, tablename):
        """
        Upload DataFrame to specified PostgreSQL table.

        Args:
            df (pd.DataFrame): DataFrame to upload.
            tablename (str): Table name.

        Returns:
            None
        """
        try:
            conn = self.create_connection()
            df.to_sql(name=tablename, con=conn, if_exists="replace", index=False)
            conn.close()
        except Exception as e:
            raise RuntimeError(f"Failed to upload data to table {tablename}: {e}")
