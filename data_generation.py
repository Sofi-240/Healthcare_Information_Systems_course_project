import pandas as pd
import numpy as np
import random
from table_obj import Table
from ServerInitiation import connect2serverDB
import datetime

random_dict = {
    'FNames': ['Ariel', 'Yuval', 'Eden', 'Adi', 'Amit', 'Lior', 'Doron', 'Gal', 'Omer', 'Or', 'Rotem', 'Shachar',
               'Shai', 'Shalev', 'Tal', 'Moran', 'Neta', 'Nitzan', 'Sahar'],
    'LNames': ['Cohen', 'Levy', 'Rosenberg', 'Katz', 'Levy-Bencheton', 'Friedland', 'Levi-Abekasis', 'David', 'Shohat',
               'Leviatan', 'Dayan', 'Ashkenazi', 'Mizrahi', 'Aloni', 'Golan', 'Madar', 'Shapiro', 'Weiss', 'Friedman',
               'Goldberg', 'Schwartz', 'Kaplan', 'Stein', 'Berger', 'Rosenbaum', 'Eisenberg', 'Silberstein', 'Kagan',
               'Mizrahi', 'Levy', 'Ben-David', 'Cohen', 'Ezra', 'Azoulay', 'Shoham', 'Sasson', 'Saban', 'Dayan',
               'Toledano', 'Abuhatzira', 'Harari', 'Ben-Haim'],
    'mNames': ['David', 'Yosef', 'Moshe', 'Avraham', 'Yaakov', 'Isaac', 'Samuel', 'Daniel', 'Benjamin', 'Jonathan',
               'Aaron', 'Eitan', 'Itai', 'Ariel', 'Gideon', 'Nathan', 'Reuven', 'Yitzhak', 'Asher', 'Barak',
               'Eliezer', 'Uri', 'Rafi', 'Yair', 'Meir', 'Noam', 'Oren', 'Shlomo', 'Zev', 'Eli', 'Tzur'],
    'fNames': ['Sarah', 'Rachel', 'Leah', 'Rebecca', 'Miriam', 'Esther', 'Hannah', 'Ruth', 'Tamar', 'Batya', 'Shoshana',
               'Devorah', 'Adina', 'Aviva', 'Ayala', 'Bracha', 'Chana', 'Elisheva', 'Gila', 'Hadas', 'Ilana', 'Keren',
               'Liora', 'Michal', 'Naomi', 'Ora', 'Penina', 'Ronit', 'Shira', 'Tova', 'Elior'],
    'date_range': (1965, 2000),
    'City': {'N': ['Haifa', 'Nazareth', 'Tiberias', 'Akko', 'Zichron Yaakov'],
             'S': ['Eilat', 'Beer-Sheva', 'Ashkelon', 'Ashdod'],
             'C': ['Jerusalem', 'Tel-Aviv', 'Netanya', 'Bat-Yam', 'Rishon-LeZion', 'Petah-Tikva', 'Holon', 'Ramat-Gan',
                   'Herzliya', 'Givatayim', 'Rehovot', 'Yavne']},
    'Hospital': {'N': ['Meir', 'Ziv'],
                 'S': ['Soroka', 'Yosef-Tal'],
                 'C': ['Tel-Hashomer', 'Belinson', 'Ichilov']},
    'phone_prefix': ['050', '054', '052'],
    'department': {'Noiro': ['tumer', 'alzhaimer', 'stroke'],
                   'Heart': ['tumer', 'alzhaimer', 'stroke']},
}


def calculate_age(dob):
    return int((datetime.date.today() - dob).days / 365)


def random_phone(prefix=''):
    if not prefix:
        return random_phone(random.choice(random_dict['phone_prefix']))
    if len(prefix) == 10:
        return prefix
    return random_phone(prefix + str(random.choice(range(10))))


def random_city(area):
    return random.choice(random_dict['City'].get(area))


def random_hospital(area):
    return random.choice(random_dict['Hospital'].get(area))


def random_area(N, P_north, P_south):
    return np.random.choice(a=['N', 'S', 'C'], size=(N,), p=[P_north, P_south, 1 - P_north - P_south]).tolist()


def random_ID(curr_id=''):
    if len(curr_id) == 9:
        return curr_id
    if not curr_id:
        return random_ID(str(random.choice(range(1, 10))) + str(random.choice(range(10))))
    return random_ID(curr_id + str(random.choice(range(10))))


def random_binary(N, p_true=0.5):
    return np.random.choice(a=[True, False], size=(N,), p=[p_true, 1 - p_true])


def random_gender(N, p_female=0.5):
    return np.random.choice(a=['F', 'M'], size=(N,), p=[p_female, 1 - p_female])


def random_Name(gender):
    if gender == 'M':
        return random.choice(random_dict['mNames'] + random_dict['FNames']), random.choice(random_dict['LNames'])
    return random.choice(random_dict['fNames'] + random_dict['FNames']), random.choice(random_dict['LNames'])


def random_date(rng=random_dict['date_range']):
    Y = random.randint(rng[0], rng[1])
    M = random.randint(1, 12)
    if M == 2:
        D = random.randint(1, 28)
    else:
        D = random.randint(1, 30)
    return datetime.date(Y, M, D)


def random_diagnostic(department):

    return


# cursor, con = connect2serverDB()
columns = ['ID', 'DB', 'FirstName', 'gender', 'area', 'city', 'phone', 'hospital']
data_N = 1000
hash_map = {'id': {}, 'name': {}, 'phone': {}}
DB_counter = [int(0.3 * data_N), int(0.7 * data_N), 30]
patient_df = pd.DataFrame(np.zeros((data_N, len(columns))), columns=columns)
patient_df['gender'] = random_gender(patient_df.shape[0], 0.6)
patient_df['area'] = random_area(patient_df.shape[0], 0.2, 0.2)
random_dict['date_range'] = (1965, 2000)

for i in list(patient_df.index):
    a, g = patient_df.loc[i, ['area', 'gender']]
    patient_df.loc[i, 'city'] = random_city(a)
    patient_df.loc[i, 'hospital'] = random_hospital(a)
    patient_df.loc[i, 'FirstName'] = random_Name(g)[0]
    d = random_date(random_dict['date_range'])
    age = calculate_age(d)
    if age < 25:
        DB_counter[0] -= 1
    else:
        DB_counter[1] -= 1

    if DB_counter[0] <= 0:
        random_dict['date_range'] = (1965, 1998)

    patient_df.loc[i, 'DB'] = d.strftime('%Y-%m-%d')
    phone = random_phone()
    phone_ptr = 0
    while hash_map['phone'].get(phone) is not None and phone_ptr < data_N:
        phone_ptr += 1
        phone = random_phone()
        print('Searching for phone number iter:', phone_ptr)
    patient_df.loc[i, 'phone'] = random_phone()
    ID = random_ID()
    id_Ptr = 0
    while hash_map['id'].get(ID) is not None and id_Ptr < data_N:
        id_Ptr += 1
        ID = random_ID()
        print('Searching for phone number iter:', id_Ptr)
    patient_df.loc[i, 'ID'] = random_ID()
