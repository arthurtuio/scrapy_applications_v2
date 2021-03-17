from psycopg2.extras import DictCursor
from database.postgres_connector import PostgresConnector


class CredentialsParoquia:
    def __init__(self, pg_conn):
        self._pg_conn = pg_conn

    def get_all_not_synced_credentials(self):
        with self._pg_conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                self._get_all_not_synced_credentials_sql_template()
            )

            return cursor.fetchall()

    def sync_first_not_synced_credential(self):
        with self._pg_conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                self._sync_first_not_synced_credential_sql_template()
            )

    @staticmethod
    def _get_all_not_synced_credentials_sql_template():
        return """
            SELECT 
                *
            FROM 
                scrapy.credentials_paroquia_sem_datas
            WHERE 
                sync_status IS false
        """

    @staticmethod
    def _sync_first_not_synced_credential_sql_template():
        return """
            UPDATE scrapy.credentials_paroquia_sem_datas
            SET
                updated_at = now(),
                sync_status = True
            WHERE id = (
                SELECT id 
                FROM scrapy.credentials_paroquia_sem_datas
                WHERE sync_status IS False
                ORDER BY created_at
                LIMIT 1
            )
        """


# For testing purposes
if __name__ == '__main__':
    db_connection = PostgresConnector().connect_using_localhost_credentials()

    with db_connection as pg_conn:
        credenciais_paroquia = CredentialsParoquia(pg_conn)
        print(
            credenciais_paroquia.get_first_not_synced_credential()
        )
