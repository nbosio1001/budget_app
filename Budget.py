# Editing Budget.xlsx Project using openpyxl
# Use https://openpyxl.readthedocs.io/en/stable/tutorial.html#loading-from-a-file
# for tutorial

#This is the original Budget File, Placed as a textfile.

import os
import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy # Create SQL Database with my standard format
from expenses_dict import expenses_dict
import datetime # Allows Python to call dates as datetime objects



# Importing multiple files from same folder
path=r'C:\Users\Nick Bosio\Documents\Python\Budget_App\Transactions\\'
dirs = os.listdir(path)


#df_list=[]

#phone_reg='[\d\d\d\d][/or-][/d/d][/or-][\d\d\d\d]'
date_regex='\d{1,2}\/\d{1,2}\/\d{4}$' # $:end of line
# This would print all the files and directories
df_list=[]
location_list=[]
card_dfs=[]
#date_as_first_row=[]
date=[]
date_test=[]

for file in dirs:
    #print(file)
    file_name=path+file
    #print(file_name)
    df=pd.read_csv(file_name,header=None)
    df=df.dropna(axis='columns',how='all') # Drops columns that contain all nan values
    #df=df.sort([0])
    
    # =============================================================================
    try:
        df['Date'] = pd.to_datetime(df[0])#,infer_datetime_format=True)
        df=df.sort_values(['Date'])
    except ValueError:
        location=df.apply(lambda row: row.astype(str).str.contains(date_regex).any(), axis=1) # Outputs boolean series where the location of Year Ended is true
        df=df.loc[location]
    # =============================================================================
    
    card_dfs.append(df.reset_index(drop=True))



investor_card_df=card_dfs[1].filter([0,2,7]).rename(columns={0:'Date',2:'Description',7:'Amount'})
investor_card_df.Amount=investor_card_df.Amount.astype(float)
blue_card_df=card_dfs[0].filter([0,3,2]).rename(columns={0:'Date',3:'Description',2:'Amount'})
blue_card_df.Amount=blue_card_df.Amount.astype(float)

schwab_bank=card_dfs[2]
schwab_bank[4]=schwab_bank[4].str.split('$').str[1]
schwab_bank[4] = schwab_bank[4].replace(',', '',regex=True).astype(float)
schwab_bank[4]*=-1

schwab_bank[5]=schwab_bank[5].str.split('$').str[1]
schwab_bank[5] = schwab_bank[5].replace(',', '',regex=True).astype(float)

schwab_bank[4]=schwab_bank[4].fillna(schwab_bank[5])
schwab_bank=schwab_bank.filter([0,3,4]).rename(columns={0:'Date',3:'Description',4:'Amount'})

#schwab_bank=card_dfs[2].filter([0,3,2]).rename(columns={0:'Date',3:'Description',2:'Amount'})

vertical_stack = pd.merge(investor_card_df, blue_card_df, on=['Date','Description','Amount'],how='outer')
vertical_stack=pd.merge(vertical_stack,schwab_bank, on=['Date','Description','Amount'],how='outer')
vertical_stack.Amount=vertical_stack.Amount.astype(float)
vertical_stack.Date = pd.to_datetime(vertical_stack['Date'])#,infer_datetime_format=True)
vertical_stack=vertical_stack.sort_values(['Date'])
#vertical_stack=vertical_stack.sort_values(by=['Date']
#print(type(vertical_stack.Amount))

def My_attempt_at_formatting_csv_files_based_on_conditions(df):
    # Code at bottom
    pass # may use this: print("First Module's Name: {}".format(__name__))

    
def dataframe_creation():
    df=pd.read_excel(excelfilepath,sheet_name='June 2019') # Reads Excel and imports into dataframe
    
    df.columns=df.iloc[0,:] # Uses the first index as the column title
    df.drop(df.index[0], inplace=True) # Drops the first row, there is still an issue with the index not resetting (ie Index starts at 1 instead of 0)
    df.Amount=pd.to_numeric(df.Amount) # Changes Amount column from an object to a float64
    
    amount=df['Amount'] # Creates a individual dataframe from 'Amount' Column
    description=df['Description'] # Creates a individual dataframe from 'Description' Column

def sql_formatting():
    year=input("Input cell containing year: ")
    sql="('"+year+"-"+month+"-"+day+"','"+description+"','"+amount+"'),"
 
    


# Regex ^ [caret] and $ [dollar] symbol represent start and end of a line of text respectivaely
# Word-based version are \< and \>
 
expenses_dict=expenses_dict()

#def Big_function(vertical_stack,expenses_dict): 
keys=expenses_dict.keys() # Gets the keys from the expenses dictionary
#print(keys)
values=expenses_dict.values() # Gets values from expenses dictionary

keys=list(keys) # Cleans up keys and places in list
values=list(values) # Cleans up values and places in list

amount=vertical_stack['Amount'] # Creates a individual dataframe from 'Amount' Column

description=vertical_stack['Description'] # Creates a individual dataframe from 'Description' Column
 
charge_amount=[]
other_amount=[]
 
joined_string=['|'.join(value) for value in values] #List Input, Outputs string with | between strings

descript_bool_check=[]
category_amount_check=[]
value_check=[]
 
