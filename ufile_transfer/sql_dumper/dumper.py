import yaml
import os
import subprocess

# docker run -it mysql /usr/bin/mysqldump -h [MYSQL_HOST] -u [MYSQL_USER] --password=[MYSQL_PASSWORD] [MYSQL_DATABASE] > backup.sql

# BIN = "docker run --rm -it mysql:5.7 /usr/bin/mysqldump"
BIN = "mysqldump"

if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(root, "staging.yaml")
    with open(config_file) as f:
        config = yaml.load(f)


    # for content in config["mysql"]:
    #     print(content)
    member_db = config["mysql"][0]["member"]

    # script = f'{BIN} -h host.docker.internal --port={member_db["port"]} -u {member_db["username"]} --password={member_db["password"]} -d {member_db["db_name"]} > {os.path.join(root, "temp.sql")}'
    script = f'{BIN} -h {member_db["host"]} --port={member_db["port"]} -u {member_db["username"]} -d {member_db["db_name"]} --password={member_db["password"]} > {os.path.join(root, "temp.sql")}'
    print(script)

    process = subprocess.Popen(script.split(' '), stdout=subprocess.PIPE)
    out, err = process.communicate() # process.wait will wati process over

