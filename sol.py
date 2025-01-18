import pandas as pd
import numpy as np


def string_to_table(data):
    # get the cols
    cols= data.split('\n')[0].split(';')
    # get the rows
    rows = data.split('\n')[1:-1]
    for i in range(len(rows)):
        rows[i] = rows[i].split(';')
    # return the raw data frame
    return pd.DataFrame(columns= cols, 
                        data = rows)




def fix_airline_code(df):
    # Fix the  Airline Code using regex


    # First we remove everything before the first Capital letter
    df['Airline Code'] = df['Airline Code'].str.extract(r'[^A-Z]*([A-Z].*)')


    # We retain everything to the last lowercase letter
    df['Airline Code'] = df['Airline Code'].str.extract(r'(.*[a-z]).*')


    # Assumption: We assume that the airline code
    # sits nicely within the first capital letter and
    # last lower case letter
    return df






def fix_to_from(df):


    # use regex to extract the From column and To column
    df['From'] = df['To_From'].str.extract(r'.*[_](.*)')
    df['From'] = df['From'].str.upper()
    df = df.rename(columns = {'To_From':'To'})


    df['To'] = df['To'].str.extract(r'(.*)[_].*')
    df['To'] = df['To'].str.upper()
    return df




def fix_flight_codes(df):
    df['FlightCodes']=df['FlightCodes'].replace('',0).astype(float).astype(int)


    # get the index of the first non-zero element in the column FlightCodes
    id_non_zero = df[df.FlightCodes > 0].index[0]
    # get the code value for the first non-zero element
    code = df[df.FlightCodes > 0].iloc[0]['FlightCodes']


    # We use this code value to build the rest of the table
    # First we create a list of values that need updating
    updated_values = []
    for row in df.itertuples():
        idx = row[0]
        if idx == id_non_zero:
            continue
        if row.FlightCodes != 0:
            continue
        diff = (idx - id_non_zero)*10
        updated_values.append([idx, code + diff])


    # Now we can update the values, using the id's
    # and first non-zero code value, we can fill in the 
    # missing code values 
    col_id = df.columns.get_loc('FlightCodes')
    for idx, value in updated_values:
        df.iloc[idx,col_id] = value
    
    return df




def table_to_string(df):
    # use the join function to rebuilt the string 
    # representation of the table
    rows_str = []


    rows_str.append(';'.join(df.columns.to_list()))


    for idx, row in df.iterrows():
        row = row.astype(str)
        rows_str.append(';'.join(row.to_list()))


    res = '\\n'.join(rows_str)


    return res


# Import the data
data =  'Airline Code;DelayTimes;FlightCodes;To_From\nAir Canada (!);[21, 40];20015.0;WAterLoo_NEWYork\n<Air France> (12);[];;Montreal_TORONTO\n(Porter Airways. );[60, 22, 87];20035.0;CALgary_Ottawa\n12. Air France;[78, 66];;Ottawa_VANcouvER\n""".\\.Lufthansa.\\.""";[12, 33];20055.0;london_MONTreal\n'






df = string_to_table(data)




# Fix the  Airline Code
df = fix_airline_code(df)


df = fix_to_from(df)


df = fix_flight_codes(df)


print(f'Data Frame:\n{df}\n')


print(f'String Representation:\n{table_to_string(df)}')
