# aws-curl-lite

This is a development test project to call a REST API using SigV4Auth. 

## Background

I had intended to use [awscurl](https://github.com/okigan/awscurl) for AWS request signing. However, awscurl has a long standing issue with supporting AWS SSO (see [issue #114](https://github.com/okigan/awscurl/issues/114)). For my purposes, AWS SSO support was essential to conveniently test resource policies applying cross-account allow-lists in AWS API Gateway.

## Usage

1. Install project dependencies with uv:
   ```
   uv install
   ```
2. Run the CLI:
   ```
   uv run aws-curl-lite --profile <your_aws_profile> --location <your_api_endpoint>
   ```