for value in joined_string:
    value_check.append(value)
    descript_bool=description.str.contains(value,na=False,case=False)
    #descript_bool=description.str.contains('\b'+value or value+',' or ', '+value,na=False,case=False)
    #print(type(descript_bool))
    descript_bool_check.append(descript_bool)
    category_amount=vertical_stack.loc[descript_bool,'Amount'].sum()
    category_amount_check.append(vertical_stack.loc[descript_bool,'Amount'].sum())
    clean_output=float(abs(round(category_amount,2)))
    charge_amount.append(clean_output) #Escape code is used: \b
    # pandas.Series.str.contains
    # Series is a one-dimensional labeled array capable of holding any data type (integers, strings,)    
    other_amount=abs(round(vertical_stack.loc[~description.str.contains('\b'+value or value+',' or ', '+value or ' '+value+' ',na=False,case=False),
                                  'Amount'].sum(),2))
 #print(list(charge_amount))
 #print(list(expenses_dict.keys()))
cool=dict(zip(list(expenses_dict.keys()),charge_amount))

labels=cool.keys()
expense_chart_sizes=[list(cool.values())]
fig2,ax2=plt.subplots()
ax2.pie(expense_chart_sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax2.axis('equal')
plt.legend()

cool['Other Amount']=other_amount

#total=0
#total+=cool.values()

#print(cool.dtypes)


#matplotlib=Big_function(vertical_stack,expenses_dict)  
     
#    ''' Looks at the dataframe with the column title 'Description'. \b is a escape code. There may be a problem with using escape codes (\b). But if I remove the escape\
#    code, then there is a problem with example gas being in vegas.'''
#     
#     #Plotting data in chart
#     #https://matplotlib.org/gallery/pie_and_polar_charts/pie_features.html#sphx-glr-gallery-pie-and-polar-charts-pie-features-py


def matplotlib(cool):     
#    plt.figure(figsize=(6,6))
#    ax = plt.axes([0.1, 0.1, 0.8, 0.8])
    
    labels=cool.keys()
    expense_chart_sizes=[list(cool.values())] #Size of pie chart section, Probably frace
    #colors=['#ff9999','#66b3ff','#99ff99','#ffcc99']

   
    fig1,ax1=plt.subplots()
    ax1.pie(expense_chart_sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.legend()
    
    return plt.show()

    
    
     #return plt.show()
     
     #plt.pie(cool.values(),labels=cool.keys())
     #plt.axis('equal')
     #plt.show()
#     
#     
#matplotlib(matplotlib)  
# =============================================    
#plt.figure(figsize=(6,6))
#ax = plt.axes([0.1, 0.1, 0.8, 0.8])
#
#labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
#fracs = [15,30,45, 10]
#
#explode=(0, 0.05, 0, 0)
#p = plt.pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
#plt.title('Raining Hogs and Dogs', bbox={'facecolor':'0.8', 'pad':5})
#
#w = p[0][0]
#plt.show() 
#
#class PieEventHandler:
#    def __init__(self,p):
#        self.p = p
#        self.fig = p[0].figure
#        self.ax = p[0].axes
#        self.fig.canvas.mpl_connect('button_press_event', self.onpress)
#
#    def onpress(self, event):
#        if event.inaxes!=self.ax:
#            return
#
#        for w in self.p:
#            (hit,_) = w.contains(event)
#            if hit:
#                print w.get_label()
#
#
#handler = PieEventHandler(p[0])  
# =============================================================================
#     
#     
#     
#     
#     
#     
#     
#     
#     
#def My_attempt_at_formatting_csv_files_based_on_conditions(df):
#    df_list.append(df) # Shows me all the CSV files as variables
#
#    # =============================================================================
#    location=df.apply(lambda col: col.astype(str).str.contains(date_regex).any(), axis=1)
#    # df.apply(applies function, to row(axis=0) or column (axis=1) assigned)
#    # Lambda function is a nameless function that requires an argument followed by a colon
#    # Probably it is a ndarray, an N-dimensional array type which describes a collection of “items” of the same type
#    # =============================================================================
#    #location_list.append(location)
#    dates_as_first_row=df[location] # Drops the dataframe to the first date value, KEEP!!!!
#    
#    # =============================================================================
#    # THIS SECTION BELOW IS FOR GETTING ONLY THE DATE, DESCRIPTION, AND AMOUNT DATAFRAMES
#    date_column=dates_as_first_row.filter(regex=date_regex,axis='columns')
#    for date in dates_as_first_row:
#        cool=dates_as_first_row[date]
#   #     boolean_series=cool.str.contains(date_regex)
#        a=boolean_series.index[boolean_series]
#        interesting=pd.DataFrame(date)
#        print(type(WOAH))
#    print(type(date_as_first_row))
#    # =============================================================================
#    
#    date.append(date_as_first_row[date_as_first_row.Type==attempt])
#    clean_df=date_as_first_row.drop([1],axis=1)
#    
#    clean_df=clean_df.rename(columns={0:'Date',2:'Description',7:'Amount'})
#    
#    clean_df.to_csv(r'C:\Users\Nick Bosio\Desktop\Testing.csv')
#    
#    
#    
#    for series in df:
#        print(type(series))
#        location=df.apply(lambda row: row.astype(str).str.contains('Year Ended' or 'December 31,').any(), axis=1)
#    #        descript_bool=series.str.contains(attempt,na=False,case=False)
#    df_list.append(df)
#    print(type(df_list[3].iloc[2].Datetime))
#    
#    df=pd.read_csv(file)
#    
#     #Import CSV file into Python Pandas, manipulate data, push into a new csv file
#    
#    excelfilepath=r'C:\Users\Nick Bosio\Documents\Budget\Budget.xlsx' #Store this info in the cloud.