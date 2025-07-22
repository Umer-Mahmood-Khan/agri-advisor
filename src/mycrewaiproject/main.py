# src/mycrewaiproject/main.py

import os
import sys
from dotenv import load_dotenv

# Add src/ to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from mycrewaiproject.crew import create_crew

# Load environment variables
load_dotenv()

def run():
    # Get crop type dynamically from user
    crop_type = input("Please enter the crop type (e.g., cotton, wheat, maize): ").strip()

    # Create and configure the crew
    crew = create_crew()

    # Pass dynamic input (crop type) to agents and tasks
    result = crew.kickoff(inputs={"crop_type": crop_type})

    print("\n=== FINAL WEATHER REPORT FOR {} ===\n".format(crop_type.upper()))
    print(result)


if __name__ == '__main__':
    run()
