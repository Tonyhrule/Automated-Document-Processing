import os
import json
from pathlib import Path
from cleanlab_studio import Studio

class DocumentProcessor:
    def __init__(self):
        self.studio = Studio(os.environ["CLEANLAB_API_KEY"])
        self.tlm = self.studio.TLM()
        
    def process_documents(self, input_dir: str, output_dir: str):
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        for file in input_path.glob("*.txt"):
            with open(file, 'r') as f:
                content = f.read()
                output_file = output_path / f"{file.stem}.json"
                with open(output_file, 'w') as out:
                    json.dump({"content": content}, out)
    
    def detect_table_content(self, text: str) -> bool:
        prompt = """Determine if the following text contains tabular data with profile information.
        Return 'true' if it contains table-like structured data, 'false' otherwise.
        
        Text: {text}"""
        response = self.tlm.prompt(prompt.format(text=text))
        print(f"\nTable detection response: {response}")
        return isinstance(response, dict) and response.get('response', '').lower() == 'true'

    def extract_profile_info(self, text: str) -> dict:
        if not self.detect_table_content(text):
            return {'response': {'first_name': 'not_found', 'last_name': 'not_found', 'gender': 'not_found'}, 
                    'trustworthiness_score': 0}

        prompt = """Extract profile information from this table. For each row, provide the first name, last name, and gender.
        Format the response as a list of JSON objects, each with fields: first_name, last_name, gender.
        
        Text: {text}"""
        
        response = self.tlm.prompt(prompt.format(text=text))
        print(f"\nProfile extraction response: {response}")
        
        if isinstance(response, dict):
            response['trustworthiness_score'] = response.get('trustworthiness_score', 0)
            return response
        return {'response': {'first_name': 'not_found', 'last_name': 'not_found', 'gender': 'not_found'}, 
                'trustworthiness_score': 0}
