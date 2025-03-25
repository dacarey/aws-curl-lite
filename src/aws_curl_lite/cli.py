#!/usr/bin/env python3
import argparse
import sys
import json  # added for pretty printing JSON

import boto3
from botocore.awsrequest import AWSRequest
from botocore.auth import SigV4Auth
from botocore.exceptions import TokenRetrievalError
import requests


def main():
    parser = argparse.ArgumentParser(
        description="Make a signed GET request to an AWS API Gateway or Lambda function URL"
    )
    parser.add_argument(
        "--profile",
        required=True,
        help="AWS CLI profile name (assumes AWS SSO login is already done)",
    )
    parser.add_argument(
        "--location",
        required=True,
        help="URL of the AWS API Gateway REST API or Lambda function URL",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Output raw response body without pretty print",
    )
    args = parser.parse_args()

    # Create a boto3 session using the specified profile
    session = boto3.Session(profile_name=args.profile)
    credentials = session.get_credentials()
    if credentials is None:
        print(f"Could not load AWS credentials for profile '{args.profile}'.")
        sys.exit(1)
    
    try:
        frozen_creds = credentials.get_frozen_credentials()
    except TokenRetrievalError:
        print(f"AWS SSO session has expired or is not available for profile '{args.profile}'.")
        print(f"Please run: aws sso login --profile {args.profile}")
        sys.exit(1)

    # Retrieve region from the session; this must be set in your profile/config
    region = session.region_name
    if not region:
        print(f"Region not found in profile '{args.profile}'. Please set it up.")
        sys.exit(1)

    # For API Gateway, the service is "execute-api". (Adjust if needed for Lambda URLs.)
    service = "execute-api"

    # Create an AWSRequest for a GET call
    aws_request = AWSRequest(method="GET", url=args.location)

    # Sign the request with SigV4Auth using the frozen credentials
    SigV4Auth(frozen_creds, service, region).add_auth(aws_request)

    # Convert signed headers to a dict
    headers = dict(aws_request.headers)

    # Make the GET request using the signed headers
    response = requests.get(args.location, headers=headers)
    print("Status Code:", response.status_code)
    print("Response Body:")
    content_type = response.headers.get("Content-Type", "").lower()
    if not args.raw and "application/json" in content_type:
        try:
            parsed = response.json()
            print(json.dumps(parsed, indent=4))
        except ValueError:
            print(response.text)
    else:
        print(response.text)


if __name__ == "__main__":
    main()
