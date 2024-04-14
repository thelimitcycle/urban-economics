import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#start by looking at the regional GDP data
cagdp2 = pd.read_csv('CAGDP2-MSA.csv', skiprows=3)

save_data = False #save the crunched data to a .csv file

gdp_linecodes = [3.0,6.0,10.0,11.0,12.0,34.0,35.0,36.0,45.0,51.0,56.0,60.0,64.0,65.0,69.0,70.0,76.0,79.0,82.0,83.0] #line codes that I declare relevant
relevant_rows = cagdp2.loc[cagdp2['LineCode'].isin(gdp_linecodes)]
#set the gdp values to integers
relevant_rows['2022'] = pd.to_numeric(relevant_rows['2022'],errors ='coerce').fillna(0).astype('int')
#create two new columns
relevant_rows['percentage_of_msa_gdp'] = 0.0
relevant_rows['ratio_to_USA'] = 0.0
relevant_rows['big_economy'] = False
GeoFips = relevant_rows['GeoFips'].unique().tolist() #get the FIPS codes
fip2name = dict(zip(GeoFips, [0] * len(GeoFips)))

gdp_totals = dict(zip(GeoFips, [0] * len(GeoFips)))

top_25_fips = ['35620', '31080', '41860', '16980', '19100', '42660', '14460', '33100', '12060', '47900', '26420', '38060', '19820', '37980', '41740', '41940', '33460', '40140', '12420', '45300', '12580', '19740', '36740', '16740']
#calculate the percentage contribution of GDP for each industry for each city and compare it to the US as a whole
for gf in GeoFips:
    msa_gdp = relevant_rows.loc[relevant_rows['GeoFips']==gf]['2022'].sum()
    msa_name = relevant_rows.loc[relevant_rows['GeoFips']==gf]['GeoName'].unique()[0]
    fip2name[gf] = msa_name
    gdp_totals[gf] = msa_gdp

    #ok so this it the money line, it pulls out the rows that have the correct GeoFips ID and then sets the column 'percentage_of_msa_gdp' to the calculation
    relevant_rows.loc[relevant_rows['GeoFips']== gf, 'percentage_of_msa_gdp'] = relevant_rows.loc[relevant_rows['GeoFips']== gf]['2022'].div(msa_gdp)
    #GooFips are stored as strings which is good, but important to remember. don't filter with an integer value!!
    #Also it works better if you convert to numpy arrays before doing the division. not sure why....
    relevant_rows.loc[relevant_rows['GeoFips']== gf, 'ratio_to_USA'] = (relevant_rows.loc[relevant_rows['GeoFips']== gf]['percentage_of_msa_gdp'].to_numpy())/(relevant_rows.loc[relevant_rows['GeoFips']== '00998']['percentage_of_msa_gdp'].to_numpy())
    relevant_rows.loc[relevant_rows['GeoFips']== gf, 'big_economy'] = gf in top_25_fips
    
if save_data == True:
    relevant_rows.to_csv('cagdp2-crunched2.csv') #export the calculations to a .csv file

#create a histogram of the GDPs
gdp_sorted = sorted(gdp_totals.items(), key=lambda x: x[1], reverse=True)
gdp_totals.pop('00998')
relevant_gdps = gdp_totals.values()
top_25 = gdp_sorted[1:25]
#show the GDPs in a stem plot
plt.figure()
plt.stem(sorted(relevant_gdps,reverse=True))
plt.yscale('log')
plt.show()


#calculate the breakdown of economy sizes
#should make a dictionary that maps geofips to a human-readable city name
#calculate the linecode correlation for the big economies

big_economies = relevant_rows.loc[relevant_rows['big_economy']==True]
indices = big_economies.groupby('GeoFips')['ratio_to_USA'].idxmax()
top_industries = big_economies.loc[indices]
if save_data == True:
    top_industries.to_csv('CAGDP2_top_industries.csv')
#i'll need to set up a correlation matrix. 

#ok time to play with the data. I have the
#I have the breakdowns for every industry for every city and the ratios of that to the US as as whole. Lets see who wins....
#set up the a correlation matrix to see which are correlated to one another
pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
"""
industries = relevant_rows['Description'].unique()
print(industries)

nerds = relevant_rows.loc[relevant_rows['Description'] == '      Accommodation and food services']
print(nerds.sort_values(by='ratio_to_USA',ascending=False))

triange = relevant_rows.loc[relevant_rows['GeoFips']]
#need to sort out into large, medium and small economies


#calculate the correaltion 
"""

big_gdp = relevant_rows.loc[relevant_rows['big_economy']==True]['2022'].sum()
everybody_else = relevant_rows.loc[(relevant_rows['big_economy']==False)& (relevant_rows['GeoFips']!='00998')]['2022'].sum()
print("economies of top 25 as a percentage of everything: " + str(big_gdp/(big_gdp+everybody_else)))

