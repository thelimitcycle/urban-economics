import pandas as pd

oes = pd.read_excel('all_data_M_2022.xlsx',sheet_name='All May 2022 data')

#so I'm going to want area types 1 (USA) and 4 (MSA)

#and lets start with "major" category
"""
['AREA', 'AREA_TITLE', 'AREA_TYPE', 'PRIM_STATE', 'NAICS', 'NAICS_TITLE',
      'I_GROUP', 'OWN_CODE', 'OCC_CODE', 'OCC_TITLE', 'O_GROUP', 'TOT_EMP',
       'EMP_PRSE', 'JOBS_1000', 'LOC_QUOTIENT', 'PCT_TOTAL', 'PCT_RPT',
       'H_MEAN', 'A_MEAN', 'MEAN_PRSE', 'H_PCT10', 'H_PCT25', 'H_MEDIAN',
       'H_PCT75', 'H_PCT90', 'A_PCT10', 'A_PCT25', 'A_MEDIAN', 'A_PCT75',
       'A_PCT90', 'ANNUAL', 'HOURLY']
"""
# print(oes['AREA_TYPE'].unique())
# oes_relevant = oes.loc[((oes['AREA_TYPE'] == 1 ) | (oes['AREA_TYPE'] == 4 )) &(oes['O_GROUP']=='major') & (oes['NAICS']=='000000')]

# oes_relevant.to_csv('oes-relevant.csv')

#now just do that same analysis that I did with the cagdp2 data

oes_median_income = oes.loc[((oes['AREA_TYPE']== 4)& (oes['OCC_CODE']=="00-0000"))]
oes_median_income.to_csv('median_income_msa.csv')
