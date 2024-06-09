import json
import argparse
import os
from utils.print_utils import print_item, print_file_variables
from pathlib import Path




def postman_to_http(input_file_path, output_file_path):
    with open(input_file_path, 'r') as f:
        postman_collection = json.load(f)
       
        if 'item' in postman_collection and len(postman_collection['item']) > 0 and 'item' in postman_collection['item'][0]:
            print(f"Reading {input_file_path}")
            for chapter in postman_collection['item']:
                chapter_output_filename = os.path.join(output_file_path,chapter['name']+".http")
                with open(chapter_output_filename, 'w') as f:
                    
                    print_file_variables(f)

                    # itemsColl = [item for items in postman_collection['item'] for item in items['item']]
                    itemsColl = chapter['item']
                    for item in itemsColl:
                    
                        print_item(f, item)
                print(f"Saving {chapter_output_filename}")

        else: 
            print(f"{input_file_path} is not a supported postman format")
            

def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--postmandir",required=True,help="Path to postman export json files")
    ap.add_argument("-o", "--httpdir",required=True,help="Path to http vscode rest client files")

    # Parsing console params
    args = vars(ap.parse_args())

    # Read and write directories
    postman_dir = Path(args['postmandir'])
    httpdir = Path(args['httpdir'])

    # Postman files from read directori
    postman_files = [f for f in postman_dir.iterdir()]


    # For each postman file a http file is created
    for postman_file in postman_files:
        name = Path(postman_file).name
        name_http = name.replace(".json", "")
        dir_http = os.path.join(httpdir, name_http)
        os.makedirs(dir_http, exist_ok=True)
        postman_to_http(postman_file, dir_http)    


           
if __name__ == "__main__":
    main()