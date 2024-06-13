import json
import os

def formatVariable(path):
    if path[0] == ":":
        return "{{"+path[1:]+"}}"
    else:
        return path
    
def print_file_variables(f):
    f.write('@appPath=<app-name>\n')
    f.write('@baseUrl=https://{{host}}/{{appPath}}{{envPath}}')
    f.write('\n\n')

def print_path_param_variables(f, item):
    request = item['request']
    variables = request['url']['variable']
    if len(variables) > 0:
        f.write('# Path params\n')  
    for variable in variables:
        f.write(f"@{variable['key']}={variable['value']}\n")

def print_query_params(f, item):
    request = item['request']
    query = request['url']['query']
    if len(query) > 0:
        f.write('# Query Params\n')
    for param in query:
        f.write(f"@{param['key']}={param['value']}\n")

def print_method_name(f, item):
    f.write(f"# {item['name']}\n")


def print_method_url(f, item):
    request = item['request']
    method = request['method']
    
    url = f"{''.join(request['url']['host'])}/{'/'.join([formatVariable(path) for path in request['url']['path']])}"
    
    params=""
    if len(request['url']['query']) > 0 :
        query = request['url']['query']
        params = "\n?"
        params += "&".join([f"{param['key']}={{{{{param['key']}}}}}\n" for param in query])
        
    f.write(f"{method} {url}")
    f.write(f"{params}")
    f.write("\n")

def print_headers(f, item):
    request = item['request']
    for header in request['header']:
        f.write(f"{header['key']}: {header['value']}\n")

def print_auth_header(f):
    authKey = "Authorization"
    authValue= "Bearer {{token}}"
    f.write(f"{authKey} : {authValue}")

def print_body(f, item):
    request = item['request']
    if 'body' in request:
        f.write(f"\n{request['body']['raw']}\n")

def print_end_method(f):
    f.write('\n')
    f.write('###\n')
    f.write('\n')

def print_item(f, item):
    print_method_name(f, item)
    print_path_param_variables(f, item)
    print_query_params(f, item)
    print_method_url(f, item)
    print_headers(f,item)
    print_auth_header(f)
    print_body(f, item)
    print_end_method(f)

def postman_to_http(input_file_path, output_file_path):
    with open(input_file_path, mode='r', encoding="utf8") as f:
        postman_collection = json.load(f)
       
        if 'item' in postman_collection and len(postman_collection['item']) > 0 and 'item' in postman_collection['item'][0]:
            print(f"Reading {input_file_path}")
            for chapter in postman_collection['item']:
                
                chapter_output_filename = os.path.join(output_file_path,chapter['name']+".http")
                with open(chapter_output_filename,  mode='w', encoding="utf8") as f:
                    
                    print_file_variables(f)

                    # itemsColl = [item for items in postman_collection['item'] for item in items['item']]
                    itemsColl = chapter['item']
                    for item in itemsColl:
                    
                        print_item(f, item)
                print(f"Saving {chapter_output_filename}")

        else: 
            print(f"{input_file_path} is not a supported postman format")