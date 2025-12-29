import requests
import sys

BASE_URL = "http://127.0.0.1:5000/recipes"

def main():
    # נתוני מתכון לדוגמה
    example_recipe = {
        "name": "Test Recipe",
        "ingredients": ["ingredient1", "ingredient2"],
        "instructions": "Mix well."
    }

    try:
        # שליחת POST כדי להוסיף את המתכון
        res_post = requests.post(BASE_URL, json=example_recipe)
        if res_post.status_code != 201:
            print(f"POST failed with status {res_post.status_code}")
            sys.exit(1)

        # קבלת ה-ID של המתכון שנוצר
        recipe_id = res_post.json().get("id")
        if not recipe_id:
            print("No ID returned from POST")
            sys.exit(1)

        # מחיקת המתכון שנוצר
        res_delete = requests.delete(f"{BASE_URL}/{recipe_id}")
        if res_delete.status_code != 200:
            print(f"DELETE failed with status {res_delete.status_code}")
            sys.exit(1)

        # הכל עבר בהצלחה
        print("Test passed")
        sys.exit(0)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
