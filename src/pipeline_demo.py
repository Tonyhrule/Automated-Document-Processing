import os
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))
from document_processor import DocumentProcessor

def main():
    # Initialize processor
    processor = DocumentProcessor()
    
    # Set up directories
    base_dir = Path(__file__).parent.parent
    input_dir = base_dir / "data" / "input"
    output_dir = base_dir / "data" / "output"
    
    # Create directories if they don't exist
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\nProcessing documents...")
    processor.process_documents(str(input_dir), str(output_dir))
    
    print("\nProcessed files in output directory:")
    for file in output_dir.glob("*.json"):
        print(f"- {file.name}")
    
    print("\nExtracting profile information...")
    results = []
    for file_path in output_dir.glob("*.json"):
        with open(file_path, "r") as f:
            content = f.read()
            profile_info = processor.extract_profile_info(content)
            trustworthiness = profile_info.get("trustworthiness_score", 0)
            response = profile_info.get("response", {})
            if isinstance(response, str):
                try:
                    import json
                    response = json.loads(response)
                except:
                    response = {}
            
            # Only include results that are from tables and have high confidence
            if (trustworthiness > 0.7 and isinstance(response, dict) and
                not all(v == "not_found" for v in response.values())):
                results.append({
                    "data": response,
                    "trustworthiness": trustworthiness,
                    "source": file_path.name
                })
    
    print("\nProcessing Results:")
    for result in results:
        print(f"\nSource: {result['source']}")
        print(f"Data: {result['data']}")
        print(f"Trustworthiness Score: {result['trustworthiness']}")
    return results

if __name__ == "__main__":
    main()
