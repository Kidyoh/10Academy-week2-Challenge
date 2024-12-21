mkdir tellco-analysis
cd tellco-analysis

# Create main directories
mkdir -p .vscode .github/workflows src notebooks tests scripts

# Create initial files
touch .gitignore README.md requirements.txt
touch src/__init__.py
touch notebooks/__init__.py notebooks/README.md
touch tests/__init__.py
touch scripts/__init__.py scripts/README.md 