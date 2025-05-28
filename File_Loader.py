import ast
import csv

def load_transactions(filepath):
    transactions = []

    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)  # Read rows as dicts
            for row in reader:
                found = False
                for value in row.values():
                    if value is not None:
                        val = value.strip()
                        if val.startswith('[') and val.endswith(']'):
                            try:
                                parsed = ast.literal_eval(val)
                                if isinstance(parsed, list):
                                    transactions.append([item.strip() for item in parsed])
                                    found = True
                                    break
                            except:
                                pass
                if not found:
                    # Fallback: treat all non-empty, non-None values as transaction items
                    transaction = [item.strip() for item in row.values() if item and item.strip()]
                    transactions.append(transaction)

    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
    except Exception as e:
        print(f"Error: {e}")

    return transactions