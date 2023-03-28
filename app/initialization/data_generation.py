import pandas as pd
import numpy as np
import random
import datetime
import json
import os
from app.initialization.table_obj import Table

random_dict = json.loads(
    open(os.path.split(os.path.dirname(__file__))[0] + '\\initialization\\' + 'random_dict.txt', 'r').read())
symptoms_txt = open(os.path.split(os.path.dirname(__file__))[0] + '\\initialization\\' + 'symptoms.txt', 'r').readlines()


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


def department_table():
    return pd.DataFrame([[10, 'Oncology'], [20, 'Neurological'], [40, 'Vascular']], columns=['DEPID', 'DEPN'])


def diseases_table(department_data):
    old_disease_neurological = random_dict['old_disease_neurological']
    Oncology = random_dict['Oncology']
    neurological = random_dict['Neurological']
    vascular = random_dict['Vascular']
    M = len(Oncology) + len(neurological) + len(vascular) + len(old_disease_neurological)
    data = pd.DataFrame(np.zeros((M, 4)), columns=['DESID', 'DESN', 'DEPID', 'DEPN'])
    data['DESN'] = Oncology + neurological + old_disease_neurological + vascular
    DEPN = ['Oncology'] * len(Oncology) + ['Neurological'] * len(neurological)
    DEPN += ['Neurological'] * len(old_disease_neurological) + ['Vascular'] * len(vascular)
    DEPID = [10] * len(Oncology) + [20] * len(neurological) + [20] * len(old_disease_neurological) + [40] * len(
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


def diseases_symptoms_table(diseases_data):
    diseases_group = diseases_data.groupby(['DESN'], as_index=False)
    data = pd.DataFrame(columns=['DESID', 'DESN', 'Symptom'])

    curr_diseases = ''
    curr_diseases_id = 0
    r = 0
    for line in symptoms_txt:
        if line[-2] == ':':
            curr_diseases = line[:-2]
            curr_diseases_id = diseases_group.get_group(curr_diseases)['DESID'].iloc[0]
        else:
            data.loc[r, :] = [curr_diseases_id, curr_diseases, line[:-2]]
            r += 1

    symptoms_group = data.groupby(['DESID'], as_index=False)
    diseases_group = diseases_data.groupby(['DESID'], as_index=False)
    del_list = []
    for k in list(diseases_group.groups.keys()):
        try:
            symptoms_group.get_group(k)
            continue
        except KeyError:
            del_list.append(diseases_group.get_group(k).index[0])
    if del_list:
        diseases_data.drop(index=del_list, inplace=True)
    return diseases_data, data


def patient_table(N):
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
    for i in range(N):
        y, m, d = stack[i, :]
        data.loc[i, 'DOB'] = datetime.date(y, m, d)

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
    data.loc[:, 'First_diagnosis'] = None
    data.loc[:, 'Second_diagnosis'] = None
    return data


def patient_symptoms_by_gender(gender, diseases_data, symptoms_data, patient_data, patient_symptoms_data=None):
    def age_calc(born):
        today = datetime.date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    if patient_symptoms_data is None:
        patient_symptoms_data = pd.DataFrame(columns=['ID', 'Symptom'])
        r = 0
    else:
        r = patient_symptoms_data.shape[0]
    dep_names = list(diseases_data['DEPN'].unique())
    age = patient_data['DOB'].apply(age_calc)
    diseases_symptoms_group = symptoms_data.groupby(['DESN'])

    old_age_mask = (age >= 60) & (patient_data['gender'] == gender)
    mask = random_NP_mask(old_age_mask.sum(), 0.2, 0.2, 0.3)
    slc = old_age_mask.loc[old_age_mask == True]
    for m, des in enumerate(random_dict['old_disease_neurological']):
        sym = diseases_symptoms_group.get_group(des)
        pet_id = patient_data.loc[slc.loc[mask[:, m]].index, 'ID']
        for curr_id in pet_id:
            curr_sym = set(random.choices(list(sym.index), k=random.choice(range(1, 4))))
            if not curr_sym:
                curr_sym = set(random.choices(list(sym.index), k=1))
            for s in curr_sym:
                patient_symptoms_data.loc[r, :] = [curr_id, sym.loc[s, 'Symptom']]
                r += 1

    age_mask = ((age < 60) & (patient_data['gender'] == gender)) | (old_age_mask == False)
    mask = random_NP_mask(age_mask.sum(), 0.3, 0.3)
    slc = age_mask.loc[age_mask == True]

    for m, curr_dep in enumerate(dep_names):
        curr_des = random_dict[curr_dep]
        pet_id = patient_data.loc[slc.loc[mask[:, m]].index, 'ID']
        for curr_id in pet_id:
            sym = diseases_symptoms_group.get_group(random.choice(curr_des))
            if gender == 'M' and sym['DESN'].iloc[0] == 'Breast cancer':
                sym = diseases_symptoms_group.get_group('Prostate cancer')
            elif gender == 'F' and sym['DESN'].iloc[0] == 'Prostate cancer':
                sym = diseases_symptoms_group.get_group('Breast cancer')
            curr_sym = set(random.choices(list(sym.index), k=random.choice(range(1, 4))))
            if not curr_sym:
                curr_sym = set(random.choices(list(sym.index), k=1))
            for s in curr_sym:
                patient_symptoms_data.loc[r, :] = [curr_id, sym.loc[s, 'Symptom']]
                r += 1
    return patient_symptoms_data


def patient_symptoms_table(diseases_data, symptoms_data, patient_data):
    data = patient_symptoms_by_gender('M', diseases_data, symptoms_data, patient_data)
    data = patient_symptoms_by_gender('F', diseases_data, symptoms_data, patient_data, patient_symptoms_data=data)
    return data


patient_df = patient_table(1000)
department_df = department_table()
diseases_df, diseases_symptoms_df = diseases_symptoms_table(diseases_table(department_df))
patient_symptoms_df = patient_symptoms_table(diseases_df, diseases_symptoms_df, patient_df)




# patient_df = Table('patient',
#                    data=patient_df,
#                    pks=['ID'],
#                    fks=[['First_diagnosis'], ['Second_diagnosis']],
#                    refs=[['First_diagnosis'], ['Second_diagnosis']],
#                    ref_tables=['diseases'])
#
# diseases_df = Table('diseases',
#                     data=diseases_df,
#                     pks=['DESID'],)
# diseases_symptoms_df = Table('diseases_symptoms', data=diseases_symptoms_df)
# patient_symptoms_df = Table('patient_symptoms', data=patient_symptoms_df)
