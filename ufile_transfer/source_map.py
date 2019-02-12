"""SourceMap
This records the position and condition of the pattern we want to search. With these,
we can easily to update and revert the data.
"""
import sqlite3
from collections import namedtuple

# ok, ... use sqlite.. I give using csv up. :(

TYPE_DB = "db"
TYPE_FILE = "file"

class SourceMap:

    """SourceMap is a source map of content changed between before and after
    """

    def __init__(self, save_fname: str = None):
        self._store_path = ":memory:" if save_fname is None else save_fname
        self._conn = sqlite3.connect(self._store_path)
        self._cursor = self._conn.cursor()
        self._rows = []
        self._row_type = namedtuple("row", ["id", "type", "pos", "name", "subpath", "origin", "after", "uploaded", "downloaded"])

        create_sql_table = ("""CREATE TABLE IF NOT EXISTS source
                                (id integer PRIMARY KEY,
                                 type text NOT NULL,
                                 pos text NOT NULL,
                                 name text NOT NULL,
                                 subpath text NOT NULL,
                                 origin text,
                                 after text,
                                 uploaded INTEGER DEFAULT 0,
                                 downloaded INTEGER DEFAULT 0,
                                 unique (pos, name))""")

        self._cursor.execute(create_sql_table)
        self._conn.commit() # need to call commit to send change to the db server

    @property
    def row_type(self):
        return self._row_type

    def close(self):
        self._cursor.close()
        self._conn.close()

    def get_undownloaded_resources(self):
        """get undownloaded resources for downloader
        """
        sql = "SELECT * FROM source WHERE downloaded = 0"
        self._cursor.execute(sql)

        for row in map(self._row_type._make, self._cursor.fetchall()):
            yield row

    def get_unuploaded_resources(self):
        """grab files which are downloaded and unuploaded for uploader
        """
        sql = "SELECT * FROM source WHERE uploaded = 0 and downloaded = 1"
        self._cursor.execute(sql)

        for row in map(self._row_type._make, self._cursor.fetchall()):
            yield row

    def get_revert_sqls(self):
        sql = "SELECT origin FROM source WHERE type = ?"
        self._cursor.execute(sql, (TYPE_DB, ))

        for pos in self._cursor.fetchall():
            yield pos[0]

    def mark_downloaded(self, row):
        row = row._replace(downloaded=1)
        sql = "UPDATE source SET downloaded=? where name = ?"
        self._cursor.execute(sql, (row.downloaded, row.name))
        self._conn.commit()

    def mark_uploaded(self, row):
        row = row._replace(uploaded=1)
        sql = "UPDATE source SET uploaded=? where name = ?"
        self._cursor.execute(sql, (row.uploaded, row.name))
        self._conn.commit()

    def _add_in_batch(self, row):
        self._rows.append(row)

    def file_insert(self, origin, new, name, subpath, pos):
        row = self._row_type._make([None, TYPE_FILE, pos, name, subpath, origin, new, 0, 0])
        self._add_in_batch(row)

    def db_insert(self, origin, new, name, subpath, pos):
        row = self._row_type._make([None, TYPE_DB, pos, name, subpath, origin, new, 0, 0])
        self._add_in_batch(row)

    def commit(self):
        bind_var = ",".join(["?" for _ in self._row_type._fields])
        sql = f"INSERT INTO source VALUES ({bind_var})"
        try:
            if len(self._rows) != 0:
                self._cursor.executemany(sql, self._rows)
                self._conn.commit()
                self._rows = []
        except sqlite3.IntegrityError as e:
            pass
        except Exception as e:
            raise e

