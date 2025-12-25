from core.database import get_database

def clear_all_data():
    db = get_database()

    # Clear all collections
    collections = ['users', 'students', 'faculty', 'attendance', 'results', 'leaves', 'holidays', 'events']

    for collection_name in collections:
        try:
            result = db[collection_name].delete_many({})
            print(f"Cleared {result.deleted_count} documents from {collection_name}")
        except Exception as e:
            print(f"Error clearing {collection_name}: {e}")

if __name__ == "__main__":
    clear_all_data()
    print("Database cleared successfully!")
