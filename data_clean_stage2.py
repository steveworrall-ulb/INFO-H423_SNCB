import pandas as pd
import numpy as np


# Read data into pd DataFrame

df_merged = pd.read_csv(r"C:/Users/space/Desktop/ULB docs/---Data Mining/project/cleaned_stage1.csv", sep=';')
#df_merged = pd.read_csv(r"C:/Users/space/Desktop/ULB docs/---Data Mining/project/ar41_for_ulb_mini_test.csv", sep=';')
#df_merged = pd.read_csv(r"C:/Users/space/Desktop/ULB docs/---Data Mining/project/ar41_for_ulb.csv", sep=';')
#df_merged = pd.read_csv(r"C:/Users/space/Desktop/ULB docs/---Data Mining/project/ar41_for_ulb_expanded_mini_20231129.csv", sep=';')
#df_merged = pd.read_csv(r"C:/Users/space/Desktop/ULB docs/---Data Mining/project/merged_elevation_xy_weather_full_dataset_mini.csv", sep=';')

# Rename columns

"""ATTENTION  - SELECT THIS RENAME COMMAND CAREFULLY - it's needed after the batch process is complete to save correctly"""

df_merged = df_merged.rename(columns={"Unnamed: 0": "Row_number2"})
#df_merged = df_merged.rename(columns={"att1": "Row_number", "mapped_veh_id": "Mapped_veh_id"})

#remove duplicate ID
df_merged = df_merged.drop('Row_number2', axis=1)

def drop_columns_with_high_zero_percentage(group):
    print('processing 1/2 ' + str(index) + ' of ' + str(job_length))
    # Select numeric columns from the current group
    numeric_group_df = group[df_merged.select_dtypes(include=[np.number]).columns]
 
    # Calculate the number of zero values for each numeric column
    number_of_zero_values = (numeric_group_df == 0).sum(axis=0)
 
    # Calculate the percentage of zero values for each numeric column
    percentage_of_zero_values = number_of_zero_values / len(numeric_group_df)
 
    # Drop columns with more than 40% zeros
    for column, percentage in percentage_of_zero_values.items():
        if percentage > 0.4:
            print('clipped col Zero - ' + str(percentage) + ' - ' + str(column))
            group.drop(columns=[column], inplace=True)    
            
 
    return group

def drop_rows_with_high_missing_values(group, threshold=0.2):
    print('processing 2/2 ' + str(index) + ' of ' + str(job_length))
    result = False
    for column in group.columns:
        column_data = group[column]
        if (column_data.isna().mean() > threshold):
            result = True

    # Return True if there are exceeding columns, False otherwise
    if(result):
        print('clipped frame Nan')
        return pd.DataFrame([]) #empty data frame
    else:
        return group

df_merged['timestamp'] = pd.to_datetime(df_merged['timestamps_UTC'],format='%Y-%m-%d %H:%M:%S')

veh_list = list(df_merged.groupby(['Mapped_veh_id'])) #list of dataframes for each vehicle

#strip list touples [(id, df)] so it's only dataframes [df]
def striplist(list_in):
    index = 0
    for x in list_in:
        list_in[index] = x[1]
        index += 1
    return list_in

striplist(veh_list)

#split list by years
veh_year_list = []
for x in veh_list:
    year_list = striplist(list(x.groupby(x.timestamp.dt.year)))
    veh_year_list += year_list
    
#split list by months
veh_month_list = []
for x in veh_year_list:
    month_list = striplist(list(x.groupby(x.timestamp.dt.month)))
    veh_month_list += month_list

#split list by days
veh_day_list = []
for x in veh_month_list:
    day_list = striplist(list(x.groupby(x.timestamp.dt.day)))
    veh_day_list += day_list

#remove pandas format timestamp column
index = 0
for x in veh_day_list:
    veh_day_list[index] = veh_day_list[index].drop('timestamp', axis=1)
    index += 1

print('segmentation step complete - there are ' + str(len(veh_day_list)) + ' vehicle/day dataframes to process.')
job_length = len(veh_day_list)

#apply the Nan percentage rule function to the array of DFs 
index = 0
for x in veh_day_list:
    veh_day_list[index] = drop_rows_with_high_missing_values(x)
    index += 1

#recombine the segments into 1 data frame by virtical concatination 
output_df = pd.concat(veh_day_list, axis=0)

#sort the dataframe by Row_number
output_df = output_df.sort_values(by=['Row_number'])
print(output_df.head(100))

#output dataframe to a CSV file 
output_df.to_csv("C:/Users/space/Desktop/ULB docs/---Data Mining/project/cleaned_stage2.csv", sep = ';')
