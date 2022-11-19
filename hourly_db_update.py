import sqlite3
import requests

# Database connection
conn = sqlite3.connect('/home/fagan/hackedNews/users.db')
c = conn.cursor()

url = "https://hacker-news.firebaseio.com/v0/topstories.json"
payload = "{}"
response = requests.request("GET", url, data=payload)

temp = response.json()
responses = []

# Load all of the API results
for article in temp[:100]:
	url = "https://hacker-news.firebaseio.com/v0/item/{}.json".format(article)
	payload = "{}"
	response = requests.request("GET", url, data=payload)
	responses.append(response.json())

# Remove all of the articles that are older than an hour 
c.execute("DELETE FROM Articles WHERE date(timestamp) < date('now', '-1 day')")

# Adding all of the articles to our database
for article in responses:
	c.execute('SELECT article_id FROM Articles WHERE article_id=' + str(article['id']))
	temp_result = c.fetchall()

	if len(temp_result) == 0:
		try:
			query_str = "INSERT INTO Articles VALUES('{id}', '{by}', '{title}', '{url}', NULL, CURRENT_TIMESTAMP)".format(id=str(article['id']), by=str(article['by']), title=str(article['title']), url=str(article['url']))
			c.execute(query_str)
		except:
			pass

conn.commit()
conn.close()

