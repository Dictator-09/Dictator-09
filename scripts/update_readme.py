#!/usr/bin/env python3
"""
Script to update GitHub profile README with repository statistics
"""

import os
import re
import sys
import requests
from datetime import datetime, timezone
from collections import Counter
from urllib.parse import quote

# Get environment variables
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME', 'Dictator-09')

# GitHub API headers
headers = {'Accept': 'application/vnd.github+json'}
if GITHUB_TOKEN:
    headers['Authorization'] = f'Bearer {GITHUB_TOKEN}'

# Language name to logo mapping for shield badges
LANGUAGE_LOGOS = {
    'c++': 'cplusplus',
    'c#': 'csharp',
    'objective-c': 'objectivec',
    'f#': 'fsharp',
    'javascript': 'javascript',
    'typescript': 'typescript',
    'python': 'python',
    'java': 'java',
    'go': 'go',
    'rust': 'rust',
    'ruby': 'ruby',
    'php': 'php',
    'swift': 'swift',
    'kotlin': 'kotlin',
}

def get_user_repos():
    """Fetch all repositories for the user"""
    all_repos = []
    page = 1
    per_page = 100
    
    while True:
        url = f'https://api.github.com/users/{GITHUB_USERNAME}/repos'
        params = {
            'per_page': per_page,
            'page': page,
            'sort': 'updated',
            'type': 'owner'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            repos = response.json()
            
            if not repos:
                break
                
            all_repos.extend(repos)
            
            # If we got fewer than per_page results, we're done
            if len(repos) < per_page:
                break
                
            page += 1
            
        except requests.RequestException as e:
            print(f"Error fetching repositories: {e}")
            break
    
    return all_repos

def get_user_info():
    """Fetch user profile information"""
    url = f'https://api.github.com/users/{GITHUB_USERNAME}'
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching user info: {e}")
        return {}

def calculate_stats(repos):
    """Calculate statistics from repositories"""
    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos)
    total_forks = sum(repo.get('forks_count', 0) for repo in repos)
    
    # Get language statistics
    languages = []
    for repo in repos:
        if repo.get('language'):
            languages.append(repo['language'])
    
    language_counts = Counter(languages)
    top_languages = language_counts.most_common(5)
    
    return {
        'total_stars': total_stars,
        'total_forks': total_forks,
        'total_repos': len(repos),
        'top_languages': top_languages
    }

def generate_readme(user_info, repos, stats):
    """Generate README content"""
    
    # Filter out forked repos for featured projects
    original_repos = [repo for repo in repos if not repo.get('fork')]
    
    # Get top 6 repositories by stars
    featured_repos = sorted(
        original_repos,
        key=lambda x: x.get('stargazers_count', 0),
        reverse=True
    )[:6]
    
    # Create language badges
    language_badges = []
    for lang, count in stats['top_languages']:
        # Sanitize language name for URL
        lang_lower = lang.lower()
        logo_name = LANGUAGE_LOGOS.get(lang_lower, re.sub(r'[^a-z0-9]', '', lang_lower))
        # Use consistent URL encoding
        lang_encoded = quote(lang)
        language_badges.append(f"![{lang}](https://img.shields.io/badge/-{lang_encoded}-informational?style=flat&logo={logo_name}&logoColor=white)")
    
    readme_content = f"""# Hi there! 👋 I'm {user_info.get('name', GITHUB_USERNAME)}

<div align="center">
  
[![GitHub followers](https://img.shields.io/github/followers/{GITHUB_USERNAME}?label=Followers&style=social)](https://github.com/{GITHUB_USERNAME})
[![GitHub User's stars](https://img.shields.io/github/stars/{GITHUB_USERNAME}?affiliations=OWNER&style=social)](https://github.com/{GITHUB_USERNAME})

</div>

## 📊 GitHub Statistics

<div align="center">

| 📈 Metric | 📊 Value |
|-----------|----------|
| **Total Repositories** | {stats['total_repos']} |
| **Total Stars Earned** | ⭐ {stats['total_stars']} |
| **Total Forks** | 🍴 {stats['total_forks']} |
| **Public Repos** | {user_info.get('public_repos', stats['total_repos'])} |

</div>

## 💻 Top Languages

<div align="center">

{' '.join(language_badges)}

</div>

## 🚀 Featured Projects

"""
    
    # Add featured repositories
    for i, repo in enumerate(featured_repos, 1):
        stars = repo.get('stargazers_count', 0)
        forks = repo.get('forks_count', 0)
        language = repo.get('language', 'N/A')
        description = repo.get('description', 'No description available')
        
        readme_content += f"""
### {i}. [{repo['name']}]({repo['html_url']})
{description}

**Language:** {language} | **Stars:** ⭐ {stars} | **Forks:** 🍴 {forks}

"""
    
    # Add about section if bio exists
    if user_info.get('bio'):
        readme_content += f"""
## 👨‍💻 About Me

{user_info['bio']}

"""
    
    # Add contact section
    readme_content += f"""
## 📫 How to Reach Me

- GitHub: [@{GITHUB_USERNAME}](https://github.com/{GITHUB_USERNAME})
"""
    
    if user_info.get('blog'):
        readme_content += f"- Website: [{user_info['blog']}]({user_info['blog']})\n"
    
    if user_info.get('twitter_username'):
        readme_content += f"- Twitter: [@{user_info['twitter_username']}](https://twitter.com/{user_info['twitter_username']})\n"
    
    if user_info.get('email'):
        readme_content += f"- Email: {user_info['email']}\n"
    
    # Add footer
    readme_content += f"""
---

<div align="center">

*This README is automatically updated daily with my latest repository statistics*

**Last Updated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}

</div>
"""
    
    return readme_content

def main():
    """Main function to update README"""
    print(f"Fetching data for user: {GITHUB_USERNAME}")
    
    # Fetch data
    user_info = get_user_info()
    repos = get_user_repos()
    
    if not repos:
        if not GITHUB_TOKEN:
            print("No repositories found - this is expected when running without a GITHUB_TOKEN")
            print("The workflow will have proper credentials when running in GitHub Actions")
        else:
            print("No repositories found for this user")
        sys.exit(1)
    
    print(f"Found {len(repos)} repositories")
    
    # Calculate statistics
    stats = calculate_stats(repos)
    
    # Generate README content
    readme_content = generate_readme(user_info, repos, stats)
    
    # Write to README.md
    readme_path = 'README.md'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"README.md updated successfully!")
    print(f"Total Stars: {stats['total_stars']}")
    print(f"Total Repos: {stats['total_repos']}")

if __name__ == '__main__':
    main()
