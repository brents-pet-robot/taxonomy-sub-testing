import requests
import os
import json

def get_commits(pr_number, repo, headers):
    """ Fetch commits from a pull request """
    commits_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/commits"
    response = requests.get(commits_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        # Log error details for debugging
        print(f"Error fetching commits: {response.status_code} - {response.text}")
        return []

def extract_commit_messages(commits):
    """ Extract commit messages from commit data """
    commit_messages = []
    for commit in commits:
        if 'commit' in commit and 'message' in commit['commit']:
            commit_messages.append(commit['commit']['message'])
    return commit_messages

def find_labels_in_messages(messages, keywords):
    """ Find labels based on keywords in commit messages """
    labels = set()
    for message in messages:
        for keyword, label in keywords.items():
            if keyword.lower() in message.lower():
                labels.add(label)
    return list(labels)

def set_labels(pr_number, repo, labels, headers):
    """ Set labels to a pull request """
    labels_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/labels"
    response = requests.post(labels_url, headers=headers, json={"labels": labels})
    if response.status_code in [200, 201]:
        print(f"Successfully set labels: {labels}")
    else:
        print(f"Failed to set labels: {response.status_code} - {response.text}")

def main():
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    REPO = 'your_username/your_repository'  # Modify this to your GitHub repo
    PR_NUMBER = os.getenv('PR_NUMBER')  # PR number should be passed as an environment variable

    if not PR_NUMBER:
        raise ValueError("PR_NUMBER environment variable is required.")

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    keywords = {
        'skill': 'skill',
        'knowledge': 'knowledge'
    }

    commits = get_commits(PR_NUMBER, REPO, headers)
    if commits:
        commit_messages = extract_commit_messages(commits)
        labels_to_set = find_labels_in_messages(commit_messages, keywords)
        if labels_to_set:
            set_labels(PR_NUMBER, REPO, labels_to_set, headers)
        else:
            print("No relevant keywords found in commit messages.")
    else:
        print("No commits retrieved or error fetching commits.")

if __name__ == "__main__":
    main()
