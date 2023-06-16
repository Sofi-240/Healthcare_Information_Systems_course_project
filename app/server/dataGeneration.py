import pandas as pd
import numpy as np
import random
import datetime
import json
import os
from app.server.tableObj import Table

random_dict = json.loads(
    open(os.path.split(os.path.dirname(__file__))[0] + '\\server\\' + 'random_dict.txt', 'r').read())
symptoms_txt = open(os.path.split(os.path.dirname(__file__))[0] + '\\server\\' + 'symptoms.txt',
                    'r').readlines()


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
    try:
        stack = np.array(random.sample(range(start, stop), N))
    except ValueError:
        print('Sample size exceeded population size.')
    return stack


def department_table():
    return pd.DataFrame([[10, 'Oncology'], [20, 'Neurological'], [30, 'Vascular']], columns=['depID', 'depName'])


def diseases_table(department_data):
    DES_N = []
    DEP_ID = []
    DEP_nameLst = []
    for idx in list(department_data.index):
        dep_name = department_data.loc[idx, 'depName']
        dep_Id = department_data.loc[idx, 'depID']
        if dep_name == 'Neurological':
            DES_N += random_dict['old_disease_neurological']
            DEP_ID += [dep_Id] * len(random_dict['old_disease_neurological'])
            DEP_nameLst += [dep_name] * len(random_dict['old_disease_neurological'])
        DES_N += random_dict[dep_name]
        DEP_ID += [dep_Id] * len(random_dict[dep_name])
        DEP_nameLst += [dep_name] * len(random_dict[dep_name])

    data = pd.DataFrame(np.zeros((len(DES_N), 3)), columns=['disID', 'disName', 'depID'])
    data['depID'] = DEP_ID
    data['depID'] = data['depID'].astype(str)
    data['disID'] = data['depID']
    data['depName'] = DEP_nameLst
    data['disName'] = DES_N
    data['disID'] = random_rnf_uni(100001, 999999, len(DES_N)).astype(str)
    return data


def diseases_symptoms_table(diseases_data):
    diseases_group = diseases_data.groupby(['disName'], as_index=False)
    data = pd.DataFrame(columns=['disID', 'disName', 'Symptom'])

    curr_diseases = ''
    curr_diseases_id = 0
    r = 0
    for line in symptoms_txt:
        if line[-2] == ':':
            curr_diseases = line[:-2]
            if not curr_diseases[0].isupper():
                ch, curr_diseases = curr_diseases[0], curr_diseases[1:]
                ch = ch.upper()
                curr_diseases[0] = ch + curr_diseases
            curr_diseases_id = diseases_group.get_group(curr_diseases)['disID'].iloc[0]
        else:
            temp = line[:-1].lower().split()
            if len(temp) == 2 and temp[1] == 'pain':
                temp = [temp[1]] + ['in', 'the'] + [temp[0]]
            data.loc[r, :] = [curr_diseases_id, curr_diseases, ' '.join(temp)]
            r += 1

    symptoms_group = data.groupby(['disID'], as_index=False)
    diseases_group = diseases_data.groupby(['disID'], as_index=False)
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


def patient_table(IDlist):
    N = len(IDlist)
    data = pd.DataFrame(IDlist, columns=['ID'])
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
    data['phone'] += random_rnf_uni(1000001, 9999999, N).astype(str)
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
    return data


def patient_symptoms_by_gender(gender, symptoms_data, patient_data, department_data,
                               patient_symptoms_data=None):
    def age_calc(born):
        today = datetime.date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    if patient_symptoms_data is None:
        patient_symptoms_data = pd.DataFrame(columns=['ID', 'Symptom'])
        r = 0
    else:
        r = patient_symptoms_data.shape[0]
    age = patient_data['DOB'].apply(age_calc)
    diseases_symptoms_group = symptoms_data.groupby(['disName'])
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

    for m, curr_dep in enumerate(list(department_data['depName'].unique())):
        curr_des = random_dict[curr_dep]
        pet_id = patient_data.loc[slc.loc[mask[:, m]].index, 'ID']
        for curr_id in pet_id:
            sym = diseases_symptoms_group.get_group(random.choice(curr_des))
            if gender == 'M' and sym['disName'].iloc[0] == 'Breast cancer':
                sym = diseases_symptoms_group.get_group('Prostate cancer')
            elif gender == 'F' and sym['disName'].iloc[0] == 'Prostate cancer':
                sym = diseases_symptoms_group.get_group('Breast cancer')
            curr_sym = set(random.choices(list(sym.index), k=random.choice(range(1, 4))))
            if not curr_sym:
                curr_sym = set(random.choices(list(sym.index), k=1))
            for s in curr_sym:
                patient_symptoms_data.loc[r, :] = [curr_id, sym.loc[s, 'Symptom']]
                r += 1
    return patient_symptoms_data


