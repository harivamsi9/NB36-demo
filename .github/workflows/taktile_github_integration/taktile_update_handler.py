import sys
import requests
import json


Taktile_API_KEY = sys.argv[1]
ORGANIZATION_NAME = sys.argv[2]


def get_raw_json(data):
    import json
    return json.dumps(data.json())



# Define the API endpoint and headers
url = 'https://eu-central-1.taktile-org.decide.taktile.com/run/api/v1/flows/list-decision-graphs/sandbox/decide'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    # 'X-Api-Key': 'c179117d-a4ce-4635-a268-b37d13668515'  # Replace with your actual API key
    'X-Api-Key': f'{Taktile_API_KEY}'

}

# Define the request body
data = {
    "data": {
        "organization_name": f"{ORGANIZATION_NAME}"
    },
    "metadata": {
        "version": "v1.0",
        "entity_id": "string"
    },
    "control": {
        "execution_mode": "sync"
    }
}

# Make the POST request
response = requests.post(url, headers=headers, data=json.dumps(data))


def getFlowIdListForOrganization(data):
    """ Params:
            data: JSON response object 
        Returns:
            List of flow_IDs in org NB36
    """    
    flow_objects = data["data"]["flows"]
    flow_IDs = [flow_id["flow_id"] for flow_id in flow_objects]
    return flow_IDs

# Check the response
if response.status_code == 200:
    print("Request was successful:")
    print(response.json())  # Print the JSON response
    print(f"Org: NB36 -> Flow_IDs: { getFlowIdListForOrganization(response.json()) }" )
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")