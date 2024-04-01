import os
import sys
import time
import traceback
from multiprocessing.dummy import Pool

# self-defined module
import parser
import image_downloader
import uploader
import source_map

# third party module
import yaml
import updater
import click
# https://github.com/tiangolo/typer
from google.api_core.exceptions import GoogleAPICallError


class UfileTransfer:

    def __init__(self, root_path, config_file):
        self._root_path = root_path
        self.sql_parser = [] # array of db_parser
        self._config = config_file
        self.project_parser = parser.FileParser(source=self._config['parse_folder'])
        self.source_map = source_map.SourceMap(os.path.join(root_path, self._config["source_map_name"]))

        db_configs = [
            self._config["mysql"][0]["member"],
            self._config["mysql"][2]["global"],
            self._config["mysql"][3]["friend"],
            self._config["mysql"][5]["billing"],
            self._config["mysql"][7]["stat"],
            self._config["mysql"][8]["admin"],
            self._config["mysql"][9]["agent"],
            self._config["mysql"][10]["log"],
            self._config["mysql"][11]["event"],
            self._config["mysql"][12]["tree"],
            self._config["mysql"][13]["dynamic"],
            self._config["mysql"][14]["billboard"],
            self._config["mysql"][15]["fan"],
        ]

        pool = Pool(4)
        self.sql_parser = pool.map(parser.DBParser, db_configs)

        pool.close()
        pool.join()

        self._gcs_host = self._config["gcs_host"]

    def process_db(self, commit=True):
        # maybe we can use multi process
        for sql_parser in self.sql_parser:
            try:
                u = updater.SQLUpdater(sql_parser.config,
                                       source_map=self.source_map,
                                       gcs_host=self._gcs_host,
                                       conn=sql_parser.conn,
                                       commit=commit)

                for table in sql_parser.walk():
                    for result in sql_parser.parse(table):
                        column_name, match, primary_key_column_name, primary_key_value = result
                        if match is not None:
                            u.generate_update_sql(table, column_name, match[0], (primary_key_column_name, primary_key_value))
            except Exception as e:
                print(f"exception happen: {e}")
                print(traceback.print_exc())
            finally:
                # do update iterate each db
                u.update()
                self.source_map.commit()
                sql_parser.close()

                print(f"-- end of {sql_parser.config['db_name']} --")

    def process_file(self, commit=True):
        """start project parser"""
        for file in self.project_parser.walk():
            try:
                u = updater.FileUpdater(file,
                                        source_map=self.source_map,
                                        gcs_host=self._gcs_host,
                                        commit=commit)
                for result in self.project_parser.parse(file):
                    line_num, content, match = result
                    pos = f"file: {file}, line: {line_num}"
                    u.update_line(content, match, pos)

                self.source_map.commit()
            except Exception as e:
                print(f"exception happen: {e} file: {file}")
            finally:
                u.close()

    def process(self):
        self.process_file()
        self.process_db()

    def revert_file(self):
        for file in self.project_parser.walk():
            u = updater.FileUpdater(file)
            u.revert()

    def revert_db(self):
        for sql_parser in self.sql_parser:
            u = updater.SQLUpdater(sql_parser.config,
                                   source_map=self.source_map,
                                   gcs_host=self._gcs_host)

            u.revert()

    def revert(self):
        self.revert_db()
        self.revert_file()

    def close(self):
        self.source_map.close()


class UfileDownloader:

    """UfileDownloader download ufile images to local.

    depends on image downloader, SourceMap
    """

    def __init__(self, root_path, config):
        self._root_path = root_path
        self._source_map = source_map.SourceMap(config["source_map_name"])
        self._download_folder = config["download_folder"]
        self._image_downloader = image_downloader.ImageDownloader()

    def start(self):
        """start download"""
        for resource in self._source_map.get_undownloaded_resources():
            link = resource.name
            target_path = os.path.join(self._root_path, self._download_folder)

            if not os.path.exists(target_path):
                os.makedirs(target_path)

            store_path = os.path.join(target_path, resource.subpath)
            try:
                self._image_downloader.download_to_file(link, store_path)
                self._source_map.mark_downloaded(resource)
            except FileNotFoundError as e:
                raise e
            except Exception as e:
                print(f"error happen {e}")

            time.sleep(0.2)


class UfileUploader:

    """UfileUploader uploads ufiles to gcs

    read files from downloader and upload them
    """

    def __init__(self, root_path, config):
        self._root_path = root_path
        self._source_map = source_map.SourceMap(os.path.join(self._root_path, config["source_map_name"]))
        self._download_folder = config["download_folder"]

        credential_path = os.path.join(self._root_path, "google-application-credentials.json")
        self._uploader = uploader.Uploader(self._root_path,
                                           credential_path,
                                           gcs_path=config["gcs_path"],
                                           bucket_name=config["bucket_name"])

    def start(self):
        """start upload"""
        resource_map = {}
        for resource in self._source_map.get_unuploaded_resources():
            try:
                file_name = os.path.join(self._root_path, self._download_folder, resource.subpath)
                if not file_name in resource_map:
                    self._uploader.upload(file_name)
                    self._source_map.mark_uploaded(resource)
                    resource_map[file_name] = True
            except GoogleAPICallError:
                pass



if __name__ == "__main__":
    # how to use
    # for staging env
    # change your config to staging.yaml
    # First, we only need to parse the db and project files (without commit)
    # Second, downloads those files
    # Thrid, uploads those fiels
    # Forth, run transfer service again but this time with (commit). this
    # will make project and db changed

    root = os.path.dirname(os.path.abspath(__file__))

    config_file = os.path.join(root, "sql_dumper/prod.yaml")
    with open(config_file) as f:
        config = yaml.load(f)


    @click.group(chain=True)
    def cli():
        """This script provides ufile transfer utils.

         - transfer

         - downloader

         - uploader
        """
        pass

    @cli.command("transfer")
    @click.option("-c", "--commit", default=True, help="make db and file changed: ture or fale")
    @click.option("-t", "--target", default="all", help="run db or file transfer: db, file, or all")
    def start_ufile_transfer(commit, target):
        """start ufile transfer to extract ufile links from files and
        db and store in the source db
        """
        ut = UfileTransfer(root, config)
        commit = True if commit.lower() == 'true' else False

        if target == "db":
            ut.process_db(commit)
        elif target == "file":
            ut.process_file(commit)
        else:
            ut.process()
        ut.close()

    @cli.command("reverter")
    @click.option("-t", "--target", default="all", help="run db or file revert")
    def start_ufile_reverter(target):
        ut = UfileTransfer(root, config)
        if target == "db":
            ut.revert_db()
        elif target == "file":
            ut.revert_file()
        else:
            ut.revert()

        ut.close()

    @cli.command("download")
    def start_ufile_downloader():
        """start downloading ufile assets from the source db
        """
        ud = UfileDownloader(root, config)
        ud.start()

    @cli.command("upload")
    def start_ufile_uploader():
        """start uploading ufile assets to the gcs
        """
        up = UfileUploader(root, config)
        up.start()

    cli()
