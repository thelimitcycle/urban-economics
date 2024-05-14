import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

rentsdf = pd.read_excel('FY2024_FMR_50_area_revised_edited.xlsx')
incomesdf = pd.read_csv('median_income_msa.csv')
top_50_fips = [35620, 31080, 41860, 16980, 19100, 42660, 14460, 33100, 12060, 47900, 26420, 38060, 19820, 37980, 41740, 41940, 33460, 40140, 12420, 45300, 12580, 19740, 36740, 16740, 38300, 40900, 17460, 29820, 18140, 38900, 34980, 17140, 26900, 41620, 41700, 41180, 28140, 47260, 25540, 33340, 14860, 39580, 40060, 39300, 15380, 10580, 35380, 46520, 24340]
rentsdf_msa = rentsdf.loc[((rentsdf['is_msa']==True)&(rentsdf['is_whole_msa']==True))]
result = pd.merge(incomesdf, rentsdf_msa, left_on='AREA', right_on='Fips', how='inner')
top_50 = result.loc[result['AREA'].isin(top_50_fips)]
rents_msa = top_50['rent_50_2'].to_numpy()
incomes_msa = top_50['A_MEDIAN'].to_numpy()

corr = np.corrcoef(incomes_msa,rents_msa)
m,b = np.polyfit(incomes_msa,rents_msa,1)
slope, intercept, r_value, p_value, std_err = stats.linregress(incomes_msa, rents_msa)
r2 = r_value*r_value

x = np.linspace(incomes_msa.min(), incomes_msa.max(),50)
y = slope*x + intercept

plt.figure()
plt.scatter(incomes_msa,rents_msa)
plt.plot(x,y,color='red', linewidth=2)
plt.ylabel('median monthly rent for 2br apartment [USD]')
plt.xlabel('median annual income [USD]')
plt.title("median annual income vs median monthly rent for top 50 urban economies" + '\n correlation = {:.3f} n=50, m={:.3f}, r^2={:.3f}'.format(corr[1,0], m, r2))
plt.show()