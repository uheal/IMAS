"""
This agent is a conversational agent that provides feedback to the Primary Care Provider or Moderator of the Multidisciplinary Team's 
responses in order to simplify them for rural areas. Attempts to remove highly technical words and content from the responses. 
"""
from autogen import AssistantAgent

class AgentSimplify:
    def __init__(self, config_list: dict):
        self.system_prompt: str = "" # TODO: FINISH SYSTEM PROMPT FOR AGENT

        # Create an AssistantAgent object representing the simplification agent.
        self.agent = AssistantAgent(
            name = "simplify",
            system_message = self.system_prompt,
            llm_config=config_list,
            human_input_mode="NEVER"
            # TODO: DECIDE ON TERMINATION METHOD
        )