import requests
import nbformat
import os
import subprocess
from base64 import b64encode



def generate_requirements_file(repo_location):
    
    MY_TOKEN = os.getenv('GITHUB_TOKEN')
    
    headers = {
        "Authorization": f"Bearer {MY_TOKEN}"
    }

    owner = 'learn-co-curriculum'
    repo_name = repo_location.split('/')[-1]
    # GitHub API endpoint to get the default branch name
    api_url = f"https://api.github.com/repos/{owner}/{repo_name}"
    print(f'Working on {api_url}')
    response = requests.get(api_url, headers=headers)
    response_data = response.json()
    default_branch = response_data['default_branch']
    
    # URL for the Jupyter notebook in the default branch
    notebook_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/{default_branch}/index.ipynb"
    
    try:
        # Fetch notebook content
        notebook_response = requests.get(notebook_url)
        notebook_content = notebook_response.text
        
        # Parse notebook content using nbformat
        nb = nbformat.reads(notebook_content, as_version=nbformat.NO_CONVERT)
        
        # Create a temporary directory to work in
        temp_dir = 'temp'
        os.makedirs(temp_dir, exist_ok=True)
        
        # Extract Python code from notebook cells
        python_code = []
        for cell in nb.cells:
            if cell.cell_type == 'code':
                python_code.append(cell.source)
        
        # Save the extracted Python code to a temporary .py file
        temp_py_file = os.path.join(temp_dir, 'notebook_code.py')
        with open(temp_py_file, 'w') as f:
            f.write('\n'.join(python_code))
        
        # Run pipreqs to generate the requirements.txt file
        if len(python_code) > 0:
            requirements_file = os.path.join(temp_dir, 'requirements.txt')
            try:
                subprocess.run(['pipreqs', temp_dir], check=True)

            
                # Read the generated requirements.txt content
                with open(requirements_file, 'r') as f:
                    requirements_content_list = f.readlines()
                with open(requirements_file, 'r') as f:
                    requirements_content = f.read()
                
                # Remove the temporary directory
                os.remove(temp_py_file)
                os.remove(requirements_file)
                os.rmdir(temp_dir)
                master_file = os.path.join(os.getcwd(), 'master.txt')
                with open(master_file, 'r') as d:
                    master_contents = d.readlines()
                
                new_packages = []
                
                for p in requirements_content_list:
                    if p in master_contents:
                        continue
                    else:
                        new_packages.append(p)
                    
                
                with open(master_file, 'a') as f:
                    f.writelines(new_packages)
                
            # Create or update requirements.txt in the repository's env folder
                env_folder_url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/env/"
                headers = {
                    "Authorization": f"Bearer {MY_TOKEN}"
                }
                
                # Check if the env folder exists, and create it if necessary
                response = requests.get(env_folder_url, headers=headers)
                if response.status_code == 404:
                    env_folder_data = {
                        "message": "Creating env folder",
                        "content": b64encode(''.encode()).decode(),
                        "branch": default_branch
                    }
                    response = requests.put(env_folder_url, json=env_folder_data, headers=headers)
                
                # Create or update requirements.txt within the env folder
                requirements_url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/env/requirements.txt"
                requirements_data = {
                    "message": "Updating requirements",
                    "content": b64encode(requirements_content.encode()).decode(),
                    "branch": default_branch
                }
                response = requests.put(requirements_url, json=requirements_data, headers=headers)
                
                if response.status_code >= 200 and response.status_code < 300:
                    print("requirements.txt file updated successfully.")
                else:
                    print("Error updating requirements.txt file.", "\n", response.status_code, "\n", response.text)
            except:
                print('error in py code, requirements file not created')

        else:
            os.remove(temp_py_file)
            os.rmdir(temp_dir)
            print('There are no code cells in this lesson')
    except:
        print('no notebook in this repository')
    
# Example usage
# generate_requirements_file("https://github.com/username/repo-name")
