import pytest
import os
import updater
import source_map

@pytest.fixture
def source_log_map(root):
    fname = os.path.join(root, "test_source.db")
    return source_map.SourceMap(fname)


def test_db_updater(test_config, test_db_parsers, source_log_map):
    for parser in test_db_parsers:
        try:
            u = updater.SQLUpdater(
                parser.config,
                source_map=source_log_map,
                gcs_host=test_config["gcs_host"],
                commit=True)

            for table in parser.walk():
                for result in parser.parse(table):
                    column_name, match, primary_key_column_name, primary_key_value = result
                    if match is not None:
                        u.generate_update_sql(table, column_name, match[0], (primary_key_column_name, primary_key_value))
        except Exception as e:
            print(f"exception happen: {e}")

        finally:
            u.update()
            source_log_map.commit()
            parser.close()

            print(f"-- end of {table}--")

def test_db_revert(test_config, test_db_parsers, source_log_map):
    parser = test_db_parsers[0]
    u = updater.SQLUpdater(
        parser.config,
        source_map=source_log_map,
        gcs_host=test_config["gcs_host"],
    )

    u.revert()

def test_file_updater(test_config, test_file_parser, source_log_map):
    parser = test_file_parser()
    for file in parser.walk():
        u = updater.FileUpdater(file,
                                source_map=source_log_map,
                                gcs_host=test_config["gcs_host"])

        for result in parser.parse(file):
            line_num, content, match = result
            pos = f"file: {file}, line: {line_num}"
            u.update_line(content, match, pos)

        source_log_map.commit()
        u.close()

def test_file_revert(test_config, test_file_parser):
    parser = test_file_parser()
    files = parser.walk()
    for file in files:
        u = updater.FileUpdater(file)
        u.revert()
