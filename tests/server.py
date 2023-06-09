from flask import Flask, request

app = Flask(__name__)

form = '''<!DOCTYPE html>
<html>
    <head>
        <title>Sample Form</title>
    </head>
    <body>
        <form method="POST" action="/">
            <label for="username">username:</label><br>
            <input type="text" id="username" name="username"><br>
            <label for="password">password:</label><br>
            <input type="password" id="password" name="password"><br>
            <input type="submit" value="submit">
        </form>
    </body>
</html>
'''

@app.route("/", methods=["GET"])
def route_get():
    print(request.headers)
    return form

@app.route("/", methods=["POST"])
def route_post():
    print(request.headers)
    print(request.form)
    username = request.form.get('username')
    password = request.form.get('password')
    return f'username：{username}, password：{password}'

if __name__ == "__main__":
    app.run()