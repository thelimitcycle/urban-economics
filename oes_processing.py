import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

save_data = True
#load the pre-processed oes database into memory
oes = pd.read_csv('oes-relevant.csv')

#make sure the columns I want to do calculations on are the correct type
oes['TOT_EMP'] = pd.to_numeric(oes['TOT_EMP'],errors ='coerce').fillna(0).astype('int')
oes['A_MEDIAN'] = pd.to_numeric(oes['A_MEDIAN'],errors ='coerce').fillna(0).astype('int')
oes['H_MEDIAN'] = pd.to_numeric(oes['H_MEDIAN'],errors ='coerce').fillna(0).astype('int')
#columns for data processing
oes['percentage_of_msa_emp'] = 0
oes['emp_ratio_to_USA'] = 0
oes['big_economy'] = False

oes['a_median_adj'] = 0
oes['h_median_adj'] = 0

oes['a_median_adj_ratio_to_USA'] = 0
oes['h_median_adj_ratio_to_USA'] = 0

#load the rpp database into memory
rpp = pd.read_csv('rpp-2022.csv',skiprows=3)

#make sure the GeoFips column is an integer
rpp['GeoFips'] = pd.to_numeric(rpp['GeoFips'],errors ='coerce').fillna(0).astype('int')

GeoFips = oes['AREA'].unique().tolist() #get the FIPS codes
emp_totals = dict(zip(GeoFips, [0]*len(GeoFips)))

top_25_fips = [35620, 31080, 41860, 16980, 19100, 42660, 14460, 33100, 12060, 47900, 26420, 38060, 19820, 37980, 41740, 41940, 33460, 40140, 12420, 45300, 12580, 19740, 36740, 16740]
top_50_fips = [35620, 31080, 41860, 16980, 19100, 42660, 14460, 33100, 12060, 47900, 26420, 38060, 19820, 37980, 41740, 41940, 33460, 40140, 12420, 45300, 12580, 19740, 36740, 16740, 38300, 40900, 17460, 29820, 18140, 38900, 34980, 17140, 26900, 41620, 41700, 41180, 28140, 47260, 25540, 33340, 14860, 39580, 40060, 39300, 15380, 10580, 35380, 46520, 24340]
#compute the percentage of people employed in each sector for each city and how it compares
#to the country as a whole
for gf in GeoFips:
    n_row, n_col = oes.loc[oes['AREA']==gf].shape
    try:
        #don't know a better way of pulling out just the number...
        rpp_value = (rpp.loc[(rpp['GeoFips']== gf) & (rpp['LineCode']== 1.0)]['2022'].to_numpy()[0])/100.0
    except IndexError:
        
        rpp_value=1.0
    
    
    if n_row == 22:
    
        total_emp = oes.loc[oes['AREA'] == gf]['TOT_EMP'].sum()
        emp_totals[gf] = total_emp

        oes.loc[oes['AREA']==gf, 'percentage_of_msa_emp'] = oes.loc[oes['AREA']==gf]['TOT_EMP'].div(total_emp)
        oes.loc[oes['AREA']==gf, 'emp_ratio_to_USA'] = (oes.loc[oes['AREA']==gf]['percentage_of_msa_emp'].to_numpy())/(oes.loc[oes['AREA']== 99]['percentage_of_msa_emp'].to_numpy())
        oes.loc[oes['AREA']==gf, 'big_economy'] = gf in top_50_fips
        #adjust the hourly and annual wages for the RPP cost of living
        oes.loc[oes['AREA']==gf, 'a_median_adj'] = oes.loc[oes['AREA']==gf]['A_MEDIAN'].div(rpp_value)
        oes.loc[oes['AREA']==gf, 'h_median_adj'] = oes.loc[oes['AREA']==gf]['H_MEDIAN'].div(rpp_value)
#split the table on the other axis: compare the job across cities and see how each city's wages compare
#after adjusting for cost of living

occ_codes = oes['OCC_CODE'].unique().tolist()
occ_names = oes['OCC_TITLE'].unique().tolist()
#need to make a translator dicionary for OCC code to Human readable
#this is kind of hacky because it relies on the unique function reading the entries in order, but it should work
occ_decoder = dict(zip(occ_codes,occ_names))

for occ in occ_codes:
    us_avg_a = oes.loc[(oes['OCC_CODE']==occ) & (oes['AREA']==99)]['A_MEDIAN'].to_numpy()[0]
    us_avg_h = oes.loc[(oes['OCC_CODE']==occ) & (oes['AREA']==99)]['H_MEDIAN'].to_numpy()[0]
    oes.loc[((oes['OCC_CODE']==occ)),'a_median_adj_ratio_to_USA'] = oes.loc[(oes['OCC_CODE']==occ)]['a_median_adj'].div(us_avg_a)
    oes.loc[((oes['OCC_CODE']==occ)),'h_median_adj_ratio_to_USA'] = oes.loc[(oes['OCC_CODE']==occ)]['h_median_adj'].div(us_avg_h)
    #make some plots??
    
    occ_emp_ratio = oes.loc[(oes['OCC_CODE']==occ) & (oes['big_economy']==True)]['emp_ratio_to_USA'].to_numpy()
    occ_sal_ratio = oes.loc[(oes['OCC_CODE']==occ) & (oes['big_economy']==True)]['a_median_adj_ratio_to_USA'].to_numpy()
    #maybe I need to sort them?
    corr = np.corrcoef(occ_emp_ratio,occ_sal_ratio)
    m,b = np.polyfit(occ_emp_ratio,occ_sal_ratio,1)
    slope, intercept, r_value, p_value, std_err = stats.linregress(occ_emp_ratio, occ_sal_ratio)
    r2 = r_value*r_value

    x = np.linspace(occ_emp_ratio.min(), occ_emp_ratio.max(), 50)
    y = slope*x +intercept
    plt.figure()
    plt.scatter(occ_emp_ratio,occ_sal_ratio)
    plt.plot(x,y,color='red', linewidth=2)
    plt.xlabel('MSA to USA employment ratio ')
    plt.ylabel('MSA to USA salary ratio')
    plt.xlim([0,4.5])
    plt.ylim([0,2])
    plt.title(occ_decoder[occ] + '\n correlation = {:.3f} n=50, m={:.3f}, r^2={:.3f}'.format(corr[1,0], m, r2))
    plt.savefig('plots/' + occ_decoder[occ] + '_scatter.png')
    plt.close()


if save_data == True:
    oes.to_csv('oes-crunched.csv')


#now its time to run some statistics and make some charts

