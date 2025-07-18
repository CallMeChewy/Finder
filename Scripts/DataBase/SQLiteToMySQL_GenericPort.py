
#!/usr/bin/env python3
"""
SQLiteToMySQL_GenericPort.py
Standard: AIDEV-PascalCase-1.7

Purpose:
Generic utility to port an arbitrary SQLite database to MySQL for development, testing,
or data analysis purposes. Handles tables, columns, primary keys, and basic data transfer.

Author: Himalaya Project
"""

import sqlite3
import mysql.connector

# CONFIGURATION
SQLITE_DB_PATH = "SourceDatabase.db"
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "your_mysql_user",
    "password": "your_mysql_password",
    "database": "TargetDatabase"
}

TYPE_MAP = {
    "INTEGER": "INT",
    "TEXT": "VARCHAR(255)",
    "REAL": "FLOAT",
    "BLOB": "LONGBLOB",
    "NUMERIC": "FLOAT"
}

def MigrateDatabase():
    sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
    sqlite_cur = sqlite_conn.cursor()

    mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
    mysql_cur = mysql_conn.cursor()

    # Get list of tables
    sqlite_cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in sqlite_cur.fetchall()]

    for table in tables:
        print(f"Processing table: {table}")

        # Fetch schema
        sqlite_cur.execute(f"PRAGMA table_info({table});")
        columns_info = sqlite_cur.fetchall()

        column_defs = []
        primary_keys = []
        for col in columns_info:
            col_name = col[1]
            col_type = col[2].upper()
            col_type_mysql = TYPE_MAP.get(col_type, "VARCHAR(255)")
            column_defs.append(f"`{col_name}` {col_type_mysql}")
            if col[5]:  # PK flag
                primary_keys.append(f"`{col_name}`")

        if not column_defs:
            continue

        create_stmt = f"CREATE TABLE IF NOT EXISTS `{table}` ({', '.join(column_defs)}"
        if primary_keys:
            create_stmt += f", PRIMARY KEY ({', '.join(primary_keys)})"
        create_stmt += ");"

        mysql_cur.execute(create_stmt)
        mysql_conn.commit()

        # Transfer data
        columns = [col[1] for col in columns_info]
        col_list = ", ".join(f"`{c}`" for c in columns)
        placeholders = ", ".join(["%s"] * len(columns))

        sqlite_cur.execute(f"SELECT {col_list} FROM `{table}`;")
        rows = sqlite_cur.fetchall()

        if rows:
            insert_stmt = f"INSERT INTO `{table}` ({col_list}) VALUES ({placeholders});"
            mysql_cur.executemany(insert_stmt, rows)
            mysql_conn.commit()
            print(f"Inserted {len(rows)} rows into `{table}`")

    sqlite_conn.close()
    mysql_conn.close()
    print("Generic migration completed.")

if __name__ == "__main__":
    MigrateDatabase()
