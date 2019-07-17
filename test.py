from flask import Flask, render_template, request, url_for, jsonify


app = Flask(__name__)




@app.route('/hello')
def hello():
	return "stefano is gay"


if __name__ == "__main__":
  app.run()
