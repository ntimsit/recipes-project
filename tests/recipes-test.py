import requests
import sys
import os

# BASE_URL כללי (לוקאלי: nginx, CI: Flask ישיר)
BASE_URL = os.getenv("BASE_URL", "http://localhost")

RECIPES_ENDPOINT = f"{BASE_URL}/recipes"

def main():
    example_recipe = {
        "name": "Test Recipe",
        "ingredients": ["ingredient1", "ingredient2"],
        "instructions": "Mix well."
    }

    try:
        # POST – הוספת מתכון
        res_post = requests.post(RECIPES_ENDPOINT, json=example_recipe)
        if res_post.status_code != 201:
            print(f"POST failed with status {res_post.status_code}")
            sys.exit(1)

        recipe_id = res_post.json().get("id")
        if not recipe_id:
            print("No ID returned from POST")
            sys.exit(1)

        # DELETE – מחיקת המתכון
        res_delete = requests.delete(f"{RECIPES_ENDPOINT}/{recipe_id}")
        if res_delete.status_code != 200:
            print(f"DELETE failed with status {res_delete.status_code}")
            sys.exit(1)

        print("Test passed")
        sys.exit(0)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

