import pathlib
import DBManager

import sqlite3
import json
    
def fillFoodNutrientData(csvPath : pathlib.Path = pathlib.Path("FoodData_Central_csv_2026-04-30\\food_nutrient.csv")):
    def insertRowIntoDB(row : list, cursor : sqlite3.Cursor):
        conn.execute("INSERT INTO food_nutrient VALUES (?,?,?,?,?,?,?,?,?);", row)

    #columns are 
    #"id","fdc_id","nutrient_id","amount","data_points","derivation_id","min","max","median","loq","footnote","min_year_acquired","percent_daily_value"
    #so indices wanted are:
    indices = [0,1,2,3,4,6,7,8,12]

    conn = DBManager.getDBConnection(DBManager.dbAddress)
    cursor = conn.cursor()

    cursor.execute("BEGIN")
    
    with open(csvPath.absolute()) as csvFile:
        rowsInserted = 0
        for lineNum, line in enumerate(csvFile):
            if lineNum == 0: #skip first line as just has column names
                continue
            if lineNum % 1000000 == 0:
                print("RowNum looked at in food_nutrient.csv: ",lineNum)
            toInsert = []
            line = line.strip("\n ")
            splitLine = line.split('","')
            splitLine[0] = splitLine[0][1:] 
            splitLine[-1] = splitLine[-1][:-2]
            for index in indices:
                if splitLine[index] == '':
                    toInsert.append(None)
                    continue
                if index in (0,1,2,4):
                    toInsert.append(int(splitLine[index]))
                elif index in(3,6,7,8,12):
                    toInsert.append(float(splitLine[index]))
                else:
                    print("Uncovered index in fillFoodNutrientData()")
            
            insertRowIntoDB(toInsert, cursor)
            rowsInserted +=1

    print(f"Done loading food_nutrient data into the database - rows inserted/looked at: {rowsInserted}/{lineNum}") #type:ignore

    cursor.execute("COMMIT")

def fillFoodData(csvPath : pathlib.Path = pathlib.Path("FoodData_Central_csv_2026-04-30\\food.csv")):
    def insertRowIntoDB(row : list, cursor : sqlite3.Cursor):
        conn.execute("INSERT INTO food VALUES (?,?,?);", row)

    #columns are 
    #"fdc_id","data_type","description","food_category_id"
    #so indices wanted are:
    indices = [0,1,2]

    conn = DBManager.getDBConnection(DBManager.dbAddress)
    cursor = conn.cursor()

    cursor.execute("BEGIN")
    
    
    with open(csvPath.absolute(), encoding="UTF-8") as csvFile:
        dataTypes = set()
        for lineNum, line in enumerate(csvFile):
            if lineNum == 0: #skip first line as just has column names
                continue
            if lineNum % 1000000 == 0:
                print("RowNum imported from food_nutrient.csv: ",lineNum)
            
            toInsert = []
            line = line.strip("\n ")
            splitLine = line.split('","')
            splitLine[0] = splitLine[0][1:] 
            splitLine[-1] = splitLine[-1][:-2]

            if splitLine[1] != "survey_fndds_food":    
                continue
            print(splitLine)
            for index in indices:
                if splitLine[index] == '':
                    toInsert.append(None)
                    continue
                if index == 0:
                    toInsert.append(int(splitLine[index]))
                elif index in (1,2):
                    toInsert.append(str(splitLine[index]))
                else:
                    print("Uncovered index in fillFoodNutrientData()")
            
            insertRowIntoDB(toInsert, cursor)

        cursor.execute("COMMIT")
        print("Done loading food_nutrient data into the database")
    
        

def fillRecipeData(jsonPath : pathlib.Path = pathlib.Path("SyntheticRecipeData.json")):
    #Please note that whilst claude was used to generate this data for testing purposes, 
    # all code written by me (Miles Halfpenny) was written by hand

    conn = DBManager.getDBConnection(DBManager.dbAddress)
    cursor = conn.cursor()

    cursor.execute("BEGIN")

    with open(jsonPath.absolute()) as jsonFile:
        for recipe in json.load(jsonFile):
            name = recipe["recipe-name"] 
            cookingTime = recipe["cooking-time"] 
            credit = recipe["credit"] 
            nutrientsSummary = recipe["nutrients-summary"] 
            instructions = recipe["instructions"]

            cursor.execute("INSERT INTO recipes(recipe_name,cooking_time,credit,nutrients_summary,instructions) VALUES (?,?,?,?,?)", 
                           (name,cookingTime,credit,str(nutrientsSummary),str(instructions)))

            curMaxID = cursor.execute("SELECT MAX(recipe_id) FROM recipes").fetchone()[0]

            for ingredientJson in recipe["ingredients"]: 
                ingredient = ingredientJson["ingredient"] 
                quantity = ingredientJson["quantity"] 

                cursor.execute("INSERT INTO recipe_ingredients VALUES (?,?,?)", 
                               (curMaxID,ingredient,quantity))
    cursor.execute("COMMIT")
    print("Recipe data successfully filled")
