"""
This agent is used to determine the complexity of a specific question. There are three possible cases for this.

1.) Low complexity - Lower complexity cases will be handled by a single Primary Care Provider (PCP) agent.
2.) Medium complexity - Medium complexity cases will be handled by a Multidisciplinary Team (MDT) of agents
3.) High complexity - High complexity cases will not be handled by this system.

"""
from autogen import AssistantAgent

class AgentAnalyzeComplexity:
    def __init__(self, config_list: dict):
        self.system_prompt: str = "" # TODO: FINISH SYSTEM PROMPT FOR AGENT

        # Create an AssistantAgent object representing the complexity agent.
        self.agent = AssistantAgent(
            name = "complexity",
            system_message = self.system_prompt,
            llm_config=config_list,
            human_input_mode="NEVER"
            # TODO: DECIDE ON TERMINATION METHOD
        )