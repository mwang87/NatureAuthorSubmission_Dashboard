import sys
sys.path.insert(0, "..")
import pandas as pd

def test():
    import parsing
    df = pd.read_csv("GNPS Dashboard Authors - Nature Biotech - Sheet1.tsv", sep=None)
    df = parsing.clean_author_df(df)
    df = parsing.deduplicate_affiliations_authors_df(df)
    output = parsing.convert_data_commands(df)
    authors_str, affiliation_str = parsing.create_author_list(df)

    print(authors_str, affiliation_str)

    #print(df)
    #print(output)


if __name__ == "__main__":
    test()