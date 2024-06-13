from packages.database import *

def AllFoods():
    allFoods = ReadDoc("cardapio.txt")

    canteen_data = {}

    for pk, columns, values in allFoods:
        if pk not in canteen_data:
            canteen_data[pk] = {}

        for collumn, value in zip(columns, values):
            canteen_data[pk][collumn] = value

    return canteen_data

def UpdateFood(id_food, new_data):
    updateFood = UpdateDoc("cardapio.txt", id_food, new_data)

    if updateFood:
        return True
    else:
        return False