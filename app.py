from flask import Flask, request, redirect

app = Flask(__name__)

words = [
    {'id':1, 'english':'whale', 'korean':'고래'},
    {'id':2, 'english':'age', 'korean':'나이'}
]
nextId = len(words) + 1

def template(content):
    html = f'''<html><head></head><body>
            <h1><a href="/">단어장</a></h1>
            <ol>
                <li><a href="/random/">random</a></li>
                <li><a href="/reads/">reads</a></li>
                <li><a href="/create/">create</a></li>
            </ol>
            {content}
        </body></html>'''
    
    return html

@app.route('/')
def index():
    content = '''<h2>Whalecoding 단어장</h2>
    <p>환영합니다</p>'''
    return template(content)

@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        content = '''<form action="/create/" method="POST">
            <p><input type="text" name="english" placeholder="영어단어"></p>
            <p><textarea name="korean" placeholder="뜻"></textarea></p>
            <p><input type="submit" value="create"></p>
            </form>'''
        return template(content)
    elif request.method == 'POST':
        global nextId
        english = request.form['english']
        korean = request.form['korean']
        newword = {'id':nextId, 'english':english, 'korean':korean}
        words.append(newword)
        nextId += 1
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
