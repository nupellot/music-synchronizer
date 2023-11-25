import os

from string import Template

from flask import Flask, url_for, render_template, json, session, redirect
from flask import Blueprint, request, render_template, current_app
import json
from typing import Tuple, List

app = Flask(__name__)

app.config['db_config'] = {
    "host": "viaduct.proxy.rlwy.net:59582",
    "user": "root",
    "password": "fa-G1daFchA5CAgCCh4fAH5a-hFFEd3f",
    "database": "railway"
}

json_config = json.dumps(app.config['db_config'])
app.config['db_config'] = json_config

def select(db_config: dict, sql: str) -> Tuple[Tuple, List[str]]:
    result = tuple()
    schema = []
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()
    return result, schema

if __name__ == '__main__':
    app.run(host='viaduct.proxy.rlwy.net', port=3306)
    select(current_app.config['db_config'], "SELECT * FROM test")