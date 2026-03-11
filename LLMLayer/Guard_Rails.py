'''
By: Ed Wang
Create on: 2025-12-27
Last Modified: 2025-12-27
Description: This module contains the guard rails for input prompts and output responses. It uses various scanners to ensure that the prompts and responses adhere to specified guidelines, such as language checks, toxicity checks, bias checks, and relevance checks.
'''




from llm_guard.input_scanners import Language, InvisibleText, PromptInjection, Toxicity, BanCode
from llm_guard.output_scanners import Bias, Relevance
from llm_guard.input_scanners.language import MatchType
from llm_guard.output_scanners.bias import MatchType as OutputMatchType
from llm_guard import scan_output, scan_prompt




print(f"---Initalizing Prompt Input Scanners---\n")

# Input Scanners for Pre RAG Prompt Check
Input_Scanners = {
    'LanguageCheck': Language(valid_languages=['en'], match_type=MatchType.FULL),
    'InvisibilityCheck': InvisibleText(),
    'PromptInjectionCheck': PromptInjection(threshold=0.20),
    'ToxicityCheck': Toxicity(threshold=0.30),
    'BanCode': BanCode()


}

print(f"---Initalizing Prompt Output Scanners---\n")


# Output Scanners for Post RAG Prompt Check
Output_Scanners = {
    'BiasCheck': Bias(threshold=0.90,  match_type=OutputMatchType.FULL),
    'Relevance': Relevance(threshold=0.5),


}


#Pre RAG Prompt Check function that takes in the users query and scans it using the input scanners.
def Pre_RAG_Prompt_Check(Prompt: str) -> dict:
    try:
        """
        Santizies the prompt based on different checks. 
        
        """
        print("---Scanning Input---\n")

        input_scanners = [scanner for _, scanner in Input_Scanners.items()]


        santized_prompt, results_valid, results_score = scan_prompt(input_scanners, Prompt)


        validity = list(results_valid.values())
        
        valid_prompt = all(validity)

        if valid_prompt:
            final_prompt = santized_prompt
        else:
            final_prompt = f"I cannot answer the question: {Prompt}"

        return {
            'IsValid': valid_prompt,
            'Prompt': final_prompt
        }


        
    except Exception as e:
        valid_prompt = False
        final_prompt = f"Unable to provide anwser due to (Pre RAG Prompt Check) system error => {e}"
        Result = {
            'IsValid':valid_prompt,
            'Prompt': final_prompt
        }
        return Result


#Post RAG Prompt Check function that takes in the augments prompt and orginial query and uses the output scanners for cleansing.
def Post_RAG_Prompt_Check(OriginalQuery ,AugmentedPrompt: str, ResponseText) -> dict:
    """
    Santizes the Augmented prompt.

    """

    print("---Scanning Response---\n")
    try:

        output_scanners = [scanner for _, scanner in Output_Scanners.items()]

        santized_response, results_valid, results_score = scan_output(output_scanners, AugmentedPrompt, ResponseText)

        validity = list(results_valid.values())
        valid_prompt = all(validity)

        if valid_prompt:
            final_response = santized_response
        else:
            final_response = f"I cannot answer the question: {OriginalQuery}"

        return {
            'IsValid': valid_prompt,
            'Response': final_response
        }


    except Exception as e:
        valid_prompt = False
        final_prompt = f"Unable to provide anwser due to (Post RAG Prompt Check) system error => {e}"
        Result = {
            'IsValid':valid_prompt,
            'Response': final_prompt
        }
        return Result




    