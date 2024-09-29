import sys
import requests
import json
import os

Taktile_API_KEY = sys.argv[1]
ORGANIZATION_NAME = sys.argv[2]

def auth_header(Taktile_API_KEY):
    return {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Api-Key': f'{Taktile_API_KEY}'
    }

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
    
def file_exists(file_path):
    """ Returns True if file_name.py present in dir_path else False """
    return os.path.isfile(file_path)

def modify_codeNode_with_src_code(flow_id, node_id, src_code):
    # PATCH patch-decision-graph/sandbox/decide
    headers = auth_header(Taktile_API_KEY)
    data = {
        "data": {
        "flow_id": f"{flow_id}",
        "node_id": f"{node_id}",
        "src_code": f"{src_code}"
        },
        "metadata": {
            "version": "v1.0",
            "entity_id": "string"
        },
        "control": {
            "execution_mode": "sync"
        }
    }
    url = "https://eu-central-1.taktile-org.decide.taktile.com/run/api/v1/flows/patch-decision-graph/sandbox/decide"

    response_srcCode = requests.post(url, headers=headers, data=json.dumps(data))
    if response_srcCode.status_code == 200:
        print(response_srcCode.json()["data"]["message"])
        return response_srcCode.json()["data"]["message"]
    
    else: api_not_ok_error(response_srcCode)
        



    

def extract_codeNode_and_update_srcCode(flow_id, res):

    decision_flow_file = os.path.join(os.path.dirname(__file__), '..', "..", "..", 'decision_flow.json')
    decision_flow_file_obj = open(decision_flow_file, 'r')
    decision_flow_lookup = json.load(decision_flow_file_obj)["decision_flow_ids"]

    dir_path = decision_flow_lookup[str(flow_id)]

    for node in res["data"]["graph"]:

        if "node_type" in node and node["node_type"] == "code_node":
            # Found CODE_NODE
            node_id = node["node_id"]
            print(f'flow_id: {flow_id}, dirPath: {dir_path}, Node Name: { node["node_name"] }, Node ID: { node_id }')

            # UPDATE SRC CODE IF FILE EXISTS
            print("CURR WORK DIR: ",os.getcwd())
            file_path = os.path.join(os.getcwd(), dir_path, node["node_name"] + '.py')
            # file_path = os.path.join(dir_path, node["node_name"] + '.py')
            if file_exists(file_path):
                src_code = ""
                # modify the src_code in the code_node
                with open(file_path, 'r') as file:
                        src_code = file.read()

                modify_codeNode_with_src_code(flow_id, node_id, src_code)
            else:
                print(f'{file_path} does not exist')




if __name__  == "__main__":
    # ENDPOINT: Return a list of Decision Flows in a customer’s workspace
    url = 'https://eu-central-1.taktile-org.decide.taktile.com/run/api/v1/flows/list-decision-graphs/sandbox/decide'

    headers = auth_header(Taktile_API_KEY)
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
    else:
        api_not_ok_error(response)


    # get-decision-graph
    for flow_id in flow_ids:
        data["data"] = { "flow_id": str(flow_id) }
        url = 'https://eu-central-1.taktile-org.decide.taktile.com/run/api/v1/flows/get-decision-graph/sandbox/decide'
        response_2 = requests.post(url, headers=headers, data=json.dumps(data))

        if response_2.status_code == 200:
            print(f"Request_2 for flow_id: {flow_id} was successful:")
            extract_codeNode_and_update_srcCode(flow_id, response_2.json())
        else:
            api_not_ok_error(response)




