# Dynamic GitHub Profile README

This repository contains an automated system that generates a dynamic GitHub profile README based on your repositories.

## 🎯 Features

- **Automatic Updates**: GitHub Actions workflow runs daily at midnight UTC
- **Repository Statistics**: Shows total repos, stars, and forks
- **Top Languages**: Displays your most-used programming languages
- **Featured Projects**: Highlights your top 6 repositories by stars
- **Dynamic Content**: All statistics update automatically from your GitHub data

## 📁 Project Structure

```
.
├── .github/
│   └── workflows/
│       └── update-readme.yml    # GitHub Actions workflow
├── scripts/
│   └── update_readme.py         # Python script to fetch and generate README
└── README.md                     # Your profile README (auto-generated)
```

## 🚀 How It Works

1. **GitHub Actions Workflow** (`.github/workflows/update-readme.yml`):
   - Runs on a schedule (daily at midnight UTC)
   - Can be manually triggered via workflow_dispatch
   - Runs on push to main branch
   - Sets up Python environment and installs dependencies
   - Executes the update script
   - Commits and pushes changes if README was updated

2. **Update Script** (`scripts/update_readme.py`):
   - Fetches your repositories using GitHub API
   - Calculates statistics (stars, forks, languages)
   - Identifies your top projects
   - Generates formatted README content
   - Writes the new content to README.md

## 🔧 Setup

The system is already configured and ready to use! When you push to the `main` branch:

1. The workflow will run automatically
2. Your README will be generated with real data from your repositories
3. The workflow will commit the updated README back to your repository

## ⚙️ Customization

You can customize the generated README by editing `scripts/update_readme.py`:

- Change the number of featured projects (default: 6)
- Modify the number of top languages displayed (default: 5)
- Adjust the README template and formatting
- Add additional statistics or sections

## 🔐 Permissions

The workflow uses `GITHUB_TOKEN` which is automatically provided by GitHub Actions with the necessary permissions to:
- Read repository data
- Commit changes to the repository

## 🎨 Manual Trigger

You can manually trigger the workflow:
1. Go to the "Actions" tab in your repository
2. Select "Update README" workflow
3. Click "Run workflow"

## 📝 Notes

- The workflow requires `contents: write` permission to commit changes
- The script handles API rate limiting gracefully
- Only non-forked repositories are featured in the projects section
- The README will show "Auto-updating" placeholders until the first workflow run completes

## 🤝 Contributing

Feel free to fork this repository and customize it for your own profile!
