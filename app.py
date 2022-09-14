from flask import Flask, request, redirect

app = Flask(__name__)

words = [
    {'id':1, 'english':'whale', 'korean':'고래'},
    {'id':2, 'english':'age', 'korean':'나이'}
]
nextId = len(words) + 1

def template(content, id=None):
    detailHtml = ''
    if id != None:
        detailHtml = f'''
        <ul>
        <li><a href="/update/{id}">update</a></li>
        <li><a href="/delete/{id}">delete</a></li>
        </ul>
        '''
    html = f'''<html><head></head><body>
            <h1><a href="/">단어장</a></h1>
            <ol>
                <li><a href="/random/">random</a></li>
                <li><a href="/reads/">reads</a></li>
                <li><a href="/create/">create</a></li>
            </ol>
            {content}
            {detailHtml}
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
        return redirect(f'/read/{newword["nextId"]}')

@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    english = ''
    korean = ''
    for word in words:
        if id == word['id']:
            english = word['english']
            korean = word['korean']
            break

    if request.method == 'GET':
        content = f'''<form action="/update/" method="POST">
            <p><input type="text" name="english" placeholder="영어단어" value="{english}"></p>
            <p><textarea name="korean" placeholder="뜻">{korean}</textarea></p>
            <p><input type="submit" value="update"></p>
            </form>'''
        return template(content)
    elif request.method == 'POST':
        global nextId
        english = request.form['english']
        korean = request.form['korean']
        newword = {'id':nextId, 'english':english, 'korean':korean}
        words.append(newword)
        nextId += 1
        return redirect(f'/read/{newword["nextId"]}')

@app.route('/reads/')
def reads():
    liTags = ''
    for word in words:
        liTags += f'''<li><a href="/read/{word["id"]}">{word["english"]}</a> {word["korean"]}</li>'''
    return template(liTags)

@app.route('/read/<int:id>/')
def read(id):
    english = ''
    korean = ''
    for word in words:
        if id == word['id']:
            english = word['english']
            korean = word['korean']
            break
    content = f'''<h2>{english}</h2>
    <p>{korean}</p>'''
    return template(content, id)

if __name__ == '__main__':
    app.run(debug=True)
