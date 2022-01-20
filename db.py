import sqlite3

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connection(db_file)
        self.cursor = self.conn.cursor()

    def get_user_frogs_count(self, username):
        result = self.cursor.execure("SELECT `frog_count` FROM users WHERE `username` = ?", (username))
        return result.fetch()

    def get_chat_frog_combo_record(self, chatId):
        result = self.cursor.execute("SELECT `frog_combo_record` FROM stats WHERE `chat_id` = ?", (chatId))
        return result.fetch()

    def increment_user_frog_count(self, username):
        self.cursor.execute("UPDATE users SET `frog_count` = `frog_count` + 1 WHERE `username` = ?", (username))
        return self.conn.commit()

    def save_chat_record(self, newRecord, chatId):
        self.cursor.execute("UPDATE stats SET `frog_combo_record` = ? WHERE `chat_id` = ?", (newRecord, chatId))
        return self.conn.commit()
