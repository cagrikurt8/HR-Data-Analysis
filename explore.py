import numpy as np
import pandas as pd
import requests
import os


# scroll down to the bottom to implement your solution

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
        'B_office_data.xml' not in os.listdir('../Data') and
        'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.

    # write your code here


def count_bigger_5(worker_group):
    return len(round(worker_group.loc[worker_group.number_project > 5], 2))


a_office_df = pd.read_xml("../Data/A_office_data.xml")
b_office_df = pd.read_xml("../Data/B_office_data.xml")
hr_df = pd.read_xml("../Data/hr_data.xml")

"""print(a_office_df.info())
print(b_office_df.info())
print(hr_df.info())"""

a_index = list()
b_index = list()

for id in a_office_df['employee_office_id']:
    a_index.append(f"A{id}")

for id in b_office_df['employee_office_id']:
    b_index.append(f"B{id}")


a_office_df.set_index([a_index], inplace=True)
b_office_df.set_index([b_index], inplace=True)
hr_df.set_index('employee_id', inplace=True)

a_b_office_df = pd.concat([a_office_df, b_office_df])
final_df = pd.merge(a_b_office_df, hr_df, left_index=True, right_index=True)

final_df.drop(['employee_office_id'], axis=1, inplace=True)
final_df.sort_index(inplace=True)

workers_left = final_df.loc[final_df.left == 1]
workers_still = final_df.loc[final_df.left == 0]

"""
Stage 4

num_pro_median = {0: round(final_df.groupby(by="left").median()["number_project"][0], 2), 1: round(final_df.groupby(by="left").median()["number_project"][1], 2)}
num_pro_5 = {0: count_bigger_5(workers_still), 1: count_bigger_5(workers_left)}
time_mean = {0: round(final_df.groupby(by="left").mean()["time_spend_company"][0], 2), 1: round(final_df.groupby(by="left").mean()["time_spend_company"][1], 2)}
time_median = {0: round(final_df.groupby(by="left").median()["time_spend_company"][0], 2), 1: round(final_df.groupby(by="left").median()["time_spend_company"][1], 2)}
work_accident = {0: round(final_df.groupby(by="left").mean()["Work_accident"][0], 2), 1: round(final_df.groupby(by="left").mean()["Work_accident"][1], 2)}
last_mean = {0: round(final_df.groupby(by="left").mean()["last_evaluation"][0], 2), 1: round(final_df.groupby(by="left").mean()["last_evaluation"][1], 2)}
last_std = {0: round(final_df.groupby(by="left").std()["last_evaluation"][0], 2), 1: round(final_df.groupby(by="left").std()["last_evaluation"][1], 2)}

result_dict = {('number_project', 'median'): num_pro_median,
               ('number_project', 'count_bigger_5'): num_pro_5,
               ('time_spend_company', 'mean'): time_mean,
               ('time_spend_company', 'median'): time_median,
               ('Work_accident', 'mean'): work_accident,
               ('last_evaluation', 'mean'): last_mean,
               ('last_evaluation', 'std'): last_std}

print(result_dict)
"""

table1 = pd.pivot_table(final_df, index=['Department'], columns=['left', 'salary'], values='average_monthly_hours', aggfunc=np.median)

result1 = table1.loc[(table1[(0, 'high')] < table1[(0, 'medium')]) | (table1[(1, 'low')] < table1[(1, 'high')])]

table2 = pd.pivot_table(final_df, index=['time_spend_company'], columns=['promotion_last_5years'], values=['satisfaction_level', 'last_evaluation'], aggfunc=['min', 'max', 'mean'])
table2 = table2.round(decimals=2)

result2 = table2.loc[(table2[('mean', 'last_evaluation', 0)] > table2[('mean', 'last_evaluation', 1)])]

print(result1.to_dict())

print(result2.to_dict())
