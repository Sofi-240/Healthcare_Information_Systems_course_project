import pandas as pd
import numpy as np
import random
import datetime

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
               'Toledano', 'Abuhatzira', 'Harari', 'Ben-Haim'],
    'old_disease_neurological': ['Alzheimer', 'Parkinson', 'Dementia'],
    'Oncology': ['Breast cancer', 'Lung cancer', 'Prostate cancer', 'Colorectal cancer', 'Skin cancer',
                 'Bladder cancer',
                 'Kidney cancer', 'Pancreatic cancer', 'Ovarian cancer', 'Leukemia', 'Lymphoma', 'Liver cancer',
                 'Bone cancer', 'Thyroid cancer', 'Esophageal cancer', 'Stomach cancer', 'Cervical cancer',
                 'Uterine cancer',
                 'Testicular cancer'],
    'neurological': ['Multiple sclerosis', 'Epilepsy', 'Migraines', 'ALS',
                     'Huntington disease', 'Stroke', 'Traumatic brain injury', 'Cerebral palsy',
                     'Tourette syndrome', 'Autism spectrum disorder', 'Schizophrenia', 'CTE', 'Neuropathy'],
    'vascular': ['Atherosclerosis', 'Coronary artery disease', 'Peripheral artery disease', 'Stroke', 'Aortic aneurysm',
                 'Raynaud disease', 'Deep vein thrombosis', 'Pulmonary embolism', 'Varicose veins',
                 'Arteriovenous malformation', 'Thromboangiitis obliterans (Buerger disease)',
                 'Hypertensive heart disease',
                 'Aortic dissection', 'Carotid artery disease', 'Takayasu arteritis'],
    'city': {'N': ['Haifa', 'Nazareth', 'Tiberias', 'Akko', 'Zichron-Yaakov'],
             'S': ['Eilat', 'Beer-Sheva', 'Ashkelon', 'Ashdod'],
             'C': ['Jerusalem', 'Tel-Aviv', 'Netanya', 'Bat-Yam', 'Rishon-LeZion', 'Petah-Tikva', 'Holon', 'Ramat-Gan',
                   'Herzliya', 'Givatayim', 'Rehovot', 'Yavne']},
    'country': {'N': ['Russia', 'Poland', 'England', 'Ukraine', 'Slovakia', 'Czech Republic'],
                'S': ['Argentina', 'Morocco', 'Yemen', 'Tripoli', 'Brazil', 'Italy', 'France']}
}


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


def random_rnf_uni(start, stop, N):
    stack = []
    counter = stop - start
    if N // counter > 0.5:
        return
    while len(stack) < N and counter > 0:
        temp = np.random.randint(10000001, 99999999, (N - len(stack),), dtype=np.int_).astype(str).tolist()
        stack = list(set(stack + temp))
        counter -= 1
    return stack


def diseases_table():
    old_disease_neurological = random_dict['old_disease_neurological']
    Oncology = random_dict['Oncology']
    neurological = random_dict['neurological']
    vascular = random_dict['vascular']
    M = len(Oncology) + len(neurological) + len(vascular) + len(old_disease_neurological)
    data = pd.DataFrame(np.zeros((M, 4)), columns=['DESID', 'DESN', 'DEPID', 'DEPN'])
    data['DESN'] = Oncology + neurological + old_disease_neurological + vascular
    DEPN = ['Oncology'] * len(Oncology) + ['neurological'] * len(neurological)
    DEPN += ['old_disease_neurological'] * len(old_disease_neurological) + ['vascular'] * len(vascular)
    DEPID = [10] * len(Oncology) + [20] * len(neurological) + [10] * len(old_disease_neurological) + [40] * len(
        vascular)
    data['DEPN'] = DEPN
    data['DEPID'] = DEPID
    DESID = []
    for curr_lst in [Oncology, neurological, old_disease_neurological, vascular]:
        stack = []
        counter = 89998
        while len(stack) < len(curr_lst) and counter > 0:
            temp = np.random.randint(10001, 99999, (len(curr_lst) - len(stack),), dtype=np.int_).astype(str).tolist()
            stack += list(set(stack + temp))
            counter -= 1
        DESID += stack

    data['DESID'] = data['DEPID'].astype(str)
    data['DEPID'] = data['DEPID'].astype(str)
    data['DESID'] += DESID
    return data


