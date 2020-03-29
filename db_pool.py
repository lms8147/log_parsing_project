import sqlite3
from datetime import datetime


class LogParsingDB:
    db_name = "log_parsing_status.db"

    def __init__(self):
        self.__create_status_table__()
        self.__create_log_table__()

    def get_connection(self):
        return sqlite3.connect(LogParsingDB.db_name)

    def __create_status_table__(self):
        with self.get_connection() as conn:
            create_query = (
                "CREATE TABLE IF NOT EXISTS PARSING_STATUS"
                "("
                "LAST_READ_DATE DATE NOT_NULL DEFAULT CURRENT_TIMESTAMP,"
                "LAST_READ_LOG_START_LINE INTEGER DEFAULT 0,"
                "LAST_READ_LOG_END_LINE INTEGER DEFAULT 0"
                ");"
            )

            cur = conn.cursor()
            cur.execute(create_query)

            count_row_query = "SELECT count(*) FROM PARSING_STATUS;"
            cur.execute(count_row_query)
            rows = cur.fetchall()
            row_count = rows[0][0]

            if row_count == 0:
                insert_default_status_query = (
                    "INSERT INTO PARSING_STATUS(LAST_READ_LOG_START_LINE, LAST_READ_LOG_END_LINE) VALUES(0, 0)"
                )
                cur.execute(insert_default_status_query)

            conn.commit()

    def __create_log_table__(self):
        with self.get_connection() as conn:
            create_query = (
                "CREATE TABLE IF NOT EXISTS WAS_LOG"
                "("
                "LOG_ID VARCHAR(36) NOT NULL,"
                "FULL_LOG TEXT,"
                "MODIFIED BOOLEAN,"
                "LAST_MOD_DATE DATE DEFAULT CURRENT_TIMESTAMP"
                "PRIMARY KEY (LOG_ID)"
                ")"
            )
            cur = conn.cursor()
            cur.execute(create_query)
            conn.commit()

    def insert_or_replace_log(self, conn, log_id, full_log):
        insert_query = "INSERT OR REPLACE INTO WAS_LOG VALUES (?, ?, 1, datetime.now());"
        cur = conn.cursor()
        cur.execute(insert_query, (log_id, full_log))

    def get_last_log(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM WAS_LOG ORDER BY LAST_MOD_DATE DESC LIMIT 1")
            rows = cur.fetchall()
            return rows[0]

    def get_parsing_status(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("select * from PARSING_STATUS")
            rows = cur.fetchall()
            return rows[0]

    def update_parsing_status(self, conn, last_read_date, last_read_start_line, last_read_end_line):
        update_query = "UPDATE PARSING_STATUS SET LAST_READ_DATE = ?, LAST_READ_LOG_START_LINE = ?, LAST_READ_LOG_END_LINE = ?"
        cur = conn.cursor()
        cur.execute(update_query, (last_read_date, last_read_start_line, last_read_end_line))

