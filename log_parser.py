from db_pool import LogParsingDB
from datetime import datetime
import uuid


class LogParser:

    def __init__(self):
        pattern_a = r"\[(ERROR|INFO)\] (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (.*)"
        pattern_b = r"\[(ERROR|INFO |INFO)\]"

    def is_log_start(self, s):
        return self.__program_log_start__.match(s) is not None

    def parse_log(self, s):
        return self.__program_log_start__.match(s)


class LogToSqliteDB:

    def __init__(self):
        self.logParsingDB = LogParsingDB()
        self.logParser = LogParser()

    def __get_parsing_status__(self):
        return self.logParsingDB.get_parsing_status()

    def __get_log_file_name__(self, last_read_date):
        current_date = datetime.now().strftime('%Y-%m-%d')
        log_file_base_name = "a"
        if last_read_date.strftime('%Y-%m-%d') == current_date:
            log_file_name = log_file_base_name
        else:
            log_file_name = log_file_base_name + last_read_date.strftime('%Y%m%d')
        return log_file_name

    def __write_log_to_db__(self, start_line, end_line, last_read_date, log_id, full_log):
        with self.logParsingDB.get_connection() as conn:
            self.logParsingDB.insert_or_replace_log(conn, log_id, full_log)
            self.logParsingDB.update_parsing_status(last_read_date, start_line, end_line)
            conn.commit()

    def __write_log_file_to_db__(self, log_file_name, start_line, end_line, last_read_date):
        current_line = 0

        with open(log_file_name, 'r') as log_file:
            log_id = ""
            full_log = ""
            while True:
                line = log_file.readline()
                if not line:
                    break
                else:
                    current_line += 1
                    if current_line < start_line:
                        continue
                    elif current_line == start_line:
                        # log 시작점이 아니면 마지막 로그 가져옴
                        log_id, full_log = self.logParsingDB.get_last_log()

                    else:
                        if self.logParser.is_log_start(line):
                            # 완성된 로그 넣음
                            self.__write_log_to_db__(start_line, current_line - 1, last_read_date, log_id, full_log)

                            # 새로운 로그 초기화함
                            log_id = str(uuid.uuid1())
                            full_log = line

                        else:
                            # 로그 append 함
                            full_log += line

            self.__write_log_to_db__(start_line, current_line - 1, last_read_date, log_id, full_log)

    def parsing_log_file_to_db(self):
        last_read_date, start_line, end_line = logToSqliteDB.__get_parsing_status__()

        log_file_name = self.__get_log_file_name__(last_read_date)
        if start_line <= end_line:
            start_line = end_line + 1

        self.__write_log_file_to_db__(log_file_name, start_line, end_line, last_read_date)


if __name__ == "__main__":

    logToSqliteDB = LogToSqliteDB()
    logToSqliteDB.parsing_log_file_to_db()
