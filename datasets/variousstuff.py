def batch_list(lst, num_batches):
    # Calculate the size of each batch
    n = len(lst)
    batch_size = n // num_batches
    remainder = n % num_batches
    
    batches = []
    start = 0
    
    for i in range(num_batches):
        # Adjust batch size to account for remainder
        end = start + batch_size + (1 if i < remainder else 0)
        batches.append(lst[start:end])
        start = end
    
    return batches


def nested_chat_initiation(validator_agent, list_of_nested_agents, trigger):
    def med_reflect(recipient, messages, sender, config):
        return f"""
    Please review the following content and provide the relevant feedback
    {recipient.chat_messages_for_summary(sender)[-1]['content']}
    """
    review_chats = []
    for agent in list_of_nested_agents:
        review_chat = {
            "recipient": agent,
            "message": med_reflect,
            "summary_method": "reflection_with_llm",
            "max_turns": 1
        }
        review_chats.append(review_chat)
    validator_agent.register_nested_chats(
        review_chats,
        trigger=trigger,
    )
