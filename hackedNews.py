from flask import Flask, render_template
import requests

app = Flask(__name__, static_folder='static_folder')

@app.route('/')
def home():
	url = "https://hacker-news.firebaseio.com/v0/topstories.json"
	payload = "{}"
	response = requests.request("GET", url, data=payload)

	temp = response.json()

	responses = []

	for article in temp[:30]:
		url = "https://hacker-news.firebaseio.com/v0/item/{}.json".format(article)
		payload = "{}"
		response = requests.request("GET", url, data=payload)
		responses.append(response.json())

	return render_template('index.html', data=responses)

if __name__ == '__main__':
   app.run()
