import re
import typing
import os
from collections import namedtuple

import yaml
import MySQLdb


class FileParser:

    """Parser accept the regular expression pattern and
    extract the content for you
    """

    def __init__(self, source=None, pattern:typing.re.Pattern=None):
        self._pattern = pattern or re.compile(r"(http|https)://.*\.ufile.*/(?P<name>[a-zA-Z0-9.]+)")
        self._source = source or "/Users/jing/Desktop/BackendApi"
        self.file_lst = []
        self._ignored_patterns = [".git", ".github", ".png", ".jpg", ".gif",
            ".phar", "p12", "pem", ".webp", "images/", "fonts/",
            "mock/", "css", "image/", "plugin/", "plugins/", ".xls",
            ".zip", ".DS_Store", "doc/", "update_img.php", ".myback",
        ]

    def _should_be_ignored(self, path:str) -> bool:
        for subpath in self._ignored_patterns:
            if subpath in path:
                return True
        return False

    def set_ignored_patterns(self, patterns:typing.List[str]):
        self._ignored_patterns = patterns

    @property
    def source(self):
        return self._source

    @source.setter
    def set_source(self, path:str):
        self._source = path

    def parse(self, file) -> typing.Tuple[int, str, typing.re.Match]:
        with open(file, 'r', errors='ignore') as f:
            for line_num, content in enumerate(f):
                match = self.extract(content)
                yield line_num, content, match

    def walk(self) -> typing.List[str]:
        for dirpath, _, files in os.walk(self._source):
            if not self._should_be_ignored(dirpath):
                for filename in files:
                    file = os.path.join(dirpath, filename)
                    if not self._should_be_ignored(file):
                        self.file_lst.append(file)

        return self.file_lst

    def extract_with_pattern(self, content, pattern:typing.re.Pattern) -> typing.re.Match[str]:
        match = pattern.search(content)
        return match

    def extract(self, content) -> typing.re.Match[str]:
        return self.extract_with_pattern(content, self._pattern)


class DBParser:

    """DBParser parse all table in database and search all column value
    contain pattern and extract it out
    """

    def __init__(self, config, pattern:typing.re.Pattern=None):
        self._config = config
        self._pattern = pattern or re.compile(r"(http|https)://.*\.ufile.*/(?P<name>[a-zA-Z0-9.]+)")
        self._conn = MySQLdb.connect(
            user=self._config["username"],
            password=self._config["password"],
            host=self._config["host"],
            port=self._config["port"],
            database=self._config["db_name"])

        self._cursor = self._conn.cursor()

        self._table = {}

    def _should_be_ignored(self, table_name:str) -> bool:
        if table_name in ["tb_op_log"]:
            return True

        return False

    def close(self):
        self._cursor.close()
        self._conn.close()

    @property
    def config(self):
       return self._config

    @property
    def conn(self):
        return self._conn

    def walk(self) -> typing.List[str]:
        """return all table name(except system's table) in the database and generate
        namedtuple of table schema
        """
        self._cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name like %s and table_schema = %s", ("tb%", self._config["db_name"],))
        table_names = [row[0] for row in self._cursor.fetchall() if not self._should_be_ignored(row[0])]

        # generate namedtuple for table schema
        for name in table_names:
            sql = "SELECT column_name FROM information_schema.columns WHERE table_schema=%s and table_name=%s"
            self._cursor.execute(sql, (self._config["db_name"], name))
            columns = [row[0] for row in self._cursor.fetchall()]
            # use rename to avoid naming conflict with some reserved words in python
            self._table[name] = namedtuple(name, columns, rename=True)

        return table_names

    def extract_with_pattern(self, content, pattern:typing.re.Pattern) -> typing.re.Match[str]:
        match = pattern.search(content)
        return match

    def extract(self, content) -> typing.re.Match[str]:
        return self.extract_with_pattern(content, self._pattern)

    def _get_table_all_record(self, table_name:str):
        sql = f"SELECT * FROM {table_name}"
        self._cursor.execute(sql)
        for row in map(self._table[table_name]._make, self._cursor.fetchall()):
            yield row

    def _get_table_primary_key_column(self, table_name:str):
        # show keys return
        # Table, Non_unique, Key_name, Seq_in_index, Column_name, Collation, Cardinality, Sub_part, Packed,..
        sql = f"SHOW KEYS FROM {table_name} WHERE Key_name = 'PRIMARY' "
        self._cursor.execute(sql)

        for row in self._cursor.fetchall():
            # check column is unique (basic condition of primary key)
            if row[1] == 0:
                return row[4]

    def parse(self, table) -> typing.Tuple[str, typing.re.Match, str, typing.T]:
        records = self._get_table_all_record(table)
        primary_key_column_name = self._get_table_primary_key_column(table)
        primary_key_value = None

        for record in records:

            for column_name in record._fields:
                value = getattr(record, column_name)
                if isinstance(value, str):
                    match = self.extract(value)
                    if primary_key_column_name is not None:
                        primary_key_value = getattr(record, primary_key_column_name)
                    yield column_name, match, primary_key_column_name, primary_key_value
                #     print(f"table: {table} index: {index} column_name: {column_names[index]} content: {match[0]}")


