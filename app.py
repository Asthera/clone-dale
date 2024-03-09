from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    # HTML content as a Python string
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Simple App</title>
    </head>
    <body>
        <h1>Welcome to Our Simple Flask App</h1>
        <p>This page is served directly from the Flask route. </p>
    </body>
    </html>
    """
    return html_content


if __name__ == '__main__':
    app.run(debug=True)
