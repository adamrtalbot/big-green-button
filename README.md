# Studios Launch Page

A simple web application with a big green "Launch" button that launches a pipeline using a Seqera Action and redirects to the run page.

## Setup

1. Install dependencies:
```
pip install -r requirements.txt
pip install types-requests  # For type checking
```

2. Set up environment variables:
```
export SEQERA_API_BASE="https://api.cloud.stage-seqera.io"
export SEQERA_ACCESS_TOKEN="your_access_token"
export SEQERA_WORKSPACE_ID="your_workspace_id"
export SEQERA_ACTION_ID="your_action_id"
```

The following environment variables are optional and only used as fallbacks if the information cannot be extracted from the API:
```
export SEQERA_WEB_BASE="https://cloud.stage-seqera.io"  # Fallback if service-info doesn't provide landingUrl
export SEQERA_ORG_NAME="your_organization_name"         # Fallback if not in the workflow details
export SEQERA_WORKSPACE_NAME="your_workspace_name"      # Fallback if not in the workflow details
```

## Running the Application

Start the web server:
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
