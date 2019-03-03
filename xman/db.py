import sqlite3


class TableMeta:
    def __init__(self, idx, column_name, column_type, is_null, default_value,
                 is_pk):
        self.idx = idx + 1
        self.column_name = column_name
        self.column_type = column_type
        self.is_null = is_null
        self.allow_null = is_null == 1 and 'Y' or 'N'
        self.default_value = default_value
        self.is_pk = is_pk
        self.pk_field = is_pk == 1 and 'Y' or 'N'


class DBUtils:
    def __init__(self, db_file):
        self.db_file = db_file

    def get_object_type(self):
        result = []
        with sqlite3.connect(self.db_file) as conn:
            c = conn.cursor()
            for row in c.execute(
                    "select type from sqlite_master group by type"):
                result.append(row[0].capitalize())
        return result

    def get_object_list(self, object_type):
        object_list = []
        with sqlite3.connect(self.db_file) as conn:
            c = conn.cursor()
            for _row in c.execute("select * from sqlite_master where type = ?",
                                  (object_type, )):
                print(_row)
                object_list.append(_row[1])
        return object_list

    def get_meta_of_table(self, table_name):
        meta_data = []
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            for row in cur.execute("PRAGMA table_info(%s)" % table_name):
                print(row)
                meta_data.append(
                    TableMeta(row[0], row[1], row[2], row[3], row[4], row[5]))
        return meta_data

    def get_meta_of_index(self, index_name):
        meta_data = []
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            for row in cur.execute("PRAGMA index_info(%s)" % index_name):
                print(row)
        return meta_data
