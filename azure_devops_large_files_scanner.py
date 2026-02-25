import requests
import pandas as pd

class AzureDevOpsOrgScanner:
    def __init__(self, organization, token):
        self.organization = organization
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        self.large_files = []
        self.project_stats = {}
        self.repo_stats = {}

    def scan_projects(self):
        projects_url = f'https://dev.azure.com/{self.organization}/_apis/projects?api-version=6.0'
        response = requests.get(projects_url, headers=self.headers)
        projects = response.json().get('value', [])

        for project in projects:
            self.scan_repositories(project['name'])

    def scan_repositories(self, project_name):
        repos_url = f'https://dev.azure.com/{self.organization}/{project_name}/_apis/git/repositories?api-version=6.0'
        response = requests.get(repos_url, headers=self.headers)
        repos = response.json().get('value', [])

        for repo in repos:
            self.get_file_information(repo['name'], project_name)

    def get_file_information(self, repository_name, project_name):
        # This method should ideally list all files in the repo and check their sizes
        # Placeholder for actual implementation, assume we get file sizes and names
        files = []  # Replace this with actual logic to get files

        for file in files:
            size = self.get_file_size(file)
            if size >= 100 * 1024 * 1024:  # Files >= 100MB
                self.large_files.append((file, size))
                self.update_stats(repo_name=repository_name, project_name=project_name, size=size)

    def get_file_size(self, file):
        # Placeholder for getting file size
        return 0  # Replace with actual logic to get file size

    def update_stats(self, repo_name, project_name, size):
        if project_name not in self.project_stats:
            self.project_stats[project_name] = 0
        self.project_stats[project_name] += size

        if repo_name not in self.repo_stats:
            self.repo_stats[repo_name] = 0
        self.repo_stats[repo_name] += size

    def create_excel_report(self):
        with pd.ExcelWriter('AzureDevOps_Large_Files_Report.xlsx', engine='xlsxwriter') as writer:
            self.create_summary_sheet(writer)
            self.create_large_files_sheet(writer)
            self.create_repository_stats_sheet(writer)
            self.create_project_stats_sheet(writer)
            self.create_by_extension_sheet(writer)

    def create_summary_sheet(self, writer):
        summary_df = pd.DataFrame(self.project_stats.items(), columns=['Project', 'Total Size'])
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

    def create_large_files_sheet(self, writer):
        large_files_df = pd.DataFrame(self.large_files, columns=['File', 'Size'])

        # Add formatting for large files
        workbook = writer.book
        worksheet = writer.sheets['Large Files']
        # Format settings can be added here

        large_files_df.to_excel(writer, sheet_name='Large Files', index=False)

    def create_repository_stats_sheet(self, writer):
        repo_df = pd.DataFrame(self.repo_stats.items(), columns=['Repository', 'Total Size'])
        repo_df.to_excel(writer, sheet_name='Repository Stats', index=False)

    def create_project_stats_sheet(self, writer):
        project_df = pd.DataFrame(self.project_stats.items(), columns=['Project', 'Total Size'])
        project_df.to_excel(writer, sheet_name='Project Stats', index=False)

    def create_by_extension_sheet(self, writer):
        # Logic to categorize by file extension
        ext_df = pd.DataFrame()  # Replace with actual data
        ext_df.to_excel(writer, sheet_name='By Extension', index=False)

# Example usage:
# scanner = AzureDevOpsOrgScanner('your_organization', 'your_token')
# scanner.scan_projects()
# scanner.create_excel_report()