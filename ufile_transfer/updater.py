import re
import io
import shutil
import os
import typing
import MySQLdb
from source_map import SourceMap


class FileUpdater:

    """read origin fie and update it inplace.
    we give it the content and target we want to replace
    """

    def __init__(self, filename, source_map:SourceMap=None, gcs_host=None, commit=True):
        self._source_map = source_map
        self._file = io.StringIO() if commit else None
        self._filename = filename
        # write file to the back file
        self._write_fname = self._filename + ".myback"

        self._gcs_host = gcs_host or "http://google.host/"
        self._commit = commit

        # a special flag for file has changed
        self._changed = False

    def update_line(self, content:str, match:typing.re.Match, pos):
        write_buffer = content

        if match is not None:
            target = match[0]
            subpath = target.split("/")[-1]
            new_target = self._gcs_host + subpath
            new_content = content.replace(target, new_target)
            self._changed = True

            if self._source_map is not None:
                self._source_map.file_insert(content, new_content, target, subpath, pos)

            write_buffer = new_content

        if self._commit:
            self._file.write(write_buffer)

    def _swap(self, target_one, target_two):
        temp_file_name = target_one + ".tmp"
        os.rename(target_one, temp_file_name)
        os.rename(target_two, target_one)
        os.rename(temp_file_name, target_two)

    def _copy_mod(self, src, dst):
        mode = os.stat(src).st_mode
        os.chmod(dst, mode)

    def swap_origin_file(self, target_name):
        # swap the origin file name and write file name
        # target <--> write_fname
        #
        # remember to resist the file mode
        # so we need to copy file mode from self._write_fname to
        # target_name(this is what we create)
        if self._changed:
            self._swap(target_name, self._write_fname)
            self._copy_mod(self._write_fname, target_name)

    def revert(self):
        if os.path.exists(self._write_fname):
            self._swap(self._filename, self._write_fname)

    def close(self):
        if self._changed and self._commit:
            with open(self._write_fname, 'w') as f:
                self._file.seek(0)
                shutil.copyfileobj(self._file, f)

            self.swap_origin_file(self._filename)

        if self._file is not None:
            self._file.close()


class SQLUpdater:

    def __init__(self, config, source_map:SourceMap=None, conn=None, gcs_host=None, commit=True):
        self._source_map = source_map
        self._config = config
        self._conn = conn or MySQLdb.connect(
            user=self._config["username"],
            password=self._config["password"],
            host=self._config["host"],
            port=self._config["port"],
            database=self._config["db_name"])

        self._cursor = self._conn.cursor()

        self._gcs_host = gcs_host or "http://google.host/"
        self._commit = commit
        self._update_sqls = []

    def generate_update_sql(self, table_name, column_name, target, conds:typing.Tuple[str, str]):
        # target is the goal we want to replace
        subpath = target.split("/")[-1]
        new_target = self._gcs_host + subpath
        sql = f"UPDATE {table_name} SET {column_name}='{new_target}' WHERE {conds[0]}={conds[1]}"

        if self._source_map is not None:

            revert_sql = f"UPDATE {table_name} SET {column_name}='{target}' WHERE {conds[0]}={conds[1]}"
            pos = f"table: {table_name} column: {column_name} {conds[0]}:{conds[1]}"
            self._source_map.db_insert(revert_sql, sql, target, subpath, pos)

        self._update_sqls.append(sql)

    def revert(self):
        sqls = [sql for sql in self._source_map.get_revert_sqls()]
        self._update_sqls = sqls
        self.update()

    def update(self):
        # only mysql-connector-python support multi..
        # NOTE: https://dev.mysql.com/downloads/connector/python/
        if self._commit:
            for sql in self._update_sqls:
                print(sql)
                self._cursor.execute(sql)

            self._conn.commit()

    def close(self):
        self._cursor.close()
        self._conn.close()