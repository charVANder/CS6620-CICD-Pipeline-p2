'''Just the Flask app entry point which imports the api stuff in my src folder
'''
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from api import create_app
if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)