import argparse
import os
from libpostmanhttp.postman_to_vscode_restclient import postman_to_http
from pathlib import Path

        

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