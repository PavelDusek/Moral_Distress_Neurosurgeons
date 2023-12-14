#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import datetime
import numpy as np

df = pd.read_excel('survey-data-burnout-moral-injury-survey-3.xlsx')
print(df.columns)

metadata = {
    'Datum': 'date',
    'Čas': 'time',
    'Dokončeno za': 'duration',
    'Zdroj': 'source',

    'Burnout (Oldenburg Burnout Inventory) x I always find new and interesting\naspects in my work.': 'OLBI1',
    'Burnout (Oldenburg Burnout Inventory) x There are days when I feel tired\nbefore I arrive at work.': 'OLBI2',
    'Burnout (Oldenburg Burnout Inventory) x After work, I tend to need more time\nthan in the past in order to relax\nand feel better': 'OLBI3',
    'Burnout (Oldenburg Burnout Inventory) x It happens more and more often\nthat I talk about my work in a\nnegative way.': 'OLBI4',
    'Burnout (Oldenburg Burnout Inventory) x I can tolerate the pressure of my\nwork very well.': 'OLBI5',
    'Burnout (Oldenburg Burnout Inventory) x Lately, I tend to think less at work\nand do my job almost mechanically.': 'OLBI6',
    'Burnout (Oldenburg Burnout Inventory) x I find my work to be a positive\nchallenge.': 'OLBI7',
    'Burnout (Oldenburg Burnout Inventory) x During my work, I often feel\nemotionally drained.': 'OLBI8',
    'Burnout (Oldenburg Burnout Inventory) x Over time, one can become\ndisconnected from this type of\nwork.': 'OLBI9',
    'Burnout (Oldenburg Burnout Inventory) x After working, I have enough\nenergy for my leisure activities.': 'OLBI10',
    'Burnout (Oldenburg Burnout Inventory) x Sometimes I feel sickened by my\nwork tasks.': 'OLBI11',
    'Burnout (Oldenburg Burnout Inventory) x After my work, I usually feel worn\nout and weary.': 'OLBI12',
    'Burnout (Oldenburg Burnout Inventory) x This is the only type of work I can\nimagine myself doing.': 'OLBI13',
    'Burnout (Oldenburg Burnout Inventory) x Usually, I can manage the amount\nof my work well.': 'OLBI14',
    'Burnout (Oldenburg Burnout Inventory) x I feel more and more engaged in\nmy work.': 'OLBI15',
    'Burnout (Oldenburg Burnout Inventory) x When I work, I usually feel\nenergized.': 'OLBI16',
    'Burnout': 'Burnout',
    
    'Moral Distress': 'Futile_Surgery',
    
    'Moral distress x Medicolegal concerns': 'Moral_Distress_Rank_Medicolegal',
    'Moral distress x Surrogate pressure for\nsurgery': 'Moral_Distress_Rank_Surrogate_Surgery',
    'Moral distress x Advanced directives / dříve vyslovené přání': 'Moral_Distress_Rank_Advanced_directives',
    'Moral distress x Urge to rescue': 'Moral_Distress_Rank_Urge_to_rescue',
    
    'Moral distress x I have experienced\nmoral distress during the\nlast year.': 'Moral_Distress_Experience',
    'Moral distress x I have performed\noperations and worried\nthat they were not\naligned with the patient’s\nvalues and goals.': 'Moral_Distress_Goals_Discrepancy',
    
    'Moral Distress.1': 'Moral_Distress_TBI_goals_discrepancy',
    
    'Moral distress - frequency x Giving “false hope” to a patient or\nfamily.': 'Moral_Distress_1_frequency',
    'Moral distress - frequency x Perform surgery following the family’s\ninsistence to continue aggressive\ntreatment even though I believe it is\nnot in the best interest of the patient.': 'Moral_Distress_2_frequency',
    'Moral distress - frequency x Feel pressured to order or carry out\norders for what I consider to be\nunnecessary or inappropriate tests and\ntreatments': 'Moral_Distress_3_frequency',
    'Moral distress - frequency x Perform surgery for a person who is\nmost likely to die regardless of this\ntreatment when no one will make a\ndecision to withdraw it.': 'Moral_Distress_4_frequency',
    'Moral distress - frequency x Participate in care that I do not agree\nwith, but do so because of fears of\nlitigation.': 'Moral_Distress_5_frequency',
    'Moral distress - frequency x Be required to care for patients who\nhave unclear or inconsistent treatment\nplans or who lack goals of care.': 'Moral_Distress_6_frequency',
    'Moral distress - frequency x Performing an operation that I think is\nnot aligned with the patient’s values\nand goals.': 'Moral_Distress_7_frequency',
    'Moral distress - frequency x Feeling overwhelmed in hyper-intense\nconversations.': 'Moral_Distress_8_frequency',
    'Moral distress - intensity x Giving “false hope” to a patient or\nfamily.': 'Moral_Distress_1_intensity',
    'Moral distress - intensity x Perform surgery following the family’s\ninsistence to continue aggressive\ntreatment even though I believe it is\nnot in the best interest of the patient.': 'Moral_Distress_2_intensity',
    'Moral distress - intensity x Feel pressured to order or carry out\norders for what I consider to be\nunnecessary or inappropriate tests and\ntreatments': 'Moral_Distress_3_intensity',
    'Moral distress - intensity x Perform surgery for a person who is\nmost likely to die regardless of this\ntreatment when no one will make a\ndecision to withdraw it.': 'Moral_Distress_4_intensity',
    'Moral distress - intensity x Participate in care that I do not agree\nwith, but do so because of fears of\nlitigation.': 'Moral_Distress_5_intensity',
    'Moral distress - intensity x Be required to care for patients who\nhave unclear or inconsistent treatment\nplans or who lack goals of care.': 'Moral_Distress_6_intensity',
    'Moral distress - intensity x Performing an operation that I think is\nnot aligned with the patient’s values\nand goals.': 'Moral_Distress_7_intensity',
    'Moral distress - intensity x Feeling overwhelmed in hyper-intense\nconversations.': 'Moral_Distress_8_intensity',
    'Moral distress': 'Leaving_Position',
    
    'Communication Training': 'Communication_Training_Comfortability',
    'Communication Training.1': 'Communication_Training_1',
    'Communication Training.2': 'Communication_Training_2',
    'Communication Training.3': 'Communication_Training_3',
    'Communication Training.4': 'Communication_Training_4',
    'Communication Training x I have the necessary\nskills to discuss end of\nlife goals in\nneurosurgery patients.': 'Communication_Training_Skills',
    
    'Palliative Care': 'Palliative_Care_Availability',
    'Palliative care x Severe TBI ': 'Palliative_Care_TBI',
    'Palliative care x Recurrent GBM': 'Palliative_Care_GBM',
    'Palliative care x Widely metastatic disease': 'Palliative_Care_Metastatic',
    'Palliative care x I rarely consult palliative care': 'Palliative_Care_Rarely',
    'Palliative care x Other...': 'Palliative_Care_Other',
    'Palliative care x Patient likely to die during this admission': 'Palliative_Care_Reason1',
    'Palliative care x Difficult family dynamics': 'Palliative_Care_Reason2',
    'Palliative care x End of life discussion is needed': 'Palliative_Care_Reason3',
    'Palliative care x Patient’s/family’s request': 'Palliative_Care_Reason4',
    'Palliative care x Time constraints in hyperintense conversations': 'Palliative_Care_Reason5',
    'Palliative care x Lack of training in having hyperintense conversations': 'Palliative_Care_Reason6',
    'Palliative care x Other': 'Palliative_Care_Reason7',
    
    'Symptoms of depression: how often have you been bothered by the following over the past 2 weeks?': 'PHQ9_1_redundant',
    'Symtoms of depression: how often have you been bothered by the following over the past 2 weeks? x Little interest or pleasure in doing things?': 'PHQ9_1',
    'Symtoms of depression: how often have you been bothered by the following over the past 2 weeks? x Feeling down, depressed, or hopeless?': 'PHQ9_2',
    'Symtoms of depression: how often have you been bothered by the following over the past 2 weeks? x Trouble falling or staying asleep, or sleeping too much?': 'PHQ9_3',
    'Symtoms of depression: how often have you been bothered by the following over the past 2 weeks? x Feeling tired or having little energy?': 'PHQ9_4',
    'Symtoms of depression: how often have you been bothered by the following over the past 2 weeks? x Poor appetite or overeating?': 'PHQ9_5',
    'Symtoms of depression: how often have you been bothered by the following over the past 2 weeks? x Feeling bad about yourself — or that you are a failure or have let yourself or your family down?': 'PHQ9_6',
    'Symtoms of depression: how often have you been bothered by the following over the past 2 weeks? x Trouble concentrating on things, such as reading the newspaper or watching television?': 'PHQ9_7',
    'Symtoms of depression: how often have you been bothered by the following over the past 2 weeks? x Moving or speaking so slowly that other people could have noticed? Or so fidgety or restless that you have been moving a lot more than usual?': 'PHQ9_8',
    'Symtoms of depression: how often have you been bothered by the following over the past 2 weeks? x Thoughts that you would be better off dead, or thoughts of hurting yourself in some way?': 'PHQ9_9',
    
    'demographics': 'Demographics_position',
    'Demographics': 'Demographics_gender',
    'Demographics.1': 'Demographics_years_of_practise',
    'Demographics.2': 'Demographics_Ethnicity',
    'Demographics.3': 'Demographics_Religion',
    'Demographics.4': 'Demographics_On_Call',
    'Demographics.5': 'Demographics_Trauma_Center',
    'Demographics.6': 'Demographics_Comments',
}

