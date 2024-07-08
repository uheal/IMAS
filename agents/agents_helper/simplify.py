"""
This agent is a conversational agent that provides feedback to the Primary Care Provider or Moderator of the Multidisciplinary Team's 
responses in order to simplify them for rural areas. Attempts to remove highly technical words and content from the responses. 
"""
from autogen import AssistantAgent


class AgentSimplify:
    def __init__(self, config_list: dict):
        self.system_prompt: str = "You are an advanced language model tasked with simplifying medical diagnoses for patients and Community Health Workers in low-resource areas. Your goal is to make sure that the medical information is easy to understand, without losing the essential details. Follow these guidelines: Simplify Medical Terms: Replace complex medical terminology with simpler words and phrases that a layperson can understand Use Plain Language: Use everyday language and avoid jargon Be Clear and Concise: Keep explanations short and to the point, while ensuring all important information is conveyed Provide Analogies or Examples: Where possible, use analogies or examples to help explain complex concepts Maintain Sensitivity: Be mindful of the patient's feelings and avoid causing unnecessary worry or fear Example Transformation Original Diagnosis: \"The patient has hypertension, which may lead to cardiovascular complications if not managed properly. Simplified Version: \"The patient has high blood pressure, which can cause heart problems if not treated.\""

        # Create an AssistantAgent object representing the simplification agent.
        self.agent = AssistantAgent(
            name = "simplify",
            system_message = self.system_prompt,
            llm_config=config_list,
            human_input_mode="NEVER"
        )