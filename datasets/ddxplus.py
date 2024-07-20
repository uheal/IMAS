import pandas as pd
import ast

def ddxdataparser(condition_path, evidence_path, patient_path):
    release_conds = pd.read_json(condition_path)
    release_evid = pd.read_json(evidence_path)
    train_patients = pd.read_csv(patient_path)
    return release_conds, release_evid, train_patients

def get_values_meaning(release_evid):
    values_meaning_list = []
    possible_values_list = []
    for col in release_evid.columns:
        values_meaning_list.append(release_evid[col]['value_meaning'])
        possible_values_list.append(release_evid[col]['possible-values'])
    return values_meaning_list, possible_values_list


def important_values(train_patients, release_conds, release_evid):
    row_values = {}
    for index, rows in train_patients.iterrows():
        evidences = train_patients.iloc[index]['EVIDENCES']
        diagnoses = train_patients.iloc[index]['DIFFERENTIAL_DIAGNOSIS']
        pathology = train_patients.iloc[index]['PATHOLOGY']
        age = train_patients.iloc[index]['AGE']
        sex = train_patients.iloc[index]['SEX']

        list_diagnoses = ast.literal_eval(diagnoses)
        likely_diagnosis = list_diagnoses[0][0]

        diagnosis_en = release_conds[likely_diagnosis]['cond-name-eng']

        list_evidences = ast.literal_eval(evidences)
        questions_list = []
        for evidence in list_evidences:
            if evidence in release_evid.columns:
                question = release_evid[evidence]['question_en']
                questions_list.append(question)
        pathology_en = release_conds[pathology]['cond-name-eng']
        row_values[index] = {'question_list': questions_list, 'likely_diagnosis': diagnosis_en, 'pathology': pathology_en, 'age': age, 'sex': sex}
    return row_values

def row_values_parser(row_values):
    EMR_string = []
    for index in row_values:
        quests = row_values[index]['question_list']
        diag = row_values[index]['likely_diagnosis']
        path = row_values[index]['pathology']
        age = row_values[index]['age']
        se = row_values[index]['sex']

        questions_total = ", ".join(quests)
        EMR_string.append("Patient No: " + str(index) + " ,questions doctor asked patient: " + questions_total + " ,age of patient: " + str(age) + " ,sex of patient: " + se + "\n")
    return EMR_string