df = df.rename(columns = metadata )

def getDateTime(row):
    date, time = row['date'], row['time']
    dt = " ".join([date, time])
    return datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")

df['datetime'] = df[['date', 'time']].apply(getDateTime, axis=1)


def parseDuration(d):
    hour, minutes, seconds = d.split(":")
    hour, minutes, seconds = int(hour), int(minutes), int(seconds)
    return 60 * hour + minutes + (seconds/60)

df['duration'] = df['duration'].apply(parseDuration)


df.head()

df['Demographics_position'].value_counts()

# ## Oldenburg Burnout Inventory (OLBI)
# https://wings.pages.ornl.gov/publications/oldenburg_burnout_inventory.pdf

def scoreOldenburg( response ):
    answers = {  'Strongly agree': 1, 'Agree': 2, 'Disagree': 3, 'Strongly\ndisagree': 4 }
    return answers[response.strip()]
    
def scoreOldenburgReversed ( response ):
    answers = {  'Strongly agree': 4, 'Agree': 3, 'Disagree': 2, 'Strongly\ndisagree': 1 }
    return answers[response.strip()]
    
df['OLBI1'] = df['OLBI1'].apply(scoreOldenburg)
df['OLBI2'] = df['OLBI2'].apply(scoreOldenburgReversed)
df['OLBI3'] = df['OLBI3'].apply(scoreOldenburgReversed)
df['OLBI4'] = df['OLBI4'].apply(scoreOldenburgReversed)
df['OLBI5'] = df['OLBI5'].apply(scoreOldenburg)
df['OLBI6'] = df['OLBI6'].apply(scoreOldenburgReversed)
df['OLBI7'] = df['OLBI7'].apply(scoreOldenburg)
df['OLBI8'] = df['OLBI8'].apply(scoreOldenburgReversed)
df['OLBI9'] = df['OLBI9'].apply(scoreOldenburgReversed)
df['OLBI10'] = df['OLBI10'].apply(scoreOldenburg)
df['OLBI11'] = df['OLBI11'].apply(scoreOldenburgReversed)
df['OLBI12'] = df['OLBI12'].apply(scoreOldenburgReversed)
df['OLBI13'] = df['OLBI13'].apply(scoreOldenburg)
df['OLBI14'] = df['OLBI14'].apply(scoreOldenburg)
df['OLBI15'] = df['OLBI15'].apply(scoreOldenburg)
df['OLBI16'] = df['OLBI16'].apply(scoreOldenburg)

