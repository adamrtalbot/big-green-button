from flask import Flask, render_template, jsonify
import os
import requests
import json
import logging
import argparse

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


def get_workflow_details(api_base, token, workflow_id):
    """Get workflow details from the Seqera Platform API."""
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        response = requests.get(f"{api_base}/workflow/{workflow_id}", headers=headers)
        response.raise_for_status()
        workflow_details = response.json()
        logging.info(
            f"Workflow Details Response: {json.dumps(workflow_details, indent=2)}"
        )
        return workflow_details
    except Exception as e:
        logging.error(f"Error getting workflow details: {str(e)}")
        return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/launch", methods=["POST"])
def launch_pipeline():
    """Launch a pipeline using Seqera Action."""
    try:
        # Get environment variables for Seqera Platform
        seqera_token = os.environ.get("SEQERA_ACCESS_TOKEN")
        action_id = os.environ.get("SEQERA_ACTION_ID")
        workspace_id = os.environ.get("SEQERA_WORKSPACE_ID")
        seqera_api_base = os.environ.get(
            "SEQERA_API_BASE", "https://api.cloud.stage-seqera.io"
        )

        # Initialize these variables at the function level
        org_name = os.environ.get("SEQERA_ORG_NAME", "")
        workspace_name = os.environ.get("SEQERA_WORKSPACE_NAME", "")

        if not all([seqera_token, action_id, workspace_id]):
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Missing required environment variables: SEQERA_ACCESS_TOKEN, SEQERA_ACTION_ID, SEQERA_WORKSPACE_ID",
                    }
                ),
                400,
            )

        # Always use the cloud.stage-seqera.io URL for the web interface
        # This is more reliable than using the landingUrl from service info
        if "api.cloud.stage-seqera.io" in seqera_api_base:
            seqera_web_base = "https://cloud.stage-seqera.io"
        elif "api.cloud.seqera.io" in seqera_api_base:
            seqera_web_base = "https://cloud.seqera.io"
        else:
            # Fall back to environment variable or default
            seqera_web_base = os.environ.get(
                "SEQERA_WEB_BASE", "https://cloud.stage-seqera.io"
            )

        logging.info(f"Using web base URL: {seqera_web_base}")

        # API endpoint for launching an action
        launch_url = (
            f"{seqera_api_base}/actions/{action_id}/launch?workspaceId={workspace_id}"
        )

        # Headers for authentication
        headers = {
            "Authorization": f"Bearer {seqera_token}",
            "Content-Type": "application/json",
        }

        # Empty payload as per API requirements
        payload = {}

        # Launch the action
        response = requests.post(launch_url, headers=headers, json=payload)

        # Print detailed debug information
        logging.info(f"Request URL: {launch_url}")
        logging.info(f"Response Status: {response.status_code}")
        logging.info(f"Response Content: {response.text}")

        # Check for error response
        if response.status_code != 200:
            error_detail = response.text
            try:
                error_json = response.json()
                if "message" in error_json:
                    error_detail = error_json["message"]
            except:
                pass

            return (
                jsonify(
                    {
                        "success": False,
                        "message": f"Error from Seqera API: {response.status_code} - {error_detail}",
                    }
                ),
                500,
            )

        # Get the response data
        response_data = response.json()
        logging.info(f"Response Data: {json.dumps(response_data, indent=2)}")

        # Construct the run URL using data from the API response
        run_url = None

        # Get the workflow ID from the response
        workflow_id = None
        if "workflowId" in response_data:
            workflow_id = response_data["workflowId"]
            logging.info(f"Found workflowId: {workflow_id}")

            # Fetch workflow details to get organization and workspace information
            workflow_details = get_workflow_details(
                seqera_api_base, seqera_token, workflow_id
            )

            if workflow_details:
                # Try to extract organization and workspace info from workflow details
                if (
                    "data" in workflow_details
                    and "workspaceRef" in workflow_details["data"]
                ):
                    workspace_ref = workflow_details["data"]["workspaceRef"]
                    logging.info(
                        f"Found workspaceRef in workflow details: {workspace_ref}"
                    )

                    if "orgName" in workspace_ref:
                        org_name = workspace_ref["orgName"]
                        logging.info(f"Found orgName in workflow details: {org_name}")

                    if "workspaceName" in workspace_ref:
                        workspace_name = workspace_ref["workspaceName"]
                        logging.info(
                            f"Found workspaceName in workflow details: {workspace_name}"
                        )

            # Ensure we have org_name and workspace_name, using environment variables as fallback
            if not org_name:
                org_name = os.environ.get("SEQERA_ORG_NAME", "")
                logging.info(f"Using fallback orgName from environment: {org_name}")

            if not workspace_name:
                workspace_name = os.environ.get("SEQERA_WORKSPACE_NAME", "")
                logging.info(
                    f"Using fallback workspaceName from environment: {workspace_name}"
                )

            # Construct the URL if we have all the necessary components
            if workflow_id and org_name and workspace_name and seqera_web_base:
                run_url = f"{seqera_web_base}/orgs/{org_name}/workspaces/{workspace_name}/watch/{workflow_id}"
                logging.info(f"Constructed run URL: {run_url}")
            else:
                logging.info(
                    f"Missing components for URL: workflow_id={workflow_id}, org_name={org_name}, workspace_name={workspace_name}, seqera_web_base={seqera_web_base}"
                )
        else:
            logging.info("No workflowId found in response")

        return jsonify(
            {
                "success": True,
                "message": "Pipeline launched successfully via Seqera Action",
                "data": response_data,
                "runUrl": run_url,
            }
        )

    except requests.exceptions.RequestException as e:
        logging.error(f"Exception details: {str(e)}")
        return (
            jsonify(
                {"success": False, "message": f"Error launching pipeline: {str(e)}"}
            ),
            500,
        )


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Studios Launch Page")
    parser.add_argument(
        "--host",
        default=os.environ.get("HOST", "0.0.0.0"),
        help="Host to bind to (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", 5000)),
        help="Port to bind to (default: 5000)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=os.environ.get("DEBUG", "").lower() in ("true", "1", "yes"),
        help="Enable debug mode",
    )
    return parser.parse_args()


# WSGI entry point for Connect binary
application = app


if __name__ == "__main__":
    args = parse_args()
    logging.info(f"Starting server on {args.host}:{args.port} (debug={args.debug})")
    app.run(host=args.host, port=args.port, debug=args.debug)