def patient_symptoms_table(symptoms_data, patient_data, department_data):
    data = patient_symptoms_by_gender('M', symptoms_data, patient_data, department_data)
    data = patient_symptoms_by_gender('F', symptoms_data, patient_data, department_data,
                                      patient_symptoms_data=data)
    return data


def researcher_table(IDlist):
    N = len(IDlist)
    data = pd.DataFrame(IDlist, columns=['ID'])

    mask = random_NP_mask(N, 0.7)
    data['gender'] = 'M'
    data.loc[mask[:, 0], 'gender'] = 'F'
    data.loc[mask[:, 0], 'Fname'] = random_item(mask[:, 0].sum(), *random_dict['Fname']['F'])
    data.loc[mask[:, 1], 'Fname'] = random_item(mask[:, 1].sum(), *random_dict['Fname']['M'])
    data.loc[:, 'Lname'] = random_item(N, *random_dict['LNames'])
    data['phone'] = random_item(N, '050', '054', '052')
    data['phone'] += random_rnf_uni(1000001, 9999999, N).astype(str)
    data.loc[:, 'Mail'] = data.loc[:, 'Fname'] + '_' + data.loc[:, 'Lname'] + pd.Series(
        random_rnf_uni(1000, 9999, N)).astype(str)
    data.loc[:, 'Mail'] += '@LUKA.com'
    return data


def initActiveR():
    return pd.DataFrame(columns=['ID', 'disID', 'rID', 'pID'])


def Trigger_table(patient_data):
    return pd.DataFrame(columns=['ID', 'FdisID', 'Fconf', 'SdisID', 'Sconf'])


def main():
    ids_uni = pd.DataFrame(random_item(1050, *list(range(1, 4))), columns=['ID'])
    ids_uni['ID'] = ids_uni['ID'].astype(str)
    ids_uni['ID'] += random_rnf_uni(10000001, 99999999, 1050).astype(str)
    ids_uni = list(ids_uni['ID'])
    patient = patient_table(ids_uni[:1000])
    department = department_table()
    diseases, diseases_symptoms = diseases_symptoms_table(diseases_table(department))
    patient_symptoms = patient_symptoms_table(diseases_symptoms, patient, department)
    diseases_symptoms.drop(columns='disName', inplace=True)
    researcher = researcher_table(ids_uni[1000:])
    ActiveResearch = initActiveR()
    patient['DOB'] = patient['DOB'].astype(str)
    PatientDiagnosis = Trigger_table(patient)

    Table('patient',
          data=patient,
          pks=['ID']).save()

    Table('diseases',
          data=diseases.merge(diseases_symptoms, how='inner', on='disID')).save()

    Table('patientdiagnosis',
          data=PatientDiagnosis,
          pks=['ID'],
          fks=[['ID']],
          refs=[['ID']],
          ref_tables=['patient']).save()

    Table('symptomsPatient',
          data=patient_symptoms,
          fks=[['ID']],
          refs=[['ID']],
          ref_tables=['patient']).save()

    Table('researcher',
          data=researcher,
          pks=['ID']).save()

    Table('activeresearch',
          data=ActiveResearch,
          fks=[['rID']],
          refs=[['ID']],
          ref_tables=['researcher']).save()

    file = open(os.path.split(os.path.dirname(__file__))[0] + '\\server\\' + 'searchHashFile.txt', 'w')
    file.write(json.dumps({}))


if __name__ == "__main__":
    random_dict = json.loads(
        open(os.path.split(os.path.dirname(__file__))[0] + '\\server\\' + 'random_dict.txt', 'r').read())
    symptoms_txt = open(os.path.split(os.path.dirname(__file__))[0] + '\\server\\' + 'symptoms.txt',
                        'r').readlines()
    main()
