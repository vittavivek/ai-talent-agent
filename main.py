import os
import sys

# Get absolute paths
root_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(root_dir, "backend")

# Change working directory to backend so file operations (like opening candidates.json) work correctly
os.chdir(backend_dir)

# Add backend directory to the Python path so inner imports (like `from parser import ...`) work
sys.path.insert(0, backend_dir)

# Import the FastAPI app from backend/main.py
# We use an alias to avoid confusing it with this current file
import main as backend_main
app = backend_main.app
