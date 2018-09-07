from flask import Flask, redirect, request
import requests
import csv
import os

try:
    import urlparse  # Python 2
except ImportError:
    import urllib.parse as urlparse  # Python 3

def add_url_params(url, params_string):
    parse_result = list(urlparse.urlsplit(url))
    parse_result[3] = "&".join(filter(lambda s: s, [parse_result[3], params_string]))
    return urlparse.urlunsplit(tuple(parse_result))

app = Flask(__name__)

links, author = {}, {}

@app.route('/<path>/')
def handler(path):
    if not links:
        refresh()
    if path in links:
        return redirect(add_url_params(links[path], request.query_string))
    return base()

@app.route('/preview/<path>/')
def preview(path):
    if not links:
        refresh()
    if path not in links:
        return 'No such link exists.'
    return 'Points to <a href="{0}">{0}</a> by {1}'.format(links[path], author[path])

@app.route("/")
def base():
    return redirect('https://cs61a.org')

@app.route("/_refresh/")
def refresh():
    links.clear()
    author.clear()
    for sheet_id in os.getenv('SHEETS').split(','):
        url = os.getenv('BASE_URL') + sheet_id
        csv_lines = requests.get(url).text.split("\n")
        csvr = list(csv.reader(csv_lines, delimiter=',', quotechar='"'))
        headers = [x.lower() for x in csvr[0]]
        for row in csvr[1:]:
            shortlink = row[headers.index('shortlink')]
            url = row[headers.index('url')]
            creator = row[headers.index('creator')]
            links[shortlink] = url
            author[shortlink] = creator
    return 'Links updated'

if __name__ == "__main__":
    app.run()