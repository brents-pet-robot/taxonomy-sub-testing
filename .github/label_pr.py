import requests
import os
import json

def get_commits(pr_number, repo, headers):
    """ Fetch commits from a pull request """
    commits_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/commits"
    response = requests.get(commits_url, headers=headers)
    return response.json()

def check_keywords(commit_messages, keywords):
    """ Check if commit messages contain specific keywords """
    labels = set()
    for message in commit_messages:
        for keyword, label in keywords.items():
            if keyword.lower() in message.lower():
                labels.add(label)
    return list(labels)

def set_labels(pr_number, repo, labels, headers):
    """ Set labels to a pull request """
    labels_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/labels"
    data = json.dumps({"labels": labels})
    response = requests.post(labels_url, headers=headers, data=data)
    return response.status_code

def main():
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    REPO = 'your_username/your_repository'  # Change this to your repository
    PR_NUMBER = os.getenv('PR_NUMBER')  # Pass this environment variable when running the script

    if not PR_NUMBER:
        raise ValueError("PR_NUMBER environment variable is required.")

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Define keywords and their corresponding labels
    keywords = {
        'skill': 'skill',
        'knowledge': 'knowledge'
    }

    commits = get_commits(PR_NUMBER, REPO, headers)
    commit_messages = [commit['commit']['message'] for commit in commits]
    labels = check_keywords(commit_messages, keywords)

    if labels:
        status = set_labels(PR_NUMBER, REPO, labels, headers)
        print(f"Labels {labels} set to PR #{PR_NUMBER} with status {status}")
    else:
        print("No relevant keywords found in commit messages.")

if __name__ == "__main__":
    main()
