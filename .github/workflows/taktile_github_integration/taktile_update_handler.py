import sys
import requests
import json

Taktile_API_KEY = sys.argv[1]
ORGANIZATION_NAME = sys.argv[2]

def get_raw_json(data):
    import json
    return json.dumps(data.json())

def getFlowIdListForOrganization(data):
    """ Params:
            data: JSON response object 
        Returns:
            List of flow_IDs in org NB36
    """    
    flow_objects = data["data"]["flows"]
    flow_IDs = [flow_id["flow_id"] for flow_id in flow_objects]
    return flow_IDs

def api_not_ok_error(response):
    print(f"Request failed with status code {response.status_code}: {response.text}")
    return 
    

def extract_codeNode_details(res):
    code_nodes = [
        {
            "node_name": node["node_name"],
            "node_id": node["node_id"]
        }
        for node in res["data"]["graph"] if "node_type" in node and node["node_type"] == "code_node"
    ]

    return code_nodes


if __name__  == "__main__":

    # Define the API endpoint and headers
    # ENDPOINT: Return a list of Decision Flows in a customer’s workspace
    url = 'https://eu-central-1.taktile-org.decide.taktile.com/run/api/v1/flows/list-decision-graphs/sandbox/decide'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Api-Key': f'{Taktile_API_KEY}'
    }

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

    flow_ids = []
    if response.status_code == 200:
        print("Request was successful")
        flow_ids = getFlowIdListForOrganization(response.json())
        print(f"Flow_IDs: { flow_ids }" )
    else:
        ## ERROR EXIT ->
        api_not_ok_error(response)


    # get-decision-graph
    for flow_id in flow_ids:
        data["data"] = { "flow_id": str(flow_id) }
        url = 'https://eu-central-1.taktile-org.decide.taktile.com/run/api/v1/flows/get-decision-graph/sandbox/decide'
        response_2 = requests.post(url, headers=headers, data=json.dumps(data))

        if response_2.status_code == 200:
            print(f"Request_2 for flow_id: {flow_id} was successful:")
            print(response_2.json())
            code_nodes = extract_codeNode_details(response_2.json())
            # Print the extracted code nodes
            for code_node in code_nodes:
                print(f"Node Name: {code_node['node_name']}, Node ID: {code_node['node_id']}")

        else:
            api_not_ok_error(response)




