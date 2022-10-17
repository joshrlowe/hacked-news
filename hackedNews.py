from flask import Flask, render_template
app = Flask(__name__, static_folder='static_folder')

@app.route('/')
def home():
	return render_template('index.html')

@app.rout('/test')
def test():
        return "hey"

if __name__ == '__main__':
   app.run()
