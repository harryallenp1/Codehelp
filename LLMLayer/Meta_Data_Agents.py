'''
By: Abira Demello
Create on: 2025-12-27
Last Modified: 2025-12-27
Description: This module contains metadata agents that help in filtering and categorizing content based on predefined rules and mappings.
'''



from langchain_core.messages import HumanMessage

Content_Sample_Maps = {
    'Which occupation type will be in demand in the future in Ontario?': 'Future Labour Force Needs',
    'What is the average anual demand for the stem fields in Ontario?': 'Future Labour Force Needs',
    'What educational requirements are needed to become a Data Scientist?': 'NOC',
    'What are the specific NOC occupations I can pursue with a degree in Political Science?': 'NOC',
    'What kind of mental health services are avaiable at Guelph University?': 'Mental Health',
    'How can I access mental health support as a student at the University of Guelph?': 'Mental Health',
    'What was the employment rate for Computer Science Graduates?':'Graduate Survey',
    'What is the employment rate for Engineering Graduates?':'Graduate Survey',

}



#Function that uses an instance of an LLM to determine the content type filters based on the query.
def Content_Type_Filter(query: str, llm) -> dict:
    try:
        
        rules_text = "\n".join(
            [f"IF query mentions anything like ({key}) THEN return '{value}'"
             for key, value in Content_Sample_Maps.items()]
        )

        #Assigning the Role.
        prompt = f"""
            You are an agent that determines which Content filters apply.

            Here are some GENERAL examples of how to decide them using an IF → THEN rule template:

            {rules_text}

            Query: "{query}"

            Return ONLY the list of all Content (from the THEN side) that apply to this query.
            The valid SKU groups are: {list(set(Content_Sample_Maps.values()))}

            Respond ONLY as a Python list, e.g => ["Graduate Survey", "Mental Health"]
            """

        response = llm.invoke([HumanMessage(content=prompt)])
        decision = response.content.strip()

        
        try:
            detected_groups = eval(decision)
            if not isinstance(detected_groups, list):
                detected_groups = []
            
            if len(detected_groups) == 0:
                detected_groups = []
        except:
            detected_groups = []

        base_meta_data = {}

        #Appending the content filter if any groups were detected.
        if detected_groups:
            base_meta_data["content"] = {"$in": detected_groups}

        return base_meta_data

    except Exception as e:
        print(f"Error in Content_Type_Filter: {e}")
        return {}

