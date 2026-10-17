import DBManager

conn = DBManager.getDBConnection(DBManager.dbAddress)
cursor = conn.cursor()

print("Ingredient testing:")
cursor.execute("SELECT COUNT(*) FROM food_nutrient WHERE food_nutrient.nutrient_id IS NOT NULL")
print(cursor.fetchall())
cursor.execute("SELECT COUNT(*) FROM food_nutrient WHERE food_nutrient.nutrient_id IS NULL")
print(cursor.fetchall())

cursor.execute("SELECT food.description, food_nutrient.nutrient_id FROM food INNER JOIN food_nutrient ON " \
"food.fdc_id = food_nutrient.fdc_id LIMIT 5")
for x in cursor.fetchall():
    print(x)
    
print()

cursor.execute("SELECT * FROM food LIMIT 2")
for x in cursor.fetchall():
    print(x)

print()

cursor.execute("SELECT * FROM food_nutrient LIMIT 2")
for x in cursor.fetchall():
    print(x)

cursor.execute("SELECT COUNT(*) FROM food JOIN food_nutrient ON food_nutrient.fdc_id = food.fdc_id")
for x in cursor.fetchall():
    print(x)

print()
print("Recipe testing:")

cursor.execute("SELECT COUNT(*) FROM recipes")
for x in cursor.fetchall():
    print(x)
cursor.execute("SELECT * FROM recipes LIMIT 2")
for x in cursor.fetchall():
    print(x)

cursor.execute("SELECT COUNT(*) FROM recipe_ingredients")
for x in cursor.fetchall():
    print(x)
cursor.execute("SELECT * FROM recipe_ingredients LIMIT 2")
for x in cursor.fetchall():
    print(x)

print()

cursor.execute("SELECT COUNT(*) FROM recipes INNER JOIN recipe_ingredients ON recipes.recipe_id = recipe_ingredients.recipe_id")
for x in cursor.fetchall():
    print(x)
cursor.execute("SELECT recipes.recipe_id, recipes.recipe_name, recipe_ingredients.ingredient, recipe_ingredients.quantity " \
"FROM recipes INNER JOIN recipe_ingredients ON recipes.recipe_id = recipe_ingredients.recipe_id LIMIT 2")
for x in cursor.fetchall():
    print(x)
    