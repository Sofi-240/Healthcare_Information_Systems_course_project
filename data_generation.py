import pandas as pd
import numpy as np
import random
import datetime
import json

random_dict = json.loads(open('random_dict.txt', 'r').read())


def age(born):
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


def diseases_symptoms_table(diseases_data):
    return


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
    # age = data['DOB'].apply(age)
    #
    # uni_id = (des_df['DESN'] == 'Alzheimer') | (des_df['DESN'] == 'Parkinson') | (des_df['DESN'] == 'Dementia')
    # age_mask = (age >= 55) & (data['gender'] == 'M')
    # mask = random_NP_mask(age_mask.sum(), 0.4)
    # slc = age_mask.loc[age_mask == True]
    #
    # data.loc[slc.loc[mask[:, 0]].index, 'DID'] = random_item(mask[:, 0].sum(),
    #                                                          *list(des_df.loc[uni_id == True, 'DESID'].unique()))
    # data.loc[slc.loc[mask[:, 1]].index, 'DID'] = random_item(mask[:, 1].sum(),
    #                                                          *list(des_df.loc[uni_id == False, 'DESID'].unique()))
    #
    # age_mask = (age >= 55) & (data['gender'] == 'F')
    # mask = random_NP_mask(age_mask.sum(), 0.4)
    # slc = age_mask.loc[age_mask == True]
    #
    # data.loc[slc.loc[mask[:, 0]].index, 'DID'] = random_item(mask[:, 0].sum(),
    #                                                          *list(des_df.loc[uni_id == True, 'DESID'].unique()))
    # data.loc[slc.loc[mask[:, 1]].index, 'DID'] = random_item(mask[:, 1].sum(),
    #                                                          *list(des_df.loc[uni_id == False, 'DESID'].unique()))
    #
    # age_mask = age < 55
    # data.loc[age_mask == True, 'DID'] = random_item(age_mask.sum(),
    #                                                 *list(des_df.loc[uni_id == False, 'DESID'].unique()))
    return data


diseases_df = diseases_table()
patient_df = patient_table(1000)

diseases_symptoms_df = None

# patient_df.to_csv('app\\initialization\\patient.csv', index=False)
# diseases_df.to_csv('app\\initialization\\diseases.csv', index=False)