# Sum scores:
df['OLBI-D'] = df['OLBI1'] + df['OLBI3'] + df['OLBI6'] + df['OLBI7'] + df['OLBI9'] + df['OLBI11'] + df['OLBI13'] + df['OLBI15']
df['OLBI-E'] = df['OLBI2'] + df['OLBI4'] + df['OLBI5'] + df['OLBI8'] + df['OLBI10'] + df['OLBI12'] + df['OLBI14'] + df['OLBI16']
df['OLBI']   = df['OLBI-D'] + df['OLBI-E']

# Mean scores:
def get_OLBI_D_mean(rows):
    return np.mean( [
        rows['OLBI1'],
        rows['OLBI3'],
        rows['OLBI6'],
        rows['OLBI7'],
        rows['OLBI9'],
        rows['OLBI11'],
        rows['OLBI13'],
        rows['OLBI15'],
    ] )

def get_OLBI_E_mean(rows):
    return np.mean( [
        rows['OLBI2'],
        rows['OLBI4'],
        rows['OLBI5'],
        rows['OLBI8'],
        rows['OLBI10'],
        rows['OLBI12'],
        rows['OLBI14'],
        rows['OLBI16'],
    ] )

def get_OLBI_mean(rows):
    return np.mean( [
        rows['OLBI1'],
        rows['OLBI2'],
        rows['OLBI3'],
        rows['OLBI4'],
        rows['OLBI5'],
        rows['OLBI6'],
        rows['OLBI7'],
        rows['OLBI8'],
        rows['OLBI9'],
        rows['OLBI10'],
        rows['OLBI11'],
        rows['OLBI12'],
        rows['OLBI13'],
        rows['OLBI14'],
        rows['OLBI15'],
        rows['OLBI16'],
    ] )

