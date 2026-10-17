import pandas as pd
import pathlib
import DBManager
import time
import sqlite3
    
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
        for lineNum, line in enumerate(csvFile):
            if lineNum == 0: #skip first line as just has column names
                continue
            if lineNum % 1000000 == 0:
                print("RowNum imported from food_nutrient.csv: ",lineNum)
            toInsert = []
            line = line.strip("\n ")
            splitLine = line.split('","')
            splitLine[0] = splitLine[0][1:] 
            splitLine[12] = splitLine[12][:-2]
            if splitLine[4] == '' or splitLine[4] == "0": #so if no actual data to be stored
                continue
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

    print("Done loading food_nutrient data into the database")

    cursor.execute("COMMIT")

def fillFoodData(csvPath : pathlib.Path = pathlib.Path("FoodData_Central_csv_2026-04-30\\food.csv")):
    df = pd.read_csv(csvPath.absolute(), 
                     low_memory=False)
    print(df.columns)
    quit()
    conn = DBManager.getDBConnection(DBManager.dbAddress)
    print(df.loc[0])
    print(df.loc[1])
    print(df.loc[2])
    quit()
    for row in df.rows:
        print(row)
        quit()
        conn.execute("INSERT INTO food_nutrient VALUES (?,?,?,?,?,?,?,?,?);", row)
#fillFoodData()

DBManager.deleteDatabase(DBManager.dbAddress)
start = time.time()
DBManager.createDB(DBManager.dbAddress)
end = time.time()
print(end-start)
fillFoodNutrientData()