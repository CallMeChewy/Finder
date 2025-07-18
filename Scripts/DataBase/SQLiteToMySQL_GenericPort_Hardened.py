
#!/usr/bin/env python3
"""
SQLiteToMySQL_GenericPort_Hardened.py
Standard: AIDEV-PascalCase-1.7

Purpose:
Portable, configurable utility to migrate an arbitrary SQLite database to MySQL.
Includes structured config file support and command-line argument parsing.

Author: Himalaya Project
"""

import sqlite3
import mysql.connector
import argparse
import json
import os
import sys

# Type mapping for SQLite to MySQL
TYPE_MAP = {
    "INTEGER": "INT",
    "TEXT": "VARCHAR(255)",
    "REAL": "FLOAT",
    "BLOB": "LONGBLOB",
    "NUMERIC": "FLOAT"
}

def LoadConfig(config_path):
    if not os.path.exists(config_path):
        print(f"Error: Config file '{config_path}' not found.")
        sys.exit(1)
    with open(config_path, "r") as f:
        return json.load(f)

def MigrateDatabase(sqlite_path, config):
    if not os.path.exists(sqlite_path):
        print(f"Error: SQLite file '{sqlite_path}' not found.")
        sys.exit(1)

    sqlite_conn = sqlite3.connect(sqlite_path)
    sqlite_cur = sqlite_conn.cursor()

    mysql_conn = mysql.connector.connect(**config)
    mysql_cur = mysql_conn.cursor()

    sqlite_cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in sqlite_cur.fetchall()]

    for table in tables:
        print(f"Processing table: {table}")

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
    print("Migration completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generic SQLite to MySQL Port Utility (Himalaya Hardened)")
    parser.add_argument("sqlite_db", help="Path to the SQLite .db file to migrate")
    parser.add_argument("--config", default="mysql_config.json", help="Path to MySQL config JSON file")

    args = parser.parse_args()
    config = LoadConfig(args.config)
    MigrateDatabase(args.sqlite_db, config)
