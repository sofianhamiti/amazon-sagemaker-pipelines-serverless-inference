import os
import json
import boto3
import logging
import argparse
import requests

logger = logging.getLogger(__name__)
api_client = boto3.client('apigatewayv2')


def get_api_url(api_name):
    list_apis = api_client.get_apis()['Items']
    filtered_apis = [api for api in list_apis if api["Name"] == api_name]
    api_url = filtered_apis[0]['ApiEndpoint']
    return api_url


def test_api(name, url, payload):
    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()  # if status !=200 raise exception
        return {
            'api_name': name,
            'api_url': url,
            'success': True
        }
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level", type=str, default=os.environ.get("LOGLEVEL", "INFO").upper())
    parser.add_argument("--import-build-config", type=str, required=True)
    parser.add_argument("--export-test-results", type=str, required=True)
    args, _ = parser.parse_known_args()

    # Configure logging to output the line number and message
    log_format = "%(levelname)s: [%(filename)s:%(lineno)s] %(message)s"
    logging.basicConfig(format=log_format, level=args.log_level)

    # Load the build config
    with open(args.import_build_config, "r") as f:
        config = json.load(f)

    # Get the api name from sagemaker project name
    api_name = "{}-{}".format(config["Parameters"]["SageMakerProjectName"], config["Parameters"]["StageName"])

    api_url = get_api_url(api_name)

    # send a test data point to the api and verifying the response status code
    test_payload = {
        "length": -0.158164,
        "diameter": -0.280982,
        "height": -0.227545,
        "whole_weight": -0.352298,
        "shucked_weight": -0.596421,
        "viscera_weight": -0.019102,
        "shell_weight": -0.135293,
        "sex_M": 0.0,
        "sex_F": 0.0,
        "sex_I": 1.0
    }

    results = test_api(api_name, api_url, test_payload)

    # Print results and write to file
    logger.debug(json.dumps(results, indent=4))
    with open(args.export_test_results, "w") as f:
        json.dump(results, f, indent=4)
