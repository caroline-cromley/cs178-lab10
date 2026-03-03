# name: Caroline Cromley
# date: 3-5-2026

from urllib import response

import boto3

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Recipe_Book')

def create_recipe():
    recipe = input("What is the recipe title? ")
    table.put_item(
        Item={
            "Recipe": recipe,
            "Servings": []
        }
    )
    print("creating a recipe")

def print_recipe(recipe_book):
    recipe = recipe_book.get("Recipe", "Unknown Recipe")
    servings = recipe_book.get("Servings", "Unknown Servings")

    print(f"  Recipe  : {recipe}")
    print(f"  Servings   : {servings}")
    print()

def print_all_recipes():
    """Scan the entire Recipe_Book table and print each item."""    
    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No recipes found")
        return
    
    for recipe in items:
        print_recipe(recipe)

def update_servings():
    try:
        recipe = input("What is the recipe name? ")
        servings = int(input("What is the number of servings: "))
        table.update_item(
            Key={"Recipe": recipe},
            UpdateExpression="SET Servings = :s",
            ExpressionAttributeValues={':s': servings}
    )
    except Exception as e:
        print("error in updating recipe servings")

def delete_recipe():
    recipe = input("What is the recipe name? ")
    table.delete_item(
        Key={"Recipe": recipe}
    )
    print("deleting recipe")

def query_recipe():
    """
    Prompt user for a Recipe Title.
    Print out the servings in the recipe.
    """
    recipe = input("What is the recipe name? ")
    response = table.get_item(Key={"Recipe": recipe})
    recipe = response.get("Item")
    if recipe is None:
        print("recipe not found")
        return
    servings = recipe["Servings"]
    if servings is None:
        print("recipe has no listed servings")
        return
    print(servings)

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new recipe")
    print("Press R: to READ all recipes")
    print("Press U: to UPDATE the servings for a recipe")
    print("Press D: to DELETE a recipe")
    print("Press Q: to QUERY a recipe's average servings")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_recipe()
        elif input_char.upper() == "R":
            print_all_recipes()
        elif input_char.upper() == "U":
            update_servings()
        elif input_char.upper() == "D":
            delete_recipe()
        elif input_char.upper() == "Q":
            query_recipe()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()