df['OLBI_D_mean'] = df.apply(get_OLBI_D_mean, axis = 1)
df['OLBI_E_mean'] = df.apply(get_OLBI_E_mean, axis = 1)
df['OLBI_mean']   = df.apply(get_OLBI_mean  , axis = 1)

def get_OLBI_result(rows):
    olbi_d, olbi_e = rows['OLBI_D_mean'], rows['OLBI_E_mean']
    disengagement, exhaustion = False, False
    
    if olbi_d >= 2.1:
        disengagement = True
    if olbi_e >= 2.25:
        exhaustion = True
        
    if disengagement and exhaustion:
        return "Burned out"
    elif disengagement or exhaustion:
        return "At risk"
    else:
        return "Not burned out"

df['OLBI_result'] = df[['OLBI_D_mean', 'OLBI_E_mean']].apply( get_OLBI_result, axis=1)

# ## Patient Health Questionnaire (PHQ-9)
# https://www2.gov.bc.ca/assets/gov/health/practitioner-pro/bc-guidelines/depression_patient_health_questionnaire.pdf

df['PHQ9_1'] = df['PHQ9_1'].replace({'More than the half of days': 'More than half the days'})

df.loc[ df['PHQ9_1_redundant'] != df['PHQ9_1'], ['PHQ9_1_redundant', 'PHQ9_1']]


def scorePHQ9( response ):
    answers = { 'Not at all': 0, 'Several days': 1, 'More than half the days': 2, 'More than the half of days': 2, 'Nearly every day': 3}
    return answers[response.strip()]


df['PHQ9_1'] = df['PHQ9_1'].apply(scorePHQ9)
df['PHQ9_2'] = df['PHQ9_2'].apply(scorePHQ9)
df['PHQ9_3'] = df['PHQ9_3'].apply(scorePHQ9)
df['PHQ9_4'] = df['PHQ9_4'].apply(scorePHQ9)
df['PHQ9_5'] = df['PHQ9_5'].apply(scorePHQ9)
df['PHQ9_6'] = df['PHQ9_6'].apply(scorePHQ9)
df['PHQ9_7'] = df['PHQ9_7'].apply(scorePHQ9)
df['PHQ9_8'] = df['PHQ9_8'].apply(scorePHQ9)
df['PHQ9_9'] = df['PHQ9_9'].apply(scorePHQ9)


df['PHQ9'] = df['PHQ9_1'] + df['PHQ9_2'] + df['PHQ9_3'] + df['PHQ9_4'] + df['PHQ9_5'] + df['PHQ9_6'] + df['PHQ9_7'] + df['PHQ9_9']


