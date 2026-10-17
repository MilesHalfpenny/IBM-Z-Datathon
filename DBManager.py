import sqlite3
import pathlib
import os

def createDB(dbAddress : pathlib.Path):
    conn = sqlite3.connect(dbAddress)
    cursor = conn.cursor()

    cursor.executescript("""
    PRAGMA foreign_keys = ON;   -- SQLite doesn't enforce FKs unless this is set
    
    CREATE TABLE food_nutrient (
    id                  INTEGER PRIMARY KEY,
    fdc_id              INTEGER NOT NULL,
    nutrient_id         INTEGER NOT NULL,
    amount              REAL,      -- per 100 g edible portion
    data_points         INTEGER,
    min                 REAL,
    max                 REAL,
    median              REAL,
    percent_daily_value REAL
    );

    CREATE INDEX idx_fn_fdc_nutrient ON food_nutrient (fdc_id, nutrient_id);
    CREATE INDEX idx_fn_nutrient ON food_nutrient (nutrient_id);

    
    CREATE TABLE food (
    fdc_id           INTEGER PRIMARY KEY,
    data_type        TEXT NOT NULL, 
    description      TEXT NOT NULL
    );

    CREATE INDEX idx_food_description ON food (data_type);
    CREATE INDEX idx_food_data_type ON food (data_type);

    CREATE TABLE recipes (
    recipe_id         INTEGER PRIMARY KEY,
    recipe_name       TEXT NOT NULL,
    cooking_time      TEXT,
    credit            TEXT,
    nutrients_summary TEXT NOT NULL DEFAULT '[]',
    instructions      TEXT NOT NULL DEFAULT '[]'
    );

    CREATE TABLE recipe_ingredients (
    recipe_id         INTEGER,
    ingredient        TEXT NOT NULL,
    quantity          TEXT NOT NULL,
    PRIMARY KEY (recipe_id, ingredient),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
    );
    """)

def getDBConnection(dbAddress : pathlib.Path):
    conn = sqlite3.connect(dbAddress)
    return conn

def deleteDatabase(dbAddress : pathlib.Path):
    os.remove(dbAddress.absolute())

dbAddress : pathlib.Path = pathlib.Path("Recipe-Ingredients.db")

