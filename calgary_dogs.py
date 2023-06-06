# calgary_dogs.py
# AUTHOR NAME Tej
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 git repository.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc.
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.
import numpy as np
import pandas as pd


def dog_breed_check(dog_breed, df):
    """
    Check if the given dog breed is present in the DataFrame.

    Args:
        dog_breed (str): The dog breed to check.
        df (DataFrame): The DataFrame containing the dog breed data.

    Returns:
        str: The uppercase dog breed if found.

    Raises:
        ValueError: If the dog breed is not found in the data.
    """
    if df.Breed.str.contains(f"(?i)^{dog_breed}$", regex=True).any():
        return dog_breed.upper()

    raise ValueError("Dog breed not found in the data. Please try again.")


def main():
    # Import data here
    df = pd.read_excel("CalgaryDogBreeds.xlsx")
    df2 = df.set_index(["Year", "Breed"])  # Creating multi-index pandas dataframe
    print("ENSF 592 Dogs of Calgary")

    # User input stage
    while True:  # Loop that breaks with valid user input
        dog_breed = input("Please enter a dog breed: ")
        try:
            dog_breed = dog_breed_check(
                dog_breed, df
            )  # To check if user input is valid
            break
        except ValueError as value_err:  # Error message if it is not
            print(str(value_err))

    # Data anaylsis stage

    # 1. Find and print all years where the selected breed was listed in the top breeds.
    df_breed = df2.loc[
        (slice(None), dog_breed), :
    ]  # Creating dataframe that only contains data for the selected breed

    top_breed_years = df_breed.index.get_level_values("Year").unique()
    print(f"The {dog_breed} was found in the top breeds for years:", *top_breed_years)

    #  2. Calculate and print the total number of registrations of the selected breed found in the dataset.
    total_breed = df_breed.Total.sum()
    print("There have been", total_breed, f"{dog_breed} dogs registered total.")

    # 3. Calculate and print the percentage of selected breed registrations out of the total percentage for each year (2021, 2022, 2023).
    years = [2021, 2022, 2023]
    idx = pd.IndexSlice  # indexslice object
    for year in years:
        if (
            year in top_breed_years
        ):  # if the breed was found in the top breeds for that year
            total_yearly = df2.loc[
                idx[year, :], "Total"
            ].sum()  # using the indexslice object
            total_breed_yearly = df_breed.loc[
                idx[year, :], "Total"
            ].sum()  # calculate the percentage
            percent_yearly = (total_breed_yearly / total_yearly) * 100
            print(
                f"The {dog_breed} was {round(percent_yearly, 6)}% of top breed in {year}."  # and print it
            )

        else:
            print(
                f"The {dog_breed} was 0.0% of top breed in {year}."
            )  # otherwise print 0.0% for that year

    # 4. Calculate and print the percentage of selected breed registrations out of the total three-year percentage.
    total_all_years = df2.Total.sum()
    percent_all_years = (total_breed / total_all_years) * 100
    print(
        f"The {dog_breed} was {round(percent_all_years, 6)}% of top breeds across all years."
    )

    # 5. Find and print the months that were most popular for the selected breed registrations. Print all months that tie.
    total_monthly = df_breed.groupby("Month").count()
    maximum = total_monthly["Total"].max()
    mask = total_monthly["Total"] == maximum

    print(
        f"The most popular month(s) for {dog_breed} dogs:", *total_monthly.index[mask]
    )


if __name__ == "__main__":
    main()