def patient_table(N, des_df):
    def age(born):
        today = datetime.date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    data = pd.DataFrame(random_item(N, *list(range(1, 4))), columns=['ID'])
    data['ID'] = data['ID'].astype(str)
    data['ID'] += random_rnf_uni(10000001, 99999999, N)

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
    data.loc[mask[:, 0], 'city'] = random_item(mask[:, 0].sum(), *random_dict['city']['N'])
    data.loc[mask[:, 1], 'city'] = random_item(mask[:, 1].sum(), *random_dict['city']['S'])
    data.loc[mask[:, 2], 'city'] = random_item(mask[:, 2].sum(), *random_dict['city']['C'])

    data['phone'] = random_item(N, '050', '054', '052')
    data['phone'] += random_rnf_uni(1000001, 9999999, N)
    data['HMO'] = random_item(N, 'Clalit', 'Maccabi', 'Meuhedet', 'Leumit')

    mask = random_NP_mask(N, 0.3, 0.3)
    data['COB'] = 'Israel'
    data.loc[mask[:, 0], 'COB'] = random_item(mask[:, 0].sum(), *random_dict['country']['N'])
    data.loc[mask[:, 1], 'COB'] = random_item(mask[:, 1].sum(), *random_dict['country']['S'])

    gender_mask = data['gender'] == 'M'
    mask = random_NP_mask(gender_mask.sum(), 0.3, 0.1)
    slc = gender_mask.loc[gender_mask == True]
    data.loc[slc.loc[mask[:, 0]].index, 'height'] = random_item(mask[:, 0].sum(),
                                                                *np.arange(1.50, 1.70, 0.02).tolist())
    data.loc[slc.loc[mask[:, 0]].index, 'weight'] = random_item(mask[:, 0].sum(), *np.arange(44, 80).tolist())

    data.loc[slc.loc[mask[:, 1]].index, 'height'] = random_item(mask[:, 1].sum(),
                                                                *np.arange(1.90, 2.10, 0.02).tolist())
    data.loc[slc.loc[mask[:, 1]].index, 'weight'] = random_item(mask[:, 1].sum(), *np.arange(90, 120).tolist())

    data.loc[slc.loc[mask[:, 2]].index, 'height'] = random_item(mask[:, 2].sum(),
                                                                *np.arange(1.70, 1.90, 0.02).tolist())
    data.loc[slc.loc[mask[:, 2]].index, 'weight'] = random_item(mask[:, 2].sum(), *np.arange(60, 100).tolist())

    gender_mask = data['gender'] == 'F'
    mask = random_NP_mask(gender_mask.sum(), 0.4, 0.1)
    slc = gender_mask.loc[gender_mask == True]
    data.loc[slc.loc[mask[:, 0]].index, 'height'] = random_item(mask[:, 0].sum(),
                                                                *np.arange(1.50, 1.70, 0.02).tolist())
    data.loc[slc.loc[mask[:, 0]].index, 'weight'] = random_item(mask[:, 0].sum(), *np.arange(44, 80).tolist())

    data.loc[slc.loc[mask[:, 1]].index, 'height'] = random_item(mask[:, 1].sum(),
                                                                *np.arange(1.90, 2.10, 0.02).tolist())
    data.loc[slc.loc[mask[:, 1]].index, 'weight'] = random_item(mask[:, 1].sum(), *np.arange(90, 120).tolist())

    data.loc[slc.loc[mask[:, 2]].index, 'height'] = random_item(mask[:, 2].sum(),
                                                                *np.arange(1.70, 1.90, 0.02).tolist())
    data.loc[slc.loc[mask[:, 2]].index, 'weight'] = random_item(mask[:, 2].sum(), *np.arange(60, 100).tolist())

    data.loc[:, 'support'] = random_binary(N, p_true=0.7)
    age = data['DOB'].apply(age)

    uni_id = (des_df['DESN'] == 'Alzheimer') | (des_df['DESN'] == 'Parkinson') | (des_df['DESN'] == 'Dementia')
    age_mask = (age >= 55) & (data['gender'] == 'M')
    mask = random_NP_mask(age_mask.sum(), 0.4)
    slc = age_mask.loc[age_mask == True]

    data.loc[slc.loc[mask[:, 0]].index, 'DID'] = random_item(mask[:, 0].sum(),
                                                             *list(des_df.loc[uni_id == True, 'DESID'].unique()))
    data.loc[slc.loc[mask[:, 1]].index, 'DID'] = random_item(mask[:, 1].sum(),
                                                             *list(des_df.loc[uni_id == False, 'DESID'].unique()))

    age_mask = (age >= 55) & (data['gender'] == 'F')
    mask = random_NP_mask(age_mask.sum(), 0.4)
    slc = age_mask.loc[age_mask == True]

    data.loc[slc.loc[mask[:, 0]].index, 'DID'] = random_item(mask[:, 0].sum(),
                                                             *list(des_df.loc[uni_id == True, 'DESID'].unique()))
    data.loc[slc.loc[mask[:, 1]].index, 'DID'] = random_item(mask[:, 1].sum(),
                                                             *list(des_df.loc[uni_id == False, 'DESID'].unique()))

    age_mask = age < 55
    data.loc[age_mask == True, 'DID'] = random_item(age_mask.sum(),
                                                    *list(des_df.loc[uni_id == False, 'DESID'].unique()))
    return data


diseases_df = diseases_table()
patient_df = patient_table(1000, diseases_df)

# patient_df.to_csv('app\\initialization\\patient.csv', index=False)
# diseases_df.to_csv('app\\initialization\\diseases.csv', index=False)

