import time
import DBManager
import DataFetching

DBManager.deleteDatabase(DBManager.dbAddress)
DBManager.createDB(DBManager.dbAddress)
start = time.time()
#Note that these use genuine USDA nutrition data, but for time saving purposes example nutrition summary values are used
# Therefore, whilst these are tested and function, they are not integrated into the current program
#DataFetching.fillFoodNutrientData()
#DataFetching.fillFoodData()
DataFetching.fillRecipeData()

end = time.time()
print("Time taken to fill database: ",end-start)