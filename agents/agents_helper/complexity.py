"""
This agent is used to determine the complexity of a specific question. There are three possible cases for this.

1.) Low complexity - Lower complexity cases will be handled by a single Primary Care Provider (PCP) agent.
2.) Medium complexity - Medium complexity cases will be handled by a Multidisciplinary Team (MDT) of agents
3.) High complexity - High complexity cases will not be handled by this system.

"""
from autogen import AssistantAgent


class AgentAnalyzeComplexity:
    def __init__(self, config_list: dict):
        self.system_prompt: str = "You are an agent tasked with determining the complexity of a medical case based on the information provided. Your response should be concise and limited to one word indicating the complexity level: \"low,\" \"medium,\" or \"high.\" Do not capitalize any of the words. For cases deemed \"low,\" the patient should be directed to a Primary Care Provider (PCP). These typically are cases involving very little difficulty in diagnosing nor does it require much technology to figure out the source of the problem For cases deemed \"medium,\" the patient should be directed to a Multidisciplinary Team (MDT). These typically are cases that are much more nuanced and can't be deduced by a single person. They require a large team and collaborative discussion to diagnose For cases deemed \"high,\" the patient or Community Health Worker should consult a Regional Healthcare Center (RHC). In this case, an even larger team is required to diagnose the issue. In addition, typically highly technical skills and knowledge is required to diagnose, like surgeries Please analyze the provided information and respond with one of the following words based on the complexity of the case: \"low,\" \"medium,\" or \"high.\""

        # Create an AssistantAgent object representing the complexity agent.
        self.agent = AssistantAgent(
            name = "complexity",
            system_message = self.system_prompt,
            llm_config=config_list,
            human_input_mode="NEVER"
        )