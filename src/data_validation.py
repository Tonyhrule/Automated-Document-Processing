import os
from pathlib import Path
import pandas as pd
from cleanlab_studio import Studio
from dotenv import load_dotenv

def setup_environment():
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
    
    studio = Studio(os.getenv('CLEANLAB_API_KEY'))
    return studio.TLM()

def analyze_medical_record(tlm, record):
    analysis_prompt = """Analyze this medical record for potential issues or inconsistencies:
    Patient ID: {patient_id}
    Diagnosis: {diagnosis}
    Medication: {medication}
    Dosage: {dosage}
    Note: {note}
    Visiting Hours: {visiting_hours}
    Invoice: {invoice}

    Provide:
    1. A brief summary of the record
    2. Answer 'Yes' or 'No': Are there any concerning patterns or inconsistencies?
    3. If Yes, explain the specific concerns."""
    
    response = tlm.prompt(analysis_prompt.format(**record))
    
    return {
        'summary': response.get('response', '').split('\n')[0],
        'concerns': 'Yes' if 'yes' in response.get('response', '').lower() else 'No',
        'details': response.get('response', ''),
        'trustworthiness': response.get('trustworthiness_score', 0)
    }

def main():
    tlm = setup_environment()
    df = pd.read_csv('data/data_entry.csv')
    print(f"\nAnalyzing {len(df)} medical records...")
    
    results = []
    for idx, row in df.iterrows():
        print(f"\nProcessing record {idx + 1}/{len(df)}")
        record = row.to_dict()
        analysis = analyze_medical_record(tlm, record)
        
        results.append({
            'patient_id': record['patient_id'],
            'diagnosis': record['diagnosis'],
            'summary': analysis['summary'],
            'concerns': analysis['concerns'],
            'details': analysis['details'],
            'trustworthiness': analysis['trustworthiness']
        })
    
    results_df = pd.DataFrame(results)
    
    # Sort and display concerning records by trustworthiness score
    concerning_records = results_df[results_df['concerns'] == 'Yes'].sort_values(
        by=['trustworthiness'], ascending=False)
    
    print("\nConcerning Medical Records (Sorted by Trustworthiness Score):")
    for idx, row in concerning_records.iterrows():
        print(f"\nPatient ID: {row['patient_id']}")
        print(f"Diagnosis: {row['diagnosis']}")
        print(f"Summary: {row['summary']}")
        print(f"Details: {row['details']}")
        print(f"Trustworthiness Score: {row['trustworthiness']:.4f}")
        print("-" * 80)

if __name__ == "__main__":
    main()
