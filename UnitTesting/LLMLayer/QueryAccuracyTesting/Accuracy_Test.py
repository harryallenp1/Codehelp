'''
By: Tejas Kumar
Date: 2026-01-19

The module is meant to test the LLM with queries and measure how similar the LLM's answers are to known answers. 
A match of over 0.60 generally means the answer is moderately similar. 
'''

import json
from sentence_transformers import SentenceTransformer, util
import requests
from tqdm import tqdm
import warnings

#region Wrapper transformer for transforming sentences to vectors.
answerTester = SentenceTransformer('all-mpnet-base-v2')
def Test_Answer(answer: str, knownanswer: str):
    try:
        
        known_embed = answerTester.encode(knownanswer)
        answ_embed = answerTester.encode(answer)

        #Getting the Cosine Similarity between the Known Answer and the LLMs answer.
        score = util.cos_sim(known_embed, answ_embed).item()

        return score

    except Exception as e:
        print(f"--QueryTester-- Test_Answer() => Error testing answer => [{e}]")
        return  0.0
#endregion

#region Test Queries
Test_Queries_Path = 'Test_Queries.json'

with open(Test_Queries_Path, 'r') as f:
    Test_Queries = json.load(f)
#endregion 

#region RAG API
RAG_API_URI = "http://localhost:8001/query/"

def Send_Query(user_query: str) -> str:
    try:
            
        payload = {
                "user_query": user_query
        }
        response = requests.post(RAG_API_URI, json=payload)
        response.raise_for_status()
        data = response.json()
        answer = data.get("answer", "I'm sorry, I couldn't get an answer at this time.")
        return answer
    except Exception as e:
        print(f"--QueryTester-- Send_Query() => Error sending query to RAG API => [{e}]")
        return "Error processing the query."

#endregion 



class QueryTester:
    def __init__(self, Test_Queries: dict):
        self.Test_Queries = Test_Queries
        self.Test_Queries_With_Answers = Test_Queries




        
    def Test_All_Answers(self):
        try:
            keys = list(self.Test_Queries.keys())
            for key in tqdm(keys, desc='Testing All Queries', unit='Query'):
                query = self.Test_Queries[key]['Query']

                answer = Send_Query(user_query=query)
                knownanswer = Test_Queries[key]['Known-Answer']

                score = Test_Answer(answer=answer, knownanswer=knownanswer)

                self.Test_Queries_With_Answers[key]['LLM-Answer'] = answer
                self.Test_Queries_With_Answers[key]['Similarity Score'] = score

            
        except Exception as e:
            print(print(f"--QueryTester-- Test_All_Answers() => Error => [{e}]"))
            pass

    def Save_Results(self):
        try:
            with open('Test_Queries_Results.json', 'w') as f:
                json.dump(self.Test_Queries_With_Answers, f, indent=4)
                
            print(f"Results Saved")

        except Exception as e:
            print(print(f"--QueryTester-- Save_Results() => Error => [{e}]"))
            pass


def main():
    try:
        Tester = QueryTester(Test_Queries=Test_Queries)

        print(f"---Testing Queries---")
        Tester.Test_All_Answers()

        print(f"---Saving Answers---")
        Tester.Save_Results()
    

    except Exception as e:
        print(f"main() Error =>\n\t[{e}]")
        exit()

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    main()


        




