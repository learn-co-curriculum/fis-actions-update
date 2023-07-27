# Code README

This repository contains code that interacts with GitHub's API to check and add files to a specified GitHub repository. It includes functions to check the contents and branches of a repository and add necessary files to it. Additionally, there is a usage example provided that demonstrates how to parse a list of phases and add the required files to each repository.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Checking Repository Contents](#checking-repository-contents)
  - [Checking Repository Branch](#checking-repository-branch)
  - [Adding Files to Repository](#adding-files-to-repository)
  - [Usage Example](#usage-example)

## Prerequisites
- Python 3.6 or above
- `git` module
- `shutil` module
- `os` module
- `requests` module
- `pandas` library

## Installation
1. Clone the repository from the following link:
    <a href="https://github.com/learn-co-curriculum/fis-actions-update">FIS actions updater repository on GitHub</a>

2. Change into the repository directory:

3. Install the required dependencies if you do not already have them installed.

## Usage


### Checking Repository Branch
The `check_branch` function checks if a repository contains a specific branch.

```python
def check_branch(repo_location):
    """
    Checks the repository for a curriculum branch which is necessary for the GitHub Actions to function.

    Args:
        repo_location (str): Full repository URL.

    Returns:
        bool: True if the repository contains a curriculum branch.
    """
```

### Adding Files to Repository
The `add_files_to_repo` function adds the necessary files to a repository.



### Usage Example
The following example demonstrates how to parse a list of phase numbers and create a csv of the repositories in a course. Each repository will then be updated with the necessary actions files if they are not already present in the repo.

```python

# List of phases and courses
list_of_phases = [("phase1", "course1"), ("phase2", "course2"), ("phase3", "course3")]

for phase, course in list_of_phases:
    os.system(f"github-to-canvas --query {course} > phase_{phase}_canvas.yml")
    os.system(f"github-to-canvas --map phase_{phase}_canvas.yml --urls-only > phase_{phase}_canvas.csv")
    df = pd.read_csv(f'phase_{phase}_canvas.csv')
    df.columns = ['url']

    completed = []
    for i, item in df.iterrows():
        add_files_to_repo(item['url'])
        completed.append(i)
    df = df.drop(df.index[completed])
```

Note: Replace the URLs in the example with the URLs you want to add files to.

**Important**: Before running the example, make sure to set the `GITHUB_TOKEN` environment variable with a valid GitHub personal access token.

For more details on how to obtain a personal access token, refer to the official GitHub documentation: [Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating

-a-personal-access-token)

---
Please ensure that you have the necessary permissions and access rights before performing any operations on the repositories.