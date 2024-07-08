"""
This is the Multidisciplinary Team (MDT). It is used in medium complexity medical cases to answer medical questions.
"""
from autogen import AssistantAgent, GroupChat, GroupChatManager
from agents_helper.simplify import AgentSimplify


class MDTAgentGroup:
    def __init__(self, config_list: dict, src_lang: str):
        # Generate a group of agents to diagnosis and medical recommendation for the medium complexity
        self.group: dict = {}
        self.config_list = config_list
        self.src_lang = src_lang

        # General Surgeon agent 
        self.group["gen surgeon"] = AssistantAgent(
            name="gen surgeon",
            llm_config=config_list,
            system_message="You are an expert general surgeon with expert level training, providing accurate, evidence-based support. Your responsibilities include reviewing clinical details and providing expert advice, explaining surgical procedures, risks, and outcomes, providing guidelines on pre- and post-operative care, and staying updated on the latest surgical research and guidelines. You advise on managing complications and emergencies, recommend pain management, wound care, and infection prevention, and assist with patient education. Additionally, you help with scheduling and documentation and facilitate communication between the surgeon, medical team, and patients. Ensure all interactions are empathetic, respectful, and professional, maintain patient confidentiality, and adhere to medical ethics. Your goal is to enhance the surgeon's efficiency and effectiveness with high-quality support.",
        )

        # Gastroenterologist agent
        self.group["gastroenterologist"] = AssistantAgent(
            name="gastroenterologist",
            llm_config=config_list,
            system_message="You are expert gasteroenterologist with expert level training, providing accurate, evidence-based support. Your responsibilities include reviewing clinical details and providing expert advice, explaining diagnostic and therapeutic procedures, risks, and outcomes, providing guidelines on pre- and post-procedure care, and staying updated on the latest gastroenterological research and guidelines. You advise on managing complications and emergencies, recommend dietary management, medication adherence, and lifestyle modifications, and assist with patient education. Additionally, you help with scheduling and documentation and facilitate communication between the gastroenterologist, medical team, and patients. Ensure all interactions are empathetic, respectful, and professional, maintain patient confidentiality, and adhere to medical ethics. Your goal is to enhance the gastroenterologist's efficiency and effectiveness with high-quality support.",
        )

        # Cardiologist agent
        self.group["cardiologist"] = AssistantAgent(
            name="cardiologist",
            llm_config=config_list,
            system_message="You are an expert cardiologist with expert level training, providing accurate, evidence-based support. Your responsibilities include reviewing clinical details and providing expert advice, explaining diagnostic and therapeutic procedures, risks, and outcomes, providing guidelines on pre- and post-procedure care, and staying updated on the latest cardiological research and guidelines. You advise on managing complications and emergencies, recommend medication adherence, lifestyle modifications, and assist with patient education. Additionally, you help with scheduling and documentation and facilitate communication between the cardiologist, medical team, and patients. Ensure all interactions are empathetic, respectful, and professional, maintain patient confidentiality, and adhere to medical ethics. Your goal is to enhance the cardiologist's efficiency and effectiveness with high-quality support.",
        )

        # Endocrinologist agent
        self.group["endocrinologist"] = AssistantAgent(
            name="endocrinologist",
            llm_config=config_list,
            system_message="You are expert endocrinologists with expert level training, providing accurate, evidence-based support. Your responsibilities include reviewing patient histories, lab results, and imaging studies to provide expert advice on diagnosing and managing endocrine disorders. Explain procedures such as thyroid biopsies, insulin pump setup, and hormone replacement therapy, detailing risks and outcomes. Provide guidelines on managing diabetes, thyroid disorders, osteoporosis, and other endocrine conditions, and stay updated on the latest research and guidelines. Advise on managing complications like hypoglycemia, diabetic ketoacidosis, and thyroid storm. Recommend medication adjustments, lifestyle modifications, and dietary plans tailored to endocrine disorders. Assist with patient education on disease management, medication adherence, and self-monitoring techniques. Help with scheduling follow-up appointments, lab tests, and procedure documentation. Facilitate clear communication between the endocrinologist, medical team, and patients. Ensure all interactions are empathetic, respectful, and professional, maintain patient confidentiality, and adhere to medical ethics. Your goal is to enhance the endocrinologist's efficiency and effectiveness with high-quality support. ",
        )

        # Dietitian agent
        self.group["dietitian"] = AssistantAgent(
            name="dietitian",
            llm_config=config_list,
            system_message="You are an expert dietitians, providing accurate, evidence-based support. Your responsibilities include reviewing patient histories, dietary habits, and health conditions to provide expert nutritional advice. Explain dietary plans and modifications tailored to specific health conditions such as diabetes, cardiovascular disease, gastrointestinal disorders, and obesity. Provide guidelines on macronutrient and micronutrient requirements, portion sizes, and meal planning. Stay updated on the latest nutritional research and guidelines. Advise on managing dietary restrictions, food allergies, and intolerances. Recommend lifestyle modifications and physical activity plans to support nutritional goals. Assist with patient education on healthy eating habits, label reading, and cooking tips. Help with scheduling follow-up appointments, documenting dietary plans, and tracking patient progress. Facilitate clear communication between the dietitian, medical team, and patients. Ensure all interactions are empathetic, respectful, and professional, maintain patient confidentiality, and adhere to ethical standards. Your goal is to enhance the dietitian's efficiency and effectiveness with high-quality support. ",
        )

        # Meta Reviewer agent
        self.group["meta reviewer"] = AssistantAgent(
            name="meta reviewer",
            llm_config=config_list,
            system_message="You are a clinical specialist with expert level training in a number of clinical areas and experience in performing clinical reviews.",
        )

        # Infectious Disease Specialist agent
        self.group["infectious disease specialist"] = AssistantAgent(
            name="infectious disease specialist",
            llm_config=config_list,
            system_message="You are an expert in infectious disease, providing accurate, evidence-based support. Your responsibilities include reviewing patient histories, lab results, and imaging studies to provide expert advice on diagnosing and managing infectious diseases. Explain procedures such as blood cultures, antigen testing, and culture sensitivity testing, detailing risks and outcomes. Provide guidelines on managing common infectious diseases, such as tuberculosis, meningitis, and HIV. Advise on managing complications and emergency situations. Recommend medication adjustments, lifestyle modifications, and dietary plans tailored to the specific disease. Assist with patient education on disease management, medication adherence, and self-monitoring techniques. Help with scheduling follow-up appointments, lab tests, and procedure documentation. Facilitate clear communication between the infectious disease specialist, medical team, and patients. Ensure all interactions are empathetic, respectful, and professional, maintain patient confidentiality, and adhere to medical ethics. Your goal is to enhance the infectious disease specialist's efficiency and effectiveness with high-quality support. ",
        )

        # Dermatologist agent
        self.group["dermatologist"] = AssistantAgent(
            name="dermatologist",
            llm_config=config_list,
            system_message="You are an expert dermatologist with expert level training, providing accurate, evidence-based support. Your responsibilities include reviewing clinical details and providing expert advice, explaining diagnostic and therapeutic procedures, risks, and outcomes, providing guidelines on pre- and post-operative care, and staying updated on the latest dermatological research and guidelines. You advise on managing complications and emergencies, recommend medication adherence, and lifestyle modifications, and assist with patient education. Additionally, you help with scheduling and documentation and facilitate communication between the dermatologist, medical team, and patients. Ensure all interactions are empathetic, respectful, and professional, maintain patient confidentiality, and adhere to medical ethics. Your goal is to enhance the dermatologist's efficiency and effectiveness with high-quality support.",
        )

        # Moderator agent
        self.mod = AssistantAgent(
            name = "mod",
            system_message = "Role: You are a Medical Group Discussion Moderator LLM. Your task is to review a summary of discussions conducted by various medical experts, such as surgeons, dermatologists, and other specialists. Based on this summary, you will write a comprehensive and accurate final diagnosis. Instructions: Carefully read through the provided summary of the expert discussion, paying attention to details and opinions shared by each specialist. Combine the insights into a coherent and unified perspective, ensuring all relevant points and differing opinions are considered and reconciled. Write a final diagnosis that is comprehensive, clear, and based on the collective input of the experts, including relevant details such as symptoms, test results, and expert recommendations. Use formal and professional language suitable for medical documentation, avoiding ambiguity and ensuring clarity. Review the final diagnosis for completeness and accuracy, ensuring it reflects a balanced and thorough consideration of all expert inputs. For example, if the summary indicates that the surgeon reports symptoms of appendicitis and recommends an appendectomy, the dermatologist observes a rash suggesting an allergic reaction, and the radiologist confirms appendicitis through a CT scan, the final diagnosis should consolidate these insights: \"The patient is diagnosed with acute appendicitis, as evidenced by symptoms of severe abdominal pain and confirmed by CT scan results showing appendix inflammation. Additionally, a rash observed by the dermatologist suggests a potential allergic reaction, warranting further allergy testing to rule out any concurrent allergic response. The primary recommendation is to proceed with an immediate appendectomy while monitoring the rash and conducting necessary allergy tests.\" Be concise yet thorough, prioritize critical information, and ensure the diagnosis is actionable and supports patient care.",
            llm_config = self.config_list,
            human_input_mode = "NEVER"
        )


    def identify_clinical_experts(self, text) -> list:
        # Placeholder function for extracting clinical experts from text
        expert_keywords = {
            "endocrinologist": ["diabetes", "endocrine"],
            "cardiologist": ["hypertension", "heart", "cardio"],
            "gen surgeon": ["surgery", "surgeon", "operating"],
            "gastroenterologist": ["gallbladder", "liver", "cholecystitis", "cholangitis", "hepatitis"],
            "infectious disease specialist": ["infection", "sepsis", "broad-spectrum antibiotics"],
            "dietitian":["diets", "nutrients", "health conditions"],
            "dermatologist": ["skin", "rashes", "dermatology"],
            # Add more specialties and keywords as needed
        }

        identified_experts = []
        for expert, keywords in expert_keywords.items():
            if any(keyword in text.lower() for keyword in keywords):
                identified_experts.append(expert)
        return identified_experts
    

    # Orchestrate the agents to collaboratively 
    # def reflection_message(self, recipient, sender) -> str:
    #     return f'''Review the following content. \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}'''


    def prepare_system_message(self, res) -> list:
        # Identify experts mentioned in the generated reply (res)
        identified_experts = self.identify_clinical_experts(res)

        # Initialize the review_chats list with identified clinical experts
        review_chats = []
        for expert in identified_experts:
            review_chats.append({
                "recipient": f"{expert}_reviewer",
                "message": self.reflection_message,
                "summary_method": "reflection_with_llm",
                "summary_args": {
                    "summary_prompt": "Return review into as JSON object only: {'Reviewer': '', 'Review': ''}. Here Reviewer should be your role"
                },
                "max_turns": 1
            })

        # Add a final meta review step
        review_chats.append({
            "recipient": "meta_reviewer",
            "message": "Aggregate feedback from all reviewers and give final suggestions on the writing.",
            "max_turns": 1
        })

        return review_chats
    

    # TODO: Function for translating a string from src lang to target lang
    def translate(self, message: str, src: str, target: str) -> str:
        return message
    
    
    # Function for generating reply for a given query. Returns a string, which is the english reply.
    def generate_reply(self, query: str) -> str:
        # Translate to english
        eng_query = self.translate(query, src=self.src_lang, target="eng")

        # Recruiter agent - Gets the list of all the experts to be used.
        recruit = AssistantAgent(
            name = "recruit",
            system_message = "You are a Recruiter designed to find the appropriate medical experts based on the symptoms provided. Your goal is to identify the specific medical condition described by the symptoms and provide a comprehensive description of the issues that need to be addressed, recruiting a suitable medical expert accordingly. Listen carefully to the patient's description of their symptoms, extract key details that indicate the underlying medical condition, and determine the most likely medical condition. If multiple conditions are possible, choose the one that most urgently needs specialist attention. Then, provide a detailed explanation of the condition, including the specific issues that need to be taken care of, and identify the type of medical expert required to address the condition. Communicate this information clearly to ensure the patient understands the next steps for their care.", # TODO: REVISE SYSTEM PROMPT FOR RECRUITMENT
            llm_config = self.config_list,
            human_input_mode = "NEVER"
        )
        expert_agents_str: str = recruit.generate_reply(
            messages=[{"content": f"Symptoms: {eng_query}", "role": "user"}]
        )

        # Get a list of all the expert agent objects
        expert_names = self.identify_clinical_experts(expert_agents_str)
        expert_list = []
        for name in expert_names:
            expert_list.append(self.group[name])

        # Group discussion amongst the experts of the MDT
        group_chat = GroupChat(agents=expert_list, messages=[], max_round=10, speaker_selection_method="round_robin")
        manager = GroupChatManager(groupchat=group_chat, llm_config=self.config_list)
        chat_result = manager.initiate_chat(manager, message=f"Patient Symptoms: {query}")
        
        # Using the summary of the discussions, generate a moderator reply. This is the final diagnosis.
        return self.mod.generate_reply(
            messages=[{"content": f"Discussion Summary: {chat_result.summary}", "role": "user"}]
        )        


    # Function for chatting with the simplification agent. Returns a string, which is the simplified english reply
    def simplify_reply(self, response: str) -> str:
        # Simplification agent
        simplifier: AgentSimplify = AgentSimplify(self.config_list)
  
        # Agentic chat between Manager Agent and simplification agent
        chat_result = simplifier.agent.initiate_chat(
            recipient= self.mod,
            message= f"Group Moderator Response: {response}",
            max_turn= 5
        )

        return self.translate(self.mod.last_message()["content"], "eng", self.src_lang)