import sys
sys.path.insert(0, "..")
import pandas as pd

def test():
    import parsing
    df = pd.read_csv("GNPS Dashboard Authors - Nature Biotech - Sheet1.tsv", sep=None)
    df = parsing.clean_authors_df(df)
    output = parsing.convert_data_commands(df)

    print(df)
    print(output)


if __name__ == "__main__":
    test()