# Searcher
Sends a bunch of requests to google using a file with queries  
Creates results.html with all given queries and their results  
Also saves htmls of sent queries to *.tmp.html files

# Prerequisites
- Install `requests`
- Install `beautifulsoup4`
```
python3 -m pip install requests beautifulsoup4
```
# Usage
```
python3 main.py <file>
```
example
```
python3 main.py example.txt
```
