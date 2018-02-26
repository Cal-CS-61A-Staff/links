from flask import Flask, redirect
import requests
import csv
import os

app = Flask(__name__)

links = {}
author = {}

@app.route('/<path>/')
def handler(path):
    if not links:
        refresh()
    if path in links:
        return redirect(links[path])
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
    csv_lines = []
    for url in os.getenv('DB_URL').split(','):
        csv_lines += requests.get(os.getenv('DB_URL')).text.split("\n")
    csvr = list(csv.reader(csv_lines, delimiter=',', quotechar='"'))
    headers = [x.lower() for x in csvr[0]]
    new_links, new_author = {}, {}
    for row in csvr[1:]:
        shortlink = row[headers.index('shortlink')]
        url = row[headers.index('url')]
        creator = row[headers.index('creator')]
        new_links[shortlink] = url
        new_author[shortlink] = creator
    links = new_links, author = new_author
    return 'Links updated'

if __name__ == "__main__":
    app.run()