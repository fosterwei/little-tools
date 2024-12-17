#keywords cluster & ranking excel
import pandas as pd

# Read the Excel file
df = pd.read_excel('处理后.xlsx')

# List of countries to process
countries = ['usa', 'can', 'gbr', 'deu']

# Create an Excel writer object
with pd.ExcelWriter('output.xlsx') as writer:
    for country in countries:
        # Filter data for the country
        df_country = df[df['Country'] == country]
        
        # List to hold DataFrames for each toy
        toy_dfs = []
        
        # Get unique toys in the country
        toys = df_country['name of toy'].unique()
        
        for toy in toys:
            # Filter data for the toy
            df_toy = df_country[df_country['name of toy'] == toy]
            
            # Get top 10 queries based on Impressions
            df_top = df_toy.nlargest(10, 'Impressions')
            
            # Append to the list
            toy_dfs.append(df_top)
        
        # Combine all toys' top queries
        if toy_dfs:
            df_result = pd.concat(toy_dfs)
            # Write to a sheet named after the country
            df_result.to_excel(writer, sheet_name=country, index=False)
