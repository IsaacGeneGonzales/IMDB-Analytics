import pandas as pd
import os
from raw_metadata import IMDB_DATA_PATH, imdb_files, dtypes

def load_imdb_data(table_name):
    """Load a specific IMDb TSV file into a pandas DataFrame with proper typecasting."""
    if table_name not in imdb_files:
        raise ValueError(f"Table '{table_name}' not found in imdb_files. Available tables: {list(imdb_files.keys())}")

    file_path = os.path.join(IMDB_DATA_PATH, imdb_files[table_name])

    try:
        # Load all columns as string first to avoid parsing issues
        df = pd.read_csv(
            file_path,
            sep='\t',
            encoding='utf-8',
            na_values='\\N',  # IMDb uses \N for null values
            dtype="object",  # Load everything as string initially
            low_memory=False
        )

        # Apply actual dtypes from metadata
        for col, dtype in dtypes.get(table_name, {}).items():
            if dtype == "Int64":
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")  # Convert to nullable int
            elif dtype == "float64":
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")  # Convert to float
            elif dtype == "boolean":
                df[col] = df[col].map({"1": True, "0": False}).astype("boolean")  # Convert to boolean
            else:
                df[col] = df[col].astype("string")  # Ensure non-numeric fields remain strings

        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    
    except pd.errors.ParserError:
        raise ValueError(f"Parsing error encountered in file: {file_path}")
    
    except Exception as e:
        raise RuntimeError(f"Failed to load '{table_name}': {e}")
