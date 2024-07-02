"""
This agent is used by the human CHW or patient to keep them in-the-loop in a conversational manner.
"""
from autogen import UserProxyAgent

class AgentCHW:
    def __init__(self, name: str, src_lang: str, region: str):
        # Create a UserProxyAgent object representing the CHW agent.
        self.agent = UserProxyAgent(
            name = "chw",
            human_input_mode="ALWAYS"
            # TODO: SEE IF MORE THINGS NEED TO BE ADDED TO THIS DEFINITION
        )
        self.name = name
        self.src_lang = src_lang
        self.region = region