"""
neurological:
Multiple sclerosis: ['Numbness or tingling in the limbs or face, fatigue', 
                    'difficulty with coordination and balance', muscle stiffness or spasticity,
                    'blurred or double vision, cognitive changes, bladder or bowel dysfunction',
                     'pain or prickling sensations']

Epilepsy: ['Uncontrollable shaking or jerking movements', 'loss of consciousness or awareness', 'staring spells', 
            'sensory changes', 'confusion or disorientation', 'sudden feeling of fear or anxiety', 
            'loss of bowel or bladder control', 'lip smacking', 'chewing', 'or other repetitive movements', 
            'unexplained fatigue or sleepiness', 'headaches or migraines']
            
            
Migraines: ['Intense headache pain', 'usually on one side of the head', 'nausea', 'vomiting', 
            'sensitivity to light and sound', 'visual disturbances', 'dizziness, numbness or tingling sensations']
            
ALS: ['Muscle weakness, stiffness or spasticity', 'difficulty with coordination and balance', 
      'muscle cramps or twitching', 'difficulty with speech or swallowing', 
      'difficulty breathing or shortness of breath', 'unexplained weight loss', 'cognitive changes',
       'fatigue and weakness', 'trouble walking or falling', 'loss of muscle control']
       
Huntington's disease: ['Uncontrollable movements', 'such as chorea or writhing',
                        'difficulty with coordination and balance', 'cognitive changes',
                        'including difficulty with memory, attention and problem-solving',
                        'depression', 'irritability or anxiety', 'trouble swallowing or speaking', 'weight loss']
                          
Stroke: [Sudden weakness or numbness on one side of the body, 
trouble speaking or understanding speech, 
confusion, vision changes, 
difficulty walking or loss of balance, 
severe headache.]

Traumatic brain injury: [Headache, confusion or disorientation, 
nausea or vomiting, 
sensitivity to light or sound, 
sleep disturbances, 
mood changes or irritability, 
difficulty with memory or concentration, 
loss of coordination or balance]

Cerebral palsy: [Difficulty with coordination and balance, 
muscle stiffness or spasticity, 
involuntary movements, 
difficulty with speech or swallowing, 
cognitive impairment, 
seizures, 
vision or hearing problems.
]

Tourette syndrome: [Involuntary movements or vocalizations, such as tics, 
repetitive behaviors or compulsions, 
difficulty with concentration or attention,
 anxiety or depression.]
 
Autism spectrum disorder: [Difficulty with social interactions and communication, 
repetitive behaviors or interests, 
difficulty with sensory processing, 
cognitive inflexibility, 
anxiety or depression.
]
Schizophrenia: [Delusions, 
hallucinations, 
disorganized thinking and speech, 
cognitive impairment, 
difficulty with social interactions and communication, 
disinterest or apathy, 
anxiety or depression.
]

CTE (Chronic Traumatic Encephalopathy): [Cognitive impairment, 
including difficulty with memory, 
attention, and problem-solving, 
depression, 
irritability or aggression, 
trouble with balance and coordination, 
dizziness, 
headaches.
]

Neuropathy: [Numbness or tingling in the hands or feet, 
weakness in the muscles, 
pain or burning sensations, 
sensitivity to touch or temperature, 
muscle cramps or twitching.
]

Oncology:

Breast cancer:[Lump or mass in the breast or underarm, 
nipple discharge or changes, 
breast pain, 
skin changes or dimpling, 
redness or swelling of the breast or nipple.
]

Lung cancer: [Persistent cough,
 coughing up blood or phlegm, 
 chest pain or discomfort, 
 shortness of breath, 
 hoarseness, 
 wheezing, 
 unexplained weight loss or fatigue.
]
Prostate cancer:[Difficulty with urination or changes in frequency, 
weak or interrupted urine flow, 
blood in the urine or semen, 
pain or discomfort in the pelvic area or lower back.
]

Colorectal cancer: [Changes in bowel habits, 
including diarrhea or constipation, 
rectal bleeding or blood in the stool, 
abdominal pain or cramping, 
unexplained weight loss or fatigue.
]

Skin cancer: [Changes in the appearance of a mole or other skin lesion, 
including size, 
shape, or color, 
a sore that doesn't heal, 
redness or swelling of the skin.
]

Bladder cancer: [Blood in the urine, 
pain or burning during urination, 
increased frequency or urgency to urinate, 
lower back pain or abdominal pain.
]

Kidney cancer: [Blood in the urine, 
pain or discomfort in the side or lower back, 
a mass or lump in the abdomen, 
unexplained weight loss or fatigue, fever.
]

Pancreatic cancer: [Abdominal pain or discomfort, 
unexplained weight loss or fatigue, 
loss of appetite, 
jaundice or yellowing of the skin and eyes, 
nausea or vomiting.
]

Ovarian cancer: [Abdominal bloating or swelling,
 pelvic pain or discomfort, 
 changes in bowel habits, 
 unexplained weight loss or fatigue.
]
Leukemia: [Fatigue or weakness,
 frequent infections,
  fever, 
  unexplained weight loss,
   bone or joint pain, 
   bruising or bleeding easily, 
   swollen lymph nodes.
]
Lymphoma: [Enlarged lymph nodes,
 unexplained weight loss,
  fatigue, 
  fever, 
  night sweats,
   itching.]

Liver cancer: [Abdominal pain or discomfort, 
unexplained weight loss or fatigue, 
jaundice or yellowing of the skin and eyes, 
swelling in the abdomen, nausea or vomiting.
]
Bone cancer: [Bone pain, 
swelling or tenderness near the affected area, 
unexplained fractures or breaks.]

Thyroid cancer: [Lump or swelling in the neck, 
difficulty swallowing or breathing,
 hoarseness or changes in voice, pain in the neck or throat.]

Esophageal cancer: [Difficulty swallowing or painful swallowing,
 chest pain or discomfort,
  unexplained weight loss or fatigue.
]

Stomach cancer: [Abdominal pain or discomfort,
 nausea or vomiting, 
 unexplained weight loss or fatigue, 
 loss of appetite, 
 feeling full after eating small amounts.
]
Cervical cancer: [Abnormal vaginal bleeding or discharge, 
pelvic pain or discomfort, 
pain during sex.]

Uterine cancer: [Abnormal vaginal bleeding or discharge,
 pelvic pain or discomfort,
  pain during sex, 
  unexplained weight loss or fatigue.]

Testicular cancer:[ A lump or swelling in the testicle,
 pain or discomfort in the testicle or scrotum, 
 a feeling of heaviness in the scrotum.]


vascular:

Atherosclerosis: [Chest pain or discomfort (angina), 
shortness of breath, pain or numbness in the legs or arms, 
fatigue, 
weakness.]

Coronary artery disease: [Chest pain or discomfort (angina), 
shortness of breath, 
fatigue, 
dizziness or lightheadedness, 
nausea or vomiting.]

Peripheral artery disease: [Pain or cramping in the legs or arms during activity, 
slow healing wounds or sores on the legs or feet, 
discoloration or coolness of the skin on the legs or feet.
]
Stroke: [Sudden numbness or weakness in the face,
 arm, 
 or leg (especially on one side of the body), 
 sudden confusion, 
 trouble speaking or understanding speech, 
 sudden trouble seeing in one or both eyes, 
 sudden trouble walking, 
 dizziness, or loss of balance or coordination, 
 sudden severe headache with no known cause.
]
Aortic aneurysm: [Pain in the chest,
 back, 
 or abdomen, 
 difficulty breathing or swallowing, 
 hoarseness, coughing or wheezing,
  rapid heart rate.
]
Raynaud disease: [Numbness, 
tingling, 
or pain in the fingers or toes, 
changes in skin color in response to cold or stress, 
cold hands or feet.
]
Deep vein thrombosis: [Swelling,
 pain, or tenderness in the affected leg or arm, 
 warmth or redness in the affected area, 
 a feeling of heaviness or tightness in the affected limb.
]
Pulmonary embolism:[Sudden shortness of breath, 
chest pain or discomfort (often worse with deep breaths), 
rapid or irregular heartbeat, coughing up blood, 
feeling lightheaded or faint.
]
Varicose veins: [Enlarged veins that are visible under the skin, 
often in the legs or feet, 
swelling in the affected area, aching or heaviness in the affected limb,
 itching or burning sensation over the vein.
]
Arteriovenous malformation: [Seizures or other neurological symptoms, 
headache, muscle weakness or paralysis, 
problems with vision or hearing, 
difficulty speaking or understanding speech.
]
Thromboangiitis obliterans (Buerger disease): [Pain and tenderness in the affected limb (often the legs or feet),
 cool or pale skin in the affected area, open sores or ulcers, 
 gangrene or tissue death.
]
Hypertensive heart disease: [Chest pain or discomfort (angina), 
shortness of breath, 
fatigue, 
irregular heartbeat,
 swelling in the legs or feet.
]
Aortic dissection: [Sudden severe pain in the chest or upper back, 
often described as tearing or ripping, shortness of breath,
 weakness or paralysis on one side of the body,
  difficulty speaking or understanding speech.
]
Carotid artery disease: [Weakness or numbness on one side of the body,
 difficulty speaking or understanding speech,
  sudden loss of vision in one eye, 
  severe headache.
]
Takayasu arteritis: [Fatigue, 
joint pain or stiffness, 
unexplained weight loss, 
fever, 
muscle pain or weakness, 
skin rash or redness.]



Alzheimer:['Memory loss that disrupts daily life', 'Difficulty completing familiar tasks',
            'Challenges with problem-solving or planning',
            'Confusion with time or place',
            'Trouble with visual images and spatial relationships',
            'New problems with speaking or writing',
            'Misplacing items and being unable to retrace steps',
            'Changes in mood or personality',
            'Withdrawal from social activities']
            
Parkinson's: ['Tremors especially in the hands or fingers', 'Slow movement (bradykinesia)',
            'Muscle stiffness (rigidity)',
            'Impaired balance and coordination',
            'Changes in speech, including slurred or soft speech',
            'Difficulty with fine motor tasks, such as buttoning clothes or writing',
            'Decreased ability to perform unconscious movements, such as blinking or swinging arms while walking',
            'Stooped posture',
            'Expressive face with a blank or serious expression']


Dementia:   ['Memory loss that disrupts daily life',
            'Difficulty with communication and language',
            'Impaired reasoning and judgment',
            'Difficulty with complex tasks and activities, such as managing finances or taking medications',
            'Impaired visual perception and spatial skills',
            'Changes in mood and personality',
            'Social withdrawal and isolation',
            'Changes in sleep patterns',
            'Loss of initiative and motivation']
"""
