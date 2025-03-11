#!/bin/bash

# Activate the conda environment if using conda
# conda activate studios-launch-page

# Note: Sensitive environment variables should be set before running this script
# or provided through the Connect configuration

# Run the Flask application
python app.py --host=localhost --port=5000

# Alternatively, for production:
# gunicorn --bind localhost:5000 wsgi:application 