#!/usr/bin/python


import sys
import getopt
import os
import argparse
import pandas as pd
import numpy as np

def main():
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('input_tsv', help='input tsv')
    args = parser.parse_args()

    df = pd.read_csv(args.input_tsv, sep="\t")
    convert_data(df)

def parse_str_to_df(author_string):
    from io import StringIO

    TESTDATA = StringIO(author_string)
    df = pd.read_csv(TESTDATA, sep=None)

    return df

def clean_author_df(df):
    #Making sure the required columns actually appear
    if not "Institution" in df:
        df["Institution"] = df["Department/Division"]

    return df


def deduplicate_affiliations_authors_df(df):
    # Removing duplicates if there are multiple affiliations
    grouped_df = df.groupby(["Email"])
    df = grouped_df.first()
    df["Email"] = df.index

    return df
    
def create_author_list(authors_df):
    author_str = ""
    affiliation_str = ""

    grouped_institution_df = authors_df.groupby("Institution")
    grouped_institution_df = grouped_institution_df.first()
    grouped_institution_df["Institution"] = grouped_institution_df.index
    all_institutions = set(grouped_institution_df["Institution"].tolist())

    #print(all_institutions)
    # THIS kind of repeats work from NIH, so maybe we don't do that? 

    return author_str, affiliation_str

def convert_data_commands(authors_df):
    df = authors_df.replace(np.nan, '', regex=True)

    all_commands = []

    for i, author_dict in enumerate(df.to_dict(orient="records")):
        order_field = "contrib_auth_{}_author_seq".format(i+1)
        firstname_field = "contrib_auth_{}_first_nm".format(i+1)
        lastname_field = "contrib_auth_{}_last_nm".format(i+1)
        middlename_field = "contrib_auth_{}_middle_nm".format(i+1)
        email_field = "contrib_auth_{}_email".format(i+1)
        org_field = "contrib_auth_{}_org".format(i+1)
        city_field = "contrib_auth_{}_city".format(i+1)
        country_field = "contrib_auth_{}_country".format(i+1)
        title_field = "contrib_auth_{}_title".format(i+1)

        all_commands.append('document.getElementById("{}").value = "{}"'.format(order_field, author_dict["Order"]))
        all_commands.append('document.getElementById("{}").value = "{}"'.format(firstname_field, author_dict["First Name"]))
        all_commands.append('document.getElementById("{}").value = "{}"'.format(lastname_field, author_dict["Last Name"]))
        all_commands.append('document.getElementById("{}").value = "{}"'.format(middlename_field, author_dict["Middle Name(s)/Initial(s)"]))
        all_commands.append('document.getElementById("{}").value = "{}"'.format(email_field, author_dict["Email"]))
        all_commands.append('document.getElementById("{}").value = "{}"'.format(org_field, author_dict["Institution"]))
        all_commands.append('document.getElementById("{}").value = "{}"'.format(city_field, author_dict["City"]))
        all_commands.append('document.getElementById("{}").value = "{}"'.format(country_field, author_dict["Country"]))
        all_commands.append('document.getElementById("{}").value = "{}"'.format(title_field, author_dict["Title"]))
        
    return ";\n".join(all_commands)


if __name__ == "__main__":
    main()