import sqlite3


class BestScore():
    """
        Handling database related events
    """
    def __init__(self,name):
        self.name = name
        self.__db = None
        self.__cursor = None
        self.__open_db()
        self.__create_table()
        

    def __open_db(self):
        self.__db = sqlite3.connect(self.name)
        self.__db.row_factory = sqlite3.Row
        self.__cursor = self.__db.cursor()


    def __create_table(self):
        if self.__cursor:
            self.__cursor.execute(""" CREATE TABLE IF NOT EXISTS scores(
                                    id INTEGER PRIMARY KEY ASC,
                                    nazwa VARCHAR (50) NOT NULL,
                                    score VARCHAR (5) NOT NULL
                                ) """)


    def add_record(self,name,score):
        """
            Add record to database
        """

        self.__cursor.execute(""" INSERT INTO scores VALUES(NULL,?,?); """, (name,score))
        self.__db.commit()
        self.__db.close()


    def show_records(self):
        """
            Show records from database
        """
        result = []
        self.__cursor.execute(""" SELECT * FROM scores """)
        results = self.__cursor.fetchall()
        for row in results:
            result.append((int(row['score']), row['nazwa']))
            result.sort(reverse=True)
        self.__db.close()
        return result

    def remove_data(self):
        """
            Remove all data from database
        """

        self.__cursor.execute(""" DROP TABLE IF EXIST scores """)
        self.__db.commit()
        self.__db.close()


