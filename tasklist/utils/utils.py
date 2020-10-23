# pylint:disable=missing-module-docstring, missing-function-docstring
import json
import os
import os.path

import mysql.connector as cnt


def get_config_filename():
    return os.path.join(
        os.path.dirname(__file__),
        '..',
        'config',
        'config.json',
    )


def get_config_test_filename():
    return os.path.join(
        os.path.dirname(__file__),
        '..',
        'config',
        'config_test.json',
    )


def get_app_secrets_filename():
    return os.path.join(
        os.path.dirname(__file__),
        '..',
        'config',
        'db_app_secrets.json',
    )


def get_admin_secrets_filename():
    return os.path.join(
        os.path.dirname(__file__),
        '..',
        'config',
        'db_admin_secrets.json',
    )


def run_script(filename_script, filename_config, filename_secrets):
    with open(filename_script, 'r') as file:
        script = file.read()
    with open(filename_config, 'r') as file:
        config = json.load(file)
    with open(filename_secrets, 'r') as file:
        secrets = json.load(file)
    conn = cnt.connect(
        host=config['db_host'],
        database=config['database'],
        user=secrets['user'],
        password=secrets['password'],
    )
    with conn.cursor() as cursor:
        # One has to iterate through the results to get them executed properly
        # when using multi=True in this library. Makes sense after reflecting
        # on it: each cursor has to be exhausted before emitting another
        # command. Docs are not that clear, though:
        # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
        for _ in cursor.execute(script, multi=True):
            pass
    conn.commit()
    conn.close()


def run_all_scripts(scripts_dir, filename_config, filename_secrets):
    filenames = sorted([
        filename for filename in os.listdir(scripts_dir)
        if filename.endswith('.sql')
    ])
    for filename in filenames:
        run_script(
            os.path.join(scripts_dir, filename),
            filename_config,
            filename_secrets,
        )
