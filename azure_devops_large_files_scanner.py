import requests
import openpyxl
from openpyxl.styles import PatternFill

# Constants
AZURE_DEVOPS_URL = 'https://dev.azure.com/{organization}/_apis/'
PERSONAL_ACCESS_TOKEN = 'your_personal_access_token'
HEADERS = {'Content-Type': 'application/json', 'Authorization': f'Bearer {PERSONAL_ACCESS_TOKEN}'}

# Function to scan repositories in a project

def scan_repositories(org, project):
    repo_url = f'{AZURE_DEVOPS_URL}{org}/{project}/_apis/git/repositories?api-version=6.0'
    repos = requests.get(repo_url, headers=HEADERS).json()
    large_files = []
    for repo in repos['value']:
        print(f'Scanning repository: {repo['name']}')
        large_files += scan_repository(org, project, repo['name'])
    return large_files

# Function to scan a single repository

def scan_repository(org, project, repo_name):
    repo_url = f'{AZURE_DEVOPS_URL}{org}/{project}/_apis/git/repositories/{repo_name}/refs?api-version=6.0'
    # logic to scan files in the repo
    # add checks for file size, etc.
    return []  # Replace with actual logic to collect large files

# Function to export to Excel

def export_to_excel(data, output_file):
    workbook = openpyxl.Workbook()
    summary_sheet = workbook.active
    summary_sheet.title = 'Summary'
    # Write summary data
    # Add other sheets: Large Files, Repository Stats, Project Stats, By Extension
    large_files_sheet = workbook.create_sheet(title='Large Files')
    # Add file entries in the sheet with formatting
    # Color code based on file size

    workbook.save(output_file)

# Entry point
if __name__ == '__main__':
    organization = 'your_organization'
    output_file_name = 'large_files_report.xlsx'
    large_files_data = []
    # Scan all projects
    projects_url = f'{AZURE_DEVOPS_URL}{organization}/_apis/projects?api-version=6.0'
    projects = requests.get(projects_url, headers=HEADERS).json()
    for project in projects['value']:
        large_files_data += scan_repositories(organization, project['name'])
    export_to_excel(large_files_data, output_file_name)

    print('Scanning completed and data exported to:', output_file_name)