# ## Moral Distress

def scoreDistress( response ):
    answers = {
        'Frequency - 0\n(NEVER)': 0, 'Level of Distress - 0 (none)': 0,
        '1': 1,
        '2': 2,
        '3': 3,
        '4 (VERY FREQUENTLY)': 4, '4 (Very\ndistressing)': 4,
    }
    return answers[response.strip()]


for column in [ 'Moral_Distress_1_frequency', 'Moral_Distress_2_frequency', 'Moral_Distress_3_frequency',
        'Moral_Distress_4_frequency', 'Moral_Distress_5_frequency',  'Moral_Distress_6_frequency',
        'Moral_Distress_7_frequency', 'Moral_Distress_8_frequency',
        
        'Moral_Distress_1_intensity', 'Moral_Distress_2_intensity', 'Moral_Distress_3_intensity',
        'Moral_Distress_4_intensity', 'Moral_Distress_5_intensity', 'Moral_Distress_6_intensity',
        'Moral_Distress_7_intensity', 'Moral_Distress_8_intensity',]:
    df[column] = df[column].apply(scoreDistress)

df['Moral_Distress_Score_frequency'] = \
        df[ 'Moral_Distress_1_frequency'] + \
        df[ 'Moral_Distress_2_frequency'] + \
        df[ 'Moral_Distress_3_frequency'] + \
        df[ 'Moral_Distress_4_frequency'] + \
        df[ 'Moral_Distress_5_frequency'] + \
        df[ 'Moral_Distress_6_frequency'] + \
        df[ 'Moral_Distress_7_frequency'] + \
        df[ 'Moral_Distress_8_frequency']

df['Moral_Distress_Score_intensity'] = \
        df['Moral_Distress_1_intensity'] + \
        df['Moral_Distress_2_intensity'] + \
        df['Moral_Distress_3_intensity'] + \
        df['Moral_Distress_4_intensity'] + \
        df['Moral_Distress_5_intensity'] + \
        df['Moral_Distress_6_intensity'] + \
        df['Moral_Distress_7_intensity'] + \
        df['Moral_Distress_8_intensity']

df['Moral_Distress_Score'] = df['Moral_Distress_Score_frequency'] + df['Moral_Distress_Score_intensity']
df[['Moral_Distress_Score', 'Moral_Distress_Score_frequency', 'Moral_Distress_Score_intensity']].describe()


# ## Other variables

def rankMoralDistress( response ):
    answers = {'1 most important': 1, '2': 2, '3': 3, '4': 4}
    return answers[response.strip()]

for column in ['Moral_Distress_Rank_Medicolegal', 'Moral_Distress_Rank_Surrogate_Surgery',
        'Moral_Distress_Rank_Advanced_directives', 'Moral_Distress_Rank_Urge_to_rescue',]:
    df[column] = df[column].apply(rankMoralDistress)

df['Moral_Distress_Experience'] = df['Moral_Distress_Experience'].replace( {'Generally\ndisagree': 'Generally disagree' } )
df['Moral_Distress_Goals_Discrepancy'] = df['Moral_Distress_Goals_Discrepancy'].replace( {'Generally\ndisagree': 'Generally disagree' } )
df['Communication_Training_Skills'] = df['Communication_Training_Skills'].replace( {'Generally\ndisagree': 'Generally disagree' } )

df['Palliative_Care_Rarely'] = df['Palliative_Care_Rarely'].replace({'Ne': 'NO', 'Ano': 'YES'})
df['Palliative_Care_TBI'] = df['Palliative_Care_TBI'].replace({'Ne': 'NO', 'Ano': 'YES'})
df['Palliative_Care_GBM'] = df['Palliative_Care_GBM'].replace({'Ne': 'NO', 'Ano': 'YES'})
df['Palliative_Care_Metastatic'] = df['Palliative_Care_Metastatic'].replace({'Ne': 'NO', 'Ano': 'YES'})
df['Palliative_Care_Reason1'] = df['Palliative_Care_Reason1'].replace({'Ne': 'NO', 'Ano': 'YES'})
df['Palliative_Care_Reason2'] = df['Palliative_Care_Reason2'].replace({'Ne': 'NO', 'Ano': 'YES'})
df['Palliative_Care_Reason3'] = df['Palliative_Care_Reason3'].replace({'Ne': 'NO', 'Ano': 'YES'})
df['Palliative_Care_Reason4'] = df['Palliative_Care_Reason4'].replace({'Ne': 'NO', 'Ano': 'YES'})
df['Palliative_Care_Reason5'] = df['Palliative_Care_Reason5'].replace({'Ne': 'NO', 'Ano': 'YES'})
df['Palliative_Care_Reason6'] = df['Palliative_Care_Reason6'].replace({'Ne': 'NO', 'Ano': 'YES'})

