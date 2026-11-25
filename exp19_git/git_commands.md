# Experiment 19: Git and GitHub

## One-time setup
```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
```

## Initialise and commit
```bash
cd my-web-project
git init
git status
git add README.md
git commit -m "Add README"
git add .
git commit -m "Add project files for Flask blog"
git log --oneline
```

## Push to GitHub
1. On github.com create a new empty repository (e.g. `web-lab-project`).
2. Then:
```bash
git branch -M main
git remote add origin https://github.com/<username>/web-lab-project.git
git push -u origin main
```
(GitHub asks for a Personal Access Token instead of a password.)

## Later changes
```bash
git add .
git commit -m "Describe the change"
git push
```

## Useful extras
```bash
git diff            # see unstaged changes
git branch feature  # create branch
git checkout feature
git merge feature
git clone <repo-url>
```
