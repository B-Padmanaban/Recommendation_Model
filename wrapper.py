
import sys
import json
from recommender import recommend_schemes

try:
    # Get user profile from command line arguments
    user_profile = json.loads(sys.argv[1])

    # Get recommendations
    recommendations = recommend_schemes(user_profile)
    
    # Ensure we only output valid JSON to stdout
    print(json.dumps(recommendations))
except Exception as e:
    # Print error as JSON for proper handling
    print(json.dumps({"error": str(e)}))
