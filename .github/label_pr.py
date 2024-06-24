import requests
import os
import json

def get_commits(repo, pr_number, token):
    """ Fetch commits from a pull request """
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/commits"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching commits: {response.status_code} - {response.text}")
        return []

def extract_commit_messages(commits):
    """ Extract commit messages from the commit data """
    return [commit['commit']['message'] for commit in commits]

def set_labels(repo, pr_number, labels, token):
    """ Set labels to a pull request """
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/labels"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, headers=headers, json={"labels": labels})
    if response.status_code in [200, 201]:
        print("Labels set successfully:", labels)
    else:
        print("Failed to set labels:", response.status_code, "-", response.text)

def main():
    token = os.getenv('GITHUB_TOKEN')
    repo = 'your_username/your_repository'  # Modify with your GitHub username and repository name
    pr_number = os.getenv('PR_NUMBER')

    if not pr_number:
        raise ValueError("PR_NUMBER environment variable is required.")

    commits = get_commits(repo, pr_number, token)
    if commits:
        commit_messages = extract_commit_messages(commits)
        labels = [label for keyword, label in {
            'skill': 'skill',
            'knowledge': 'knowledge'
        }.items() if any(keyword in message.lower() for message in commit_messages)]
        if labels:
            set_labels(repo, pr_number, labels, token)
        else:
            print("No relevant keywords found in commit messages.")
    else:
        print("No commits retrieved or error fetching commits.")

if __name__ == "__main__":
    main()
