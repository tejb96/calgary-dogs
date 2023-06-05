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
    if (
        df.index.get_level_values("Breed")
        .str.contains(f"(?i)^{dog_breed}$", regex=True)
        .any()
    ):
        return dog_breed.upper()

    raise ValueError("Dog breed not found in the data. Please try again.")


def main():
    # Import data here

    df = pd.read_excel("CalgaryDogBreeds.xlsx")
    df = df.set_index(["Year", "Breed"])
    print(df)
    print("ENSF 592 Dogs of Calgary")

    # User input stage
    while True:
        dog_breed = input("Please enter a dog breed: ")
        try:
            dog_breed = dog_breed_check(dog_breed, df)
        except ValueError as value_err:
            print(str(value_err))

        # Data anaylsis stage

        # 1. Find and print all years where the selected breed was listed in the top breeds.
        df_breed = df.loc[(slice(None), dog_breed), :]
        top_breed_years = df_breed.index.get_level_values("Year").unique()
        print(
            f"The {dog_breed} was found in the top breeds for years:", *top_breed_years
        )

        #  2. Calculate and print the total number of registrations of the selected breed found in the dataset.
        total_breed = df_breed.Total.sum()
        print("There have been", total_breed, f"{dog_breed} dogs registered total.")

        # 3. Calculate and print the percentage of selected breed registrations out of the total percentage for each year (2021, 2022, 2023).
        idx = pd.IndexSlice
        for year in top_breed_years:
            total_yearly = df.loc[idx[year, :], "Total"].sum()
            total_breed_yearly = df_breed.loc[idx[year, :], "Total"].sum()
            percent_yearly = (total_breed_yearly / total_yearly) * 100
            print(
                f"The {dog_breed} was {round(percent_yearly, 6)}% of top breed in {year}."
            )
        # 4. Calculate and print the percentage of selected breed registrations out of the total three-year percentage.
        total_all_years = df.Total.sum()
        percent_all_years = (total_breed / total_all_years) * 100
        print(
            f"The {dog_breed} was {round(percent_all_years, 6)}% of top breeds across all years."
        )

        # 5. Find and print the months that were most popular for the selected breed registrations. Print all months that tie.
        total_monthly = df_breed.groupby("Month").Total.sum()
        mean = total_monthly.mean()
        mask = total_monthly[total_monthly > mean]
        print(mask)

        break


if __name__ == "__main__":
    main()
