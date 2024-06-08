"""
    calgary_dogs.py
    AUTHOR: David Pozniak

    A terminal-based application for computing and printing statistics based on given input.
    Detailed specifications are provided via the Assignment 4 README file.
"""

import pandas as pd
import numpy as np

def main():

    # Import data here
    
    # Importing excel file with pandas read_excel function.
    dog_breed_data = pd.read_excel(r".\\CalgaryDogBreeds.xlsx")

    # Grabbing the headers names to be referenced when selecting data.
    headers = dog_breed_data.columns.values

    # Building and applying MultiIndex (hierarchical index), in order of breed, year, month.
    index = pd.MultiIndex.from_arrays([dog_breed_data[headers[2]], dog_breed_data[headers[0]], dog_breed_data[headers[1]]], names = [headers[2], headers[0], headers[1]])
    dog_breed_indexed = pd.DataFrame(np.array(dog_breed_data[headers[3]]), index=index, columns = [headers[3]])

    print("ENSF 692 Dogs of Calgary")

    # User input stage
    
    # I commented out the next line, but used it when testing the python script, and think it should stay so the user knows what input is valid
    # print("\nValid breed names:\n" + ", ".join(dog_breed_data[headers[2]].unique()))

    # This while loop grabs user input and validate it against all the unique dog breeds, otherwise yields a KeyError prompting for valid user input.
    while True:
        user_input = input("Please enter a dog breed:").upper().strip()
        
        if user_input in dog_breed_data[headers[2]].unique(): break
            
        try:
            raise KeyError
        except KeyError:
            print("Dog breed not found in the data. Please try again.")
        
    # Data anaylsis 

    # Printing the years in the specified formate required building a string joining all of the unique years that appear in the user selected breed dataset. 
    dog_years = dog_breed_indexed.loc[user_input,:].index.unique(0).values
    selected_years_dog = ""
    for year in dog_years:
        selected_years_dog += " " + str(year)
    print("The " + user_input + " was found in the top breeds for years: " + selected_years_dog)
    
    # Printing out the total number of registered dogs of the selected breed.
    print("There have been " + str(np.nansum(dog_breed_indexed.loc[user_input,:])) + " " + user_input + " dogs registered total.")

    # IndexSlice is not necessary and makes the code more complex, it is added due to Assignment 4 specifications to demonstrate understanding of IndexSlice.
    idx = pd.IndexSlice
    
    # Calculating the yearly totals to be used to calculate % of selected dog breed registrations vs dog registrations.
    yearly_totals = dog_breed_indexed.groupby(level=headers[0]).sum()
    selected_yearly_totals = dog_breed_indexed.loc[idx[user_input,:],idx[headers[3]]].groupby(level=headers[0]).sum()
    
    # Calculating the totals to be used to calculate % of selected totals dog breed registrations vs total dog registrations.
    total_reg = dog_breed_indexed.sum()
    selected_total_reg = dog_breed_indexed.loc[idx[user_input,:],idx[headers[3]]].sum()
    
    # Printing out the yearly %'s of selected yearly dog breed registrations vs yearly dog registrations.
    for year in dog_years:
        print("The {} was {:.06f}% of the top breeds in {}.".format(user_input, float((selected_yearly_totals.loc[year].sum()/yearly_totals.loc[year].sum())*100), str(year)))
    
    # Printing out the total % of selected total dog breed registrations vs total dog registrations.
    print("The {} was {:.06f}% of the top breeds across all years.".format(user_input, float((selected_total_reg/total_reg).iloc[0]*100)))

    # Calculating which months of the selected dog breed appear most in the data set to represent the "most popular months" for selected dog breed registrations.
    selected_num_months = dog_breed_indexed.loc[user_input,:].groupby(level=headers[1]).count()
    print("Most popular month(s) for " + user_input + " dogs:  " + " ".join(selected_num_months[selected_num_months.values == np.nanmax(selected_num_months)].index.values))
    
if __name__ == '__main__':
    main()