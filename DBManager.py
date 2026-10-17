import sqlite3
import pathlib
import os

def createDB(dbAddress : pathlib.Path):
    conn = sqlite3.connect(dbAddress)
    cursor = conn.cursor()

    cursor.executescript("""
    PRAGMA foreign_keys = ON;   -- SQLite doesn't enforce FKs unless this is set (per connection)
    
    CREATE TABLE food_nutrient (
        id                  INTEGER PRIMARY KEY,
        fdc_id              INTEGER NOT NULL,   -- -> food.fdc_id
        nutrient_id         INTEGER NOT NULL,   -- -> nutrient.id
        amount              REAL,               -- per 100 g edible portion
        data_points         INTEGER,
        min                 REAL,
        max                 REAL,
        median              REAL,
        percent_daily_value REAL
    );

    CREATE INDEX idx_fn_fdc_nutrient ON food_nutrient (fdc_id, nutrient_id);
    CREATE INDEX idx_fn_nutrient     ON food_nutrient (nutrient_id);
    """)

def getDBConnection(dbAddress : pathlib.Path):
    conn = sqlite3.connect(dbAddress)
    return conn

def deleteDatabase(dbAddress : pathlib.Path):
    os.remove(dbAddress.absolute())

dbAddress : pathlib.Path = pathlib.Path("Ingredients.db")

