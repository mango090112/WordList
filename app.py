from flask import Flask, request, redirect, render_template
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

@app.route('/')
def index():
    titleString = 'Whalecoding 단어장'
    contentString = '환영합니다.'
    return render_template('index.html', title=titleString, content=contentString)

@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        global nextId
        english = request.form['english']
        korean = request.form['korean']
        newword = {'id':nextId, 'english':english, 'korean':korean}
        words.append(newword)
        nextId += 1
        return redirect(f'/read/{newword["id"]}')

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
        return render_template('update.html', english=english, korean=korean, id=id)
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
    return render_template('reads.html', words=words)

@app.route('/read/<int:id>/')
def read(id):
    english = ''
    korean = ''
    for word in words:
        if id == word['id']:
            english = word['english']
            korean = word['korean']
            break
    return render_template('read.html', english=english, korean=korean, id=id)

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
    answer=sample[0]
    random.shuffle(sample)

    return render_template('random.html', sample=sample, answer=answer)

@app.route('/random2/')
def randomWord2():
    sample = random.sample(words, 4)
    answer=sample[0]
    random.shuffle(sample)
    return render_template('random2.html', sample=sample, answer=answer)

if __name__ == '__main__':
    app.run(debug=True)
