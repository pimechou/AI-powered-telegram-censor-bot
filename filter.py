from openai import OpenAI
import json

def filter(type, message):
    with open('config/config.json','r') as f:
        data = json.load(f)
    client = OpenAI(
        api_key=data["OpenAI_API_key"]
    )
    if type <= 2:
        response = client.responses.create(
            model=data["GPT-model"], 
            instructions="""Classify the input sentence as either offensive/harmful or not. Analyze the sentence content, reasoning step-by-step about whether it contains offensive, abusive, derogatory, or harmful language, including slurs, insults, or explicit attacks towards individuals or groups, or incites harm. Only after reasoning internally, assign a label: output 1 if the sentence is offensive or harmful, otherwise output 0. Output only the single digit (either 1 or 0) and nothing else.

                - Before producing the output, reason internally about the sentence’s content and context to determine whether it is offensive or harmful.
                - When determining whether a sentence qualifies as offensive or harmful, consider slurs, explicit attacks, hate speech, incitements to violence, or derogatory language depending on the context.
                - Do not provide any explanation, justification, or additional text—output only the digit label (“1” or “0”).
                - Output format: Only the digit 1 or 0 on a single line, with no other text or explanation.

                Examples:
                - Input: "You are a stupid idiot."
                - (Reasoning: The sentence contains a personal insult.)
                - Output: 1

                - Input: "I like sunny weather."
                - (Reasoning: The sentence expresses a neutral opinion without harmful language.)
                - Output: 0

                - Input: "That group of people is disgusting."
                - (Reasoning: The sentence uses derogatory language towards a group.)
                - Output: 1

                - Input: "Let's meet at noon."
                - (Reasoning: The sentence contains no offensive language.)
                - Output: 0

                (Reminder: The goal is to classify whether an input sentence is offensive/harmful or not, outputting only 1 or 0 as instructed.)""",
            
            input=message,
        )
    
    else:
        response = client.responses.create(
        model=data["GPT-model"], 
        instructions="""Censor any offensive or harmful words in the input sentence by replacing each letter in such words with an asterisk (*), but only if the overall meaning or intent of the sentence is objectively offensive, threatening, discriminatory, or harmful. If the sentence contains words that are typically considered offensive, but the meaning or intent of the sentence is not harmful, offensive, or negative, do not censor those words. Do not censor mild language, slang, innocuous terms, or words in neutral, positive, or literal contexts. Return the edited sentence only—exclude any explanations, reasoning, or extra output.
            - Censor words using asterisks (one per letter) only when used to express harmful, offensive, threatening, or discriminatory meanings.
            - If a typically offensive word is used in a non-harmful, neutral, or positive sense, do NOT censor it.
            - Leave non-offensive words and innocuous uses unchanged.
            - If the sentence is not offensive or harmful given its total meaning, return it unchanged.
            - Only output the final version of the sentence, without any extra information or formatting.

            # Output Format
            Return only the censored (or uncensored) sentence as plain text.

            # Examples
            Example 1:  
            Input: You are a stupid idiot!  
            Output: You are a ****** *****!

            Example 2:  
            Input: Have a nice day.  
            Output: Have a nice day.

            Example 3:  
            Input: You are such a dumb loser.  
            Output: You are such a **** *****.

            Example 4:  
            Input: The comedian used the word “jerk” in his act as a joke, but he wasn’t being mean.  
            Output: The comedian used the word “jerk” in his act as a joke, but he wasn’t being mean.

            Example 5:  
            Input: My friend accidentally said a bad word, but he apologized and explained he didn’t mean anything by it.  
            Output: My friend accidentally said a bad word, but he apologized and explained he didn’t mean anything by it.

            Example 6:  
            Input: Don’t be such a jerk!  
            Output: Don’t be such a ****!

            # Notes
            - Carefully assess the overall context and meaning of the sentence. Only censor words if the intent is genuinely harmful or offensive.
            - Do not censor words that happen to appear on offensive word lists when their usage is neutral, descriptive, or otherwise non-harmful.
            - Always preserve the sentence’s structure and meaning as much as possible while applying these rules.
            - Your objective is to censor only overtly offensive or harmful language with asterisks according to context, and to return only the resulting censored sentence as output. If the sentence is not offensive in intent or effect, do not filter any words and return it unchanged.

            (Reminder: Important—censor only if the meaning of the sentence is actually offensive or harmful, not merely because certain words appear.)""",
    
            input=message,
        )

    return response.output_text
