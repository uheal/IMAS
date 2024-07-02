"""
This is the Primary Care Provider (PCP) agent. It is used in low complexity medical cases to answer medical questions.
"""
from autogen import AssistantAgent
from agents_helper.simplify import AgentSimplify

class AgentPCP:
    def __init__(self, config_list: dict, src_lang: str):
        self.system_prompt: str = "" # TODO: FINISH SYSTEM PROMPT FOR AGENT
        self.src_lang = src_lang

        # Create an AssistantAgent object representing the PCP agent.
        self.agent = AssistantAgent(
            name = "pcp",
            system_message = self.system_prompt,
            llm_config=config_list,
            human_input_mode="NEVER"
            # TODO: DECIDE ON TERMINATION METHOD
        )

    # TODO: Function for translating a string from src lang to target lang
    def translate(self, message: str, src: str, target: str):
        pass 

    # Function for generating reply for a given query. Returns a string, which is the english reply.
    def generate_reply(self, query: str) -> str:
        # Translate to english
        eng_query = self.translate(query, src=self.src_lang, target="eng")

        # Generate reply (answer to the patient/CHW's question)
        return self.agent.generate_reply(
            messages=[{"content": eng_query, "role": "user"}]
        )
    
    # Function for chatting with the simplification agent. Returns a string, which is the simplified english reply
    def simplify_reply(self, response: str) -> str:
        # Simplification agent
        simplifier: AgentSimplify = AgentSimplify(self.config_list)
  
        # Agentic chat between PCP agent and simplification agent
        chat_result = simplifier.agent.initiate_chat(
            recipient= self.agent,
            message= f"PCP Health Worker Agent Response: {response}"
            # TODO: DECIDE ON TERMINATION METHOD
        )

        # TODO: Extract the response, translate, and return