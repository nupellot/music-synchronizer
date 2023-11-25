import os

from string import Template

from flask import Flask, url_for, render_template, json, session, redirect
from flask import Blueprint, request, render_template, current_app
import json
from typing import Tuple, List

from typing import Optional

from pymysql import connect
from pymysql.cursors import Cursor
from pymysql.connections import Connection
from pymysql.err import OperationalError

app = Flask(__name__)

app.config['db_config'] = {
    "host": "viaduct.proxy.rlwy.net",
    "user": "root",
    "password": "fa-G1daFchA5CAgCCh4fAH5a-hFFEd3f",
    "database": "railway"
}

json_config = json.dumps(app.config['db_config'])
app.config['db_config'] = json_config

class DBContextManager:
    """Класс для подключения к БД и выполнения sql-запросов."""

    def __init__(self, config: dict):
        """
        Инициализация объекта подключения.
        Args:
             config: dict - Конфиг дял подключения к БД.
        """
        self.config: dict = config
        self.conn: Optional[Connection] = None
        self.cursor: Optional[Cursor] = None

    def __enter__(self) -> Optional[Cursor]:
        """
        Реализует логику входа в контекстный менеджер.
        Создает соединение к БД и возвращает курсор для выполнения запросов.
        Return:
            Курсор для работы с БД или NULL.
        """
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            if err.args[0] == 1045:
                print('Invalid login or password')
            elif err.args[0] == 1049:
                print('Check database name')
            else:
                print(err)
            return None

    def __exit__(self, exc_type, exc_val, exc_tr) -> bool:
        """
        Реализует логику выхода из контекстого менеджера для работы с БД.
        Закрывает соединение и курсор.
        Возвращаемое значение всего True для обеспечения сокрытия списка ошибок в консоли.
        Args:
            exc_type: Тип возможной ошибки при работе менеджера.
            exc_val: Значение возможной ошибки при работе менеджера.
            exc_tr: Traceback (подробный текст ошибки) при работе менеджера.
        """
        if exc_type:
            print(f"Error type: {exc_type.__name__}")
            print(f"DB error: {' '.join(exc_val.args)}")

        if self.conn and self.cursor:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()
            self.cursor.close()
        return True

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
    app.run(host='viaduct.proxy.rlwy.net', port=59582)
    select(current_app.config['db_config'], "SELECT * FROM test")