import pandas as pd
from typing import Optional

class PointsFileLoader:
    def __init__(self, expected_columns: int = 2 or 3):
        self.expected_columns = expected_columns

    def load(self, file_path: str) -> Optional[pd.DataFrame]:
        try:
            df = pd.read_csv(file_path)

            # Check if the number of columns is valid (2 or 3)
            if len(df.columns) < 2:
                raise ValueError("Dataset must have at least two columns (x and y).")

            if len(df.columns) > 3:
                print("Warning: More than 3 columns found — only the first 3 will be used.")
                df = df.iloc[:, :3]  # Use only first 3 columns

            # Rename columns for consistency
            column_names = ['x', 'y', 'label'][:len(df.columns)]
            df.columns = column_names

            # Optionally: Validate that x and y are numeric
            df['x'] = pd.to_numeric(df['x'], errors='coerce')
            df['y'] = pd.to_numeric(df['y'], errors='coerce')

            # Drop rows with invalid x or y
            df = df.dropna(subset=['x', 'y'])

            return df

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except pd.errors.EmptyDataError:
            print("Error: File is empty.")
        except pd.errors.ParserError:
            print("Error: File format is invalid or not properly CSV.")
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        return None  # In case of any error

