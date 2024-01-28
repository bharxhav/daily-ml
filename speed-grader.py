import os
import csv
import json
from dotenv import load_dotenv
import google.generativeai as genai

class SpeedGrader:
    """
    A class to grade any code using GPT margins.
    """

    def __init__(self):
        """
        Initializes the SpeedGrader class and configures the Gemini API key.
        """
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    def get_gemini_response(self, input_text: str) -> str:
        """
        Generates a response using the Gemini API for a given input text.

        Parameters:
            input_text (str): The input text for which the response is generated.

        Returns:
            str: The generated response.
        """
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(input_text)
        return response.text

def main():
    """
    Main function.
    """

    # assignment_number = int(input('Give the assignment number:'))
    assignment_number = 1
    assignment_prompt = ""
    results = {}

    # Read assignment data from a JSON file
    with open(f'./meta/assignment{assignment_number} prompt.txt', 'r') as file:
        assignment_prompt = file.read()
    
    # Read .bat files from the ./assignments/ folder
    assignments = [f.split('.')[0] for f in os.listdir(f'./meta/assignments {assignment_number}/')]

    speed_grader = SpeedGrader()

    i = 0
    for uni in assignments:
        try:
            print(i, uni)
            i += 1

            assignment = ""

            with open(f'./meta/assignments {assignment_number}/{uni}.bas', 'r') as f:
                assignment = f.read().strip()

            prompt = assignment_prompt.format(submission=assignment)
            ret = speed_grader.get_gemini_response(prompt)[7:-3]
            results[uni] = json.loads(ret)
        except:
            print('FAILED: ', uni)

        # print(uni, results[uni])
        # break

    # Save results to a CSV file
    with open(f'./meta/assignment {assignment_number} grades.csv', 'w', newline='') as csvfile:
        fieldnames = ['UNI', 'GRADE', 'A1', 'AR1', 'A2', 'AR2', 'A3', 'AR3']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for key, value in results.items():
            writer.writerow({'UNI': key, 'GRADE': value['GRADE'], 
                             'A1': value['A1'], 'AR1': value['AR1'],
                             'A2': value['A2'], 'AR2': value['AR2'],
                             'A3': value['A3'], 'AR3': value['AR3'],
                             })

if __name__ == "__main__":
    load_dotenv()
    main()

