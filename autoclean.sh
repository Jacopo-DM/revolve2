ruff clean
black . --line-length 80
ruff format . --preview
ruff check . --fix --unsafe-fixes
sourcery review . --fix --config /Users/jmdm/Documents/Projects/Thesis/code/r2j/.sourcery.yaml