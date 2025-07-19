# scrapers/github.py

import requests
import os

def fetch_latest_github_release(owner, repo):
    """
    Fetch the latest GitHub release using the GitHub API.
    """
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
        
        # Add GitHub token if available for higher rate limits
        headers = {}
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        
        data = resp.json()
        release_name = data.get("name", "")
        release_body = data.get("body", "")
        
        if release_name and release_body:
            return f"{release_name}: {release_body[:500]}..."
        elif release_name:
            return release_name
        elif release_body:
            return release_body[:500] + "..."
        
        return None
    except Exception as e:
        print(f"Error fetching GitHub release for {owner}/{repo}: {e}")
        return None

def fetch_github_commits(owner, repo, branch="main"):
    """
    Fetch recent commits from a GitHub repository.
    """
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        params = {"sha": branch, "per_page": 5}
        
        headers = {}
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        
        commits = resp.json()
        if commits:
            latest_commit = commits[0]
            commit_message = latest_commit.get("commit", {}).get("message", "")
            author = latest_commit.get("commit", {}).get("author", {}).get("name", "")
            
            return f"Latest commit by {author}: {commit_message}"
        
        return None
    except Exception as e:
        print(f"Error fetching GitHub commits for {owner}/{repo}: {e}")
        return None 