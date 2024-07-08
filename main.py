import agents.agent_cases.mdt as mdt
import agents.agent_cases.pcp as pcp
import agents.agents_helper.chw as chw
import agents.agents_helper.complexity as complexity

# LLM Config List
config_list = {}

# Get input from the user
name = input("Hello, what is your name?")
src_lang = input("What language do you speak?")
region = input("Where are you from?")
query = input("What symptoms is your patient facing?")

# Initialize CHW and Complexity objects
chw_agent = chw.AgentCHW(name, src_lang, region)
complexity_agent = complexity.AgentAnalyzeComplexity(config_list)

# Undergo Complexity Analysis to determine case (ie. low -> PCP, medium -> MDT, high -> RHC)
analysis_results = complexity_agent.agent.generate_reply(
    messages=[{"content": f"Symptoms and Condition Description: {query}", "role": "user"}]
)

# Match case to generate the proper diagnosis depending on the complexity
reply = ""

match analysis_results:
    case "low":
        pcp_agent = pcp.AgentPCP(config_list, src_lang)
        reply = pcp_agent.simplify_reply(pcp_agent.generate_reply(query))
    case "medium":
        mdt_group = mdt.MDTAgentGroup(config_list, src_lang)
        reply = mdt_group.simplify_reply(mdt_group.generate_reply(query))
    case "high":
        reply = "Please seek help from a Regional Healthcare Center (RHC)."

print(reply)