import sys
import os
import json
import re  # Import regex for cleanup
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

import json
import os
from src.load_leads import load_leads, search_lead
from src.load_meeting_notes import load_meeting_notes, get_meeting_summary
from src.recommend_model import recommend_subscription
from src.generate_products import generate_products
from src.generate_terms import generate_terms

# Ensure output directory exists
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_full_quote(company_name):
    """Generate a full AI-powered sales quote for a company and save it as a JSON file."""

    # Load leads and meeting notes
    leads_df = load_leads()
    meeting_df = load_meeting_notes()

    # Get company details
    company_info = search_lead(company_name, leads_df)
    if not company_info:
        return f"[ERROR] No company details found for '{company_name}'."

    # Extract only necessary fields
    filtered_company_info = {
        "Name": company_info.get("Name"),
        "Company": company_info.get("Company"),
        "Professional Email": company_info.get("Professional Email"),
        "Designation": company_info.get("Designation"),
        "Persona": company_info.get("Persona"),
        "Meeting Date": company_info.get("Meeting Date")
    }

    # Get meeting summary
    meeting_summary = get_meeting_summary(company_name, meeting_df)
    if not meeting_summary:
        return f"[ERROR] No meeting summary found for '{company_name}'."

    # Generate AI-based recommendations
    subscription_recommendation = recommend_subscription(meeting_summary)  # Pass only the summary
    products_and_services = generate_products(meeting_summary)  # Pass only the summary
    purchase_terms = generate_terms()  # No need to pass summary

    # Compile final quote
    quote = {
        "company_info": filtered_company_info,
        "meeting_summary": meeting_summary,
        "subscription_recommendation": subscription_recommendation,
        "products_and_services": products_and_services,
        "purchase_terms": purchase_terms
    }

    # Convert quote to JSON
    quote_json = json.dumps(quote, indent=4)

    # Save JSON to output folder
    file_path = os.path.join(OUTPUT_DIR, f"{company_name.replace(' ', '_')}_quote.json")
    with open(file_path, "w") as f:
        f.write(quote_json)

    return quote_json, file_path

def main():
    """Main function to run the AI-powered quote generator."""
    company_name = input("Enter company name for the quote: ").strip()

    if not company_name:
        print("[ERROR] Company name cannot be empty.")
        return

    result, file_path = generate_full_quote(company_name)

    print("\n[FINAL QUOTE GENERATED]:\n")
    print(result)
    print(f"\n✅ Quote saved to: {file_path}")

if __name__ == "__main__":
    # 1. Record start time
    start_time = time.time()
    
    # 2. Run your existing main logic
    main()
    
    # 3. Record end time and compute elapsed
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n[INFO] Execution Time: {total_time:.2f} seconds")