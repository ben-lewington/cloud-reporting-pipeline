import polars as pd
import interview as iv


def load_data():
    return pd.read_csv('resources/railway_data_dictionary.csv') \
        , pd.read_csv('resources/railway.csv')


if __name__ == "__main__":
    railway_dd, railway = load_data()
    print(railway_dd)
    print(railway)
    print(iv.FOO)
