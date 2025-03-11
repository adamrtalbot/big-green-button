# Studios Launch Page

A simple web application with a big green "Launch" button that launches a pipeline using a Seqera Action and redirects to the run page.

## Setup

### Using pip

1. Install dependencies:
```
pip install -r requirements.txt
pip install types-requests  # For type checking
pip install gunicorn  # For production deployment
```

### Using conda

1. Create and activate the conda environment:
```
conda env create -f environment.yml
conda activate studios-launch-page
```

2. Set up environment variables:
```
# Required environment variables
export SEQERA_API_BASE="https://api.cloud.seqera.io"
export SEQERA_ACCESS_TOKEN="your_access_token"
export SEQERA_WORKSPACE_ID="your_workspace_id"
export SEQERA_ACTION_ID="your_action_id"

# IMPORTANT: These variables are required for URL construction
# They must be set correctly for the redirect to work
export SEQERA_ORG_NAME="your_organization_name"         # Organization slug (e.g., "seqeralabs")
export SEQERA_WORKSPACE_NAME="your_workspace_name"      # Workspace slug (e.g., "scidev-azure")
export SEQERA_WEB_BASE="https://cloud.seqera.io"        # Web UI base URL
```

## Running the Application

### Development Mode

Start the web server in development mode:
```
python app.py
```

Then open your browser and navigate to: http://localhost:5000

The page will display a big green "Launch" button centered on the screen. When clicked, it will:
1. Get service information from the Seqera Platform API to determine the web URL
2. Launch a pipeline via the specified Seqera Action
3. Get the workflow ID from the response
4. Fetch the workflow details to get organization and workspace information
5. Construct the run URL using the workflow ID and workspace information
6. Redirect to the Seqera Platform run page to monitor the pipeline execution

## Debugging with VSCode

A VSCode debug configuration is included in the `.vscode/launch.json` file. To debug the application:

1. Open the project in VSCode
2. Go to the Run and Debug view (Ctrl+Shift+D or Cmd+Shift+D on Mac)
3. Select "Python: Flask" from the dropdown menu
4. Click the green play button or press F5

The debugger will prompt you for your Seqera credentials before starting the application.

## Running with Connect

### Option 1: Running as a WSGI Application (Connect manages the application)

To run the application with the Connect binary:

1. Ensure the Connect binary is installed
2. Run the application using:
```
connect-client run --wsgi-app wsgi:application --port 5000
```

### Option 2: Running as a Service (Connect proxies to an existing application)

If Connect is already running and you want to connect your application to it:

1. Start your Flask application separately:
```
./run_app.sh
```

2. Configure Connect to proxy to your application by using the `connect_config.yml` file:
```
connect-client config --file connect_config.yml
```

This approach allows Connect to proxy requests to your locally running Flask application.
