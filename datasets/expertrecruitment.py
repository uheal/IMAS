from autogen import AssistantAgent
from ddxplus import ddxdataparser, important_values, row_values_parser
from variousstuff import batch_list

llm_config = {}

cond_path = 'health_data/release_conditions.json'
evid_path = 'ealth_data/release_evidences.json'
patient_path = 'health_data/release_test_patients.csv'

release_conds, release_evid, train_patients = ddxdataparser(cond_path, evid_path, patient_path)
row_values = important_values(train_patients, release_conds, release_evid)
health_records = row_values_parser(row_values)
batches = batch_list(health_records, 500)

first_couple_batches = batches[:7]
summary_list = []
for batch in first_couple_batches:
    recs = ", ".join(batch)
    objective= f'''
    Please give a complexity rating of diagnosing to every single patient
    within the health records:
    Health Records: {recs}
    '''

    complexity_chooser = AssistantAgent(
        name = "Complexity Chooser",
        system_message = "You are an individual who chooses the complexity of the task"
        "given some description about the issues that the patient was suffering from."
        "There are two possible complexities: low and medium."
        "Be sure to assign a complexity rating to every single patient."
        "Please keep the symptoms within your response."
        "For example: **Patient No. 0**: Diagnosing heartburn or GERD-like symptoms. **Medium Complexity**",
        llm_config=llm_config,
    )

    complexity_ratings = complexity_chooser.generate_reply(messages=[{"content": objective, "role": "user"}])

    objective = f"""
    Please assign the correct health experts to each patient according to the respective complexity:
    Records: {complexity_ratings}
    """

    recruitment_agent = AssistantAgent(
        name = "Recruiter",
        system_message = "You are a medical expert that is responsible for assigning specific health care specialists to a patient"
        "given their patient record. For the low complexity case, please assign a primary care provider to the patient and."
        "no other experts. The primary care provider should be the only expert assigned for the low complexity cases."
        "For the medium case, please generate a multi-disciplinary team consisting of different experts."
        "For example, if a patient record is assigned low complexity, it should only be assigned the primary care provider."
        "A patient having the medium case, for example, a patient who has issues with heart and lung problems, should be assigned a multi-disciplinary team"
        "consisting of a cardiologist or pulmonologist. Please ensure that the selections are appropriate for the specific patient."
        "Additionally, you should express it as Patient No. () - Complexity - Experts. Finally, do not assign general health specialists and primary care providers within the"
        "multi-disciplinary team. Don't be extremely specific but also don't be too general.",
        llm_config=llm_config,
    )

    recruiter_validator = AssistantAgent(
        name = "Recruiter Validator",
        system_message="You are an individual that validates the choice of experts assigned to"
        "help diagnose a patient's condition. Please suggest feedback for the choices made such that the Recruiter can improve upon"
        "the choices made.",
        llm_config=llm_config,
    )
    
    assignment_reviewer = AssistantAgent(
        name = "Assignment Reviewer",
        system_message = "You are a reviewer of various health conditions."
        "Your task is to ensure that the right correct experts is assigned for"
        "each complexity level. You need to ensure that patients who are assigned a low"
        "complexity will be assigned to a primary care specialist. The same applies with medium"
        "complexity cases being assigned the multi-disciplinary team of experts. If the provided diagnosis does not reflect this,"
        "then please mention this within your review such that the feedback can be considered. Additionally, patients"
        "with medium complexity should not recieve the primary care provider or similar general health specialists.",
        llm_config=llm_config,
    )
    
    expert_checker = AssistantAgent(
        name = "Expert Checker",
        system_message="You are a medical expert that specializes in many different areas."
        "Your task is to check the experts assigned under the patients that have a multi-disciplinary team"
        "looking after them. If any choice of expert does not fit the supposed task, you should present a better alternative"
        "and explain as to why the other alternative is better such that the feedback can be implemented. Do not make up experts!"
        "Additionally, if the assignments you recieve have a fake expert, that should be pointed out within the feedback. Finally,"
        "ensure that your choices are the best possible choices. ",
        llm_config=llm_config,
        
    )
    
    def med_reflect(recipient, messages, sender, config):
        return f""" Please review the following content and provide the relevant feedback {recipient.chat_messages_for_summary(sender)[-1]['content']}
         """
    review_chats = []
    for agent in [assignment_reviewer, expert_checker]:
        review_chat = {
            "recipient": agent,
            "message": med_reflect,
            "summary_method": "reflection_with_llm",
            "max_turns": 1
        }
        review_chats.append(review_chat)
    
    recruiter_validator.register_nested_chats(
        review_chats,
        trigger=recruitment_agent,
    )
    
    
    res = recruiter_validator.initiate_chat(
        recipient=recruitment_agent,
        message=objective,
        max_turns=4
    )
    
    summary_list.append(res.summary)
    
summary_batches = batch_list(summary_list, 10)
calc_batches = []
for batch in summary_batches:
    prompt = f"""
    Within the following list, please mention how many of each type of expert is present    
    within the following generated health records:
    {batch}
    """
    counter = AssistantAgent(
        name = "counter",
        system_message = "You are an accountant of health records. Please figure out"
        "the amount of each type of expert there is in the health records. You should find the patient"
        "information which contains the experts under the Patient No's. Please keep it within this format. Please"
        "only consider the patient records that have been assigned a multi-disciplinary team."
        "### Summary Counts:" 
        "- **Gastroenterologist**: 4",
        llm_config=llm_config,
    )

    res = counter.generate_reply(messages = [{"content": prompt, "role": "user"}])
    calc_batches.append(res)

prompt = f"""
Combine the counts of each specialist within the following list
into one final count for each specialist:
{calc_batches}
"""

second_counter = AssistantAgent(
    name = "Second Counter",
    system_message = "You are an individual who counts the amount of specialists within a dataset."
    "Within the provided information, you combine the counts of the specialists. For example, if one series of"
    "records includes a count of 4 Gastroenterologists assigned and another record includes a count of 6 Gastroenterologists,"
    "you would combine the counts such that you would have 10 Gastroenterologists. Report your finding as:"
    "### Summary Counts:" 
    "- **Gastroenterologist**: 4",
    llm_config=llm_config,
)

final_res = second_counter.generate_reply(messages = [{"content": prompt, "role": "user"}])