df['Demographics_position'] = df['Demographics_position'].replace({"Professor of neurosurgery": "Attending neurosurgeon", "neurologist": "Resident"})

df = df[
    [
        'datetime', 'duration',
        
        'OLBI', 'OLBI-D', 'OLBI-E',
        'OLBI1', 'OLBI2', 'OLBI3', 'OLBI4', 'OLBI5', 'OLBI6', 'OLBI7', 'OLBI8', 'OLBI9',
        'OLBI10', 'OLBI11', 'OLBI12', 'OLBI13', 'OLBI14', 'OLBI15', 'OLBI16',
        'OLBI_D_mean', 'OLBI_E_mean', 'OLBI_mean', 'OLBI_result',
        'Burnout',
        
        'Futile_Surgery',
        
        'Moral_Distress_Rank_Medicolegal', 'Moral_Distress_Rank_Surrogate_Surgery',
        'Moral_Distress_Rank_Advanced_directives', 'Moral_Distress_Rank_Urge_to_rescue',
        
        'Moral_Distress_Experience', 'Moral_Distress_Goals_Discrepancy',
        
        'Moral_Distress_TBI_goals_discrepancy',
        
        'Moral_Distress_1_frequency', 'Moral_Distress_2_frequency', 'Moral_Distress_3_frequency',
        'Moral_Distress_4_frequency', 'Moral_Distress_5_frequency',  'Moral_Distress_6_frequency',
        'Moral_Distress_7_frequency', 'Moral_Distress_8_frequency',
        
        'Moral_Distress_1_intensity', 'Moral_Distress_2_intensity', 'Moral_Distress_3_intensity',
        'Moral_Distress_4_intensity', 'Moral_Distress_5_intensity', 'Moral_Distress_6_intensity',
        'Moral_Distress_7_intensity', 'Moral_Distress_8_intensity',
        'Moral_Distress_Score', 'Moral_Distress_Score_frequency', 'Moral_Distress_Score_intensity',
        
        'Leaving_Position',
       
        'Communication_Training_Comfortability',
        'Communication_Training_1', 'Communication_Training_2', 'Communication_Training_3', 'Communication_Training_4',
        'Communication_Training_Skills',
        
        
        'Palliative_Care_Availability', 'Palliative_Care_TBI', 'Palliative_Care_GBM', 'Palliative_Care_Metastatic',
        'Palliative_Care_Rarely', 'Palliative_Care_Other',
        
        'Palliative_Care_Reason1', 'Palliative_Care_Reason2', 'Palliative_Care_Reason3', 'Palliative_Care_Reason4',
        'Palliative_Care_Reason5', 'Palliative_Care_Reason6',  'Palliative_Care_Reason7',
        
        'PHQ9',
        'PHQ9_1', 'PHQ9_2', 'PHQ9_3', 'PHQ9_4', 'PHQ9_5', 'PHQ9_6', 'PHQ9_7', 'PHQ9_8', 'PHQ9_9',
       
        'Demographics_position', 'Demographics_gender', 'Demographics_years_of_practise', 'Demographics_Ethnicity',
        'Demographics_Religion', 'Demographics_On_Call', 'Demographics_Trauma_Center', 'Demographics_Comments'
    ]
]

df['Palliative_Care_Metastatic'].value_counts()
df['Demographics_position'].value_counts()
df.info()
df.to_csv("palliative_neurosurgery_survey.csv", index=False)
#df.to_parquet("palliative_neurosurgery_survey.parquet")
