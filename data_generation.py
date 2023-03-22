import pandas as pd
import numpy as np
import random
from table_obj import Table
import ServerInitiation as server
import datetime
import os

random_dict = {
    'Fname': {'M': ['David', 'Yosef', 'Moshe', 'Avraham', 'Yaakov', 'Isaac', 'Samuel', 'Daniel', 'Benjamin', 'Jonathan',
                    'Aaron', 'Eitan', 'Itai', 'Ariel', 'Gideon', 'Nathan', 'Reuven', 'Yitzhak', 'Asher', 'Barak',
                    'Eliezer', 'Uri', 'Rafi', 'Yair', 'Meir', 'Noam', 'Oren', 'Shlomo', 'Zev', 'Eli', 'Tzur',
                    'Ariel', 'Yuval', 'Eden', 'Adi', 'Amit', 'Lior', 'Doron', 'Gal', 'Omer', 'Or', 'Rotem', 'Shachar',
                    'Shai', 'Shalev', 'Tal', 'Moran', 'Neta', 'Nitzan', 'Sahar'],
              'F': ['Sarah', 'Rachel', 'Leah', 'Rebecca', 'Miriam', 'Esther', 'Hannah', 'Ruth', 'Tamar', 'Batya',
                    'Shoshana', 'Devorah', 'Adina', 'Aviva', 'Ayala', 'Bracha', 'Chana', 'Elisheva', 'Gila', 'Hadas',
                    'Ilana', 'Keren', 'Liora', 'Michal', 'Naomi', 'Ora', 'Penina', 'Ronit', 'Shira', 'Tova', 'Elior',
                    'Ariel', 'Yuval', 'Eden', 'Adi', 'Amit', 'Lior', 'Doron', 'Gal', 'Omer', 'Or', 'Rotem', 'Shachar',
                    'Shai', 'Shalev', 'Tal', 'Moran', 'Neta', 'Nitzan', 'Sahar']},
    'LNames': ['Cohen', 'Levy', 'Rosenberg', 'Katz', 'Levy-Bencheton', 'Friedland', 'Levi-Abekasis', 'David', 'Shohat',
               'Leviatan', 'Dayan', 'Ashkenazi', 'Mizrahi', 'Aloni', 'Golan', 'Madar', 'Shapiro', 'Weiss', 'Friedman',
               'Goldberg', 'Schwartz', 'Kaplan', 'Stein', 'Berger', 'Rosenbaum', 'Eisenberg', 'Silberstein', 'Kagan',
               'Mizrahi', 'Levy', 'Ben-David', 'Cohen', 'Ezra', 'Azoulay', 'Shoham', 'Sasson', 'Saban', 'Dayan',
               'Toledano', 'Abuhatzira', 'Harari', 'Ben-Haim']}

data_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], "project_data\\")


def age(born):
    # born = datetime.datetime.strptime(born, "%d/%m/%Y").date()
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def random_binary(n, p_true=0.5):
    return np.random.choice(a=[True, False], size=(n,), p=[p_true, 1 - p_true])


def random_NP_mask(n, *P_args):
    P_args = list(P_args)
    s = 0
    for i, p in enumerate(P_args):
        s += p
    if s > 1:
        return np.zeros((n,), dtype=bool)
    if s != 1:
        P_args += [1 - s]
        i += 1
    mask = np.zeros((n, i + 1), dtype=bool)
    temp = np.random.choice(a=list(range(i + 1)), size=(n,), p=P_args)

    for n in range(i + 1):
        mask[np.where(temp == n)[0], n] = True

    return mask


def random_item(n, *P_args):
    return np.array(random.choices(P_args, k=n), dtype=type(P_args[0]))


def patient_table(N):
    data = pd.DataFrame(random_item(N, *list(range(1, 4))), columns=['ID'])
    data['ID'] = data['ID'].astype(str)
    stack = []
    counter = 89999998
    while len(stack) < N and counter > 0:
        temp = np.random.randint(10000001, 99999999, (N - len(stack),), dtype=np.int_).astype(str).tolist()
        stack = list(set(stack + temp))
        counter -= 1
    if counter <= 0:
        return
    data['ID'] += stack

    mask = random_NP_mask(N, 0.6)
    data['gender'] = 'M'
    data.loc[mask[:, 0], 'gender'] = 'F'
    data.loc[mask[:, 0], 'name'] = random_item(mask[:, 0].sum(), *random_dict['Fname']['F'])
    data.loc[mask[:, 1], 'name'] = random_item(mask[:, 1].sum(), *random_dict['Fname']['M'])

    stack = np.vstack((np.zeros((N,)), random_item(N, *list(range(1, 13))), random_item(N, *list(range(1, 31))))).T
    stack[np.where((stack[:, 2] >= 29) & (stack[:, 1] == 2))[0], 2] -= 4
    mask = random_NP_mask(N, 0.2, 0.3, 0.5)
    stack[mask[:, 0], 0] = random_item(mask[:, 0].sum(), *list(range(1985, 1997)))
    stack[mask[:, 1], 0] = random_item(mask[:, 1].sum(), *list(range(1975, 1985)))
    stack[mask[:, 2], 0] = random_item(mask[:, 2].sum(), *list(range(1950, 1975)))
    stack = stack.astype(int)
    stack = pd.DataFrame(stack, columns=['year', 'month', 'day'])
    stack = pd.to_datetime(stack, unit='D')
    data['DOB'] = stack

    mask = random_NP_mask(N, 0.3, 0.2)
    data['area'] = 'C'
    data.loc[mask[:, 0], 'area'] = 'N'
    data.loc[mask[:, 1], 'area'] = 'S'
    data.loc[mask[:, 0], 'city'] = random_item(mask[:, 0].sum(), 'Haifa', 'Nazareth', 'Tiberias', 'Akko',
                                               'Zichron Yaakov')
    data.loc[mask[:, 1], 'city'] = random_item(mask[:, 1].sum(), 'Eilat', 'Beer-Sheva', 'Ashkelon',
                                               'Ashdod')
    data.loc[mask[:, 2], 'city'] = random_item(mask[:, 2].sum(), 'Jerusalem', 'Tel-Aviv', 'Netanya',
                                               'Bat-Yam', 'Rishon-LeZion', 'Petah-Tikva', 'Holon', 'Ramat-Gan',
                                               'Herzliya', 'Givatayim', 'Rehovot', 'Yavne')

    data['phone'] = random_item(N, '050', '054', '052')
    counter = 8999998
    stack = []
    while len(stack) < N and counter > 0:
        temp = np.random.randint(1000001, 9999999, (N - len(stack),), dtype=np.int_).astype(str).tolist()
        stack = list(set(stack + temp))
        counter -= 1
    if counter <= 0:
        return
    data['phone'] += stack
    data['HMO'] = random_item(N, 'Clalit', 'Maccabi', 'Meuhedet', 'Leumit')
    return data


patient_df = patient_table(1000)
# patient_df.to_csv(data_path + 'patient.csv', index=False)
# cursor, con = server.connect2serverDB()
# patient_df = Table('patient', 'patient', ['ID'])
# server.createNewTable(patient_df)
# server.addPKs(patient_df)


# age = patient_df['DOB'].apply(age)
# patient_diagnosis = pd.DataFrame(patient_df['ID'].copy(deep=True))
# mask = (patient_df['gender'] == 'M') & (age >= 70)
# r_mask = random_NP_mask(mask.sum(), 0.3)
# patient_diagnosis.loc[r_mask[:, 0], 'disease'] = random_item(r_mask[:, 0].sum(), 'Alzheimer', 'Parkinson')
