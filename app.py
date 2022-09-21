from flask import Flask, request, redirect
import random

app = Flask(__name__)

words = [
    {'id':1, 'english':'whale', 'korean':'고래'},
    {'id':2, 'english':'age', 'korean':'나이'},
    {'id':3, 'english':'ago', 'korean':'이전에'},
    {'id':4, 'english':'activity', 'korean':'활동'},
    {'id':5, 'english':'take', 'korean':'가져가다'},
    {'id':6, 'english':'problem', 'korean':'문제'},
    {'id':7, 'english':'also', 'korean':'또한'},
    {'id':8, 'english':'future', 'korean':'미래'},
    {'id':9, 'english':'language', 'korean':'언어'},
    {'id':10, 'english':'dialogue', 'korean':'대화'},
]
nextId = len(words) + 1

def template(content, id=None):
    detailHtml = ''
    if id != None:
        detailHtml = f'''
        <ul>
        <li><a href="/update/{id}/">update</a></li>
        <li><form action="/delete/{id}/" method="POST">
        <input type="submit" value="delete"></form></li>
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
    if request.method == 'GET':
        english = ''
        korean = ''
        for word in words:
            if id == word['id']:
                english = word['english']
                korean = word['korean']
                break
        content = f'''<form action="/update/{id}" method="POST">
            <p><input type="text" name="english" placeholder="영어단어" value="{english}"></p>
            <p><textarea name="korean" placeholder="뜻">{korean}</textarea></p>
            <p><input type="submit" value="update"></p>
            </form>'''
        return template(content)
    elif request.method == 'POST':
        redirectId = 0
        for word in words:
            if id == word['id']:
                redirectId = id
                english = word['english'] = request.form['english']
                korean = word['korean'] = request.form['korean']
                break
        return redirect(f'/read/{redirectId}/')

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

@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for word in words:
        if id == word['id']:
            words.remove(word)
            break
    return redirect(f'/reads/')

@app.route('/random/')
def randomWord():
    sample = random.sample(words, 4)
    answer = sample[0]
    liTag = ''
    random.shuffle(sample)
    for word in sample:
        liTag += f'<li>{word["korean"]}</li>'
    content = f'''<h2>{answer["english"]}</h2>
    <ol>
    {liTag}
    </ol>    
    <p><details><summary>정답</summary>
    {answer["english"]}, {answer["korean"]}</details></p>
    <br/>
    <a href="/random/">next</a>'''
    return template(content)

if __name__ == '__main__':
    app.run(debug=True)
