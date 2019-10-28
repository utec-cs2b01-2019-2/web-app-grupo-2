from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/static/<content>')
def static_content(content):
    return render_template(content)


@app.route('/users', methods = ['GET'])
def get_users():
    session = db.getSession(engine)
    dbResponse = session.query(entities.User)
    data = []
    for user in dbResponse:
        data.append(user)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { 'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')


@app.route('/users', methods = ['PUT'])
def update_user():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(user, key, c[key])
    session.add(user)
    session.commit()
    return 'Updated User'

@app.route('/users', methods = ['DELETE'])
def delete_user():
    id = request.form['key']
    session = db.getSession(engine)
    users = session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        session.delete(user)
    session.commit()
    return "Deleted User"



@app.route('/create_test_users', methods = ['GET'])
def create_test_users():
    db_session = db.getSession(engine)
    user = entities.Word(question="how old are you", answer="Cual es tu edad?", warning="0", level="easy")
    db_session.add(user)
    db_session.commit()
    return "Test user created!"

@app.route('/users', methods = ['POST'])
def create_user():
    c =  json.loads(request.form['values'])
    user = entities.User(
        username=c['username'],
        name=c['name'],
        fullname=c['fullname'],
        password=c['password']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Created User'

@app.route('/authenticate', methods = ["POST"])
def authenticate():
    message = json.loads(request.data)
    username = message['username']
    password = message['password']
    #2. look in database
    db_session = db.getSession(engine)
    try:
        user = db_session.query(entities.User
            ).filter(entities.User.username == username
            ).filter(entities.User.password == password
            ).one()
        session['logged_user'] = user.id
        message = {'message': 'Authorized'}
        #return Response(message, status=200, mimetype='application/json')
        return Response(json.dumps(message, cls=connector.AlchemyEncoder), status=200, mimetype='applcation/json')

    except Exception:
        message = {'message': 'Unauthorized'}
        #return Response(message, status=401, mimetype='application/json')
        return Response(json.dumps(message, cls=connector.AlchemyEncoder), status=401, mimetype='applcation/json')


@app.route('/current', methods = ["GET"])
def current_user():
    try:
        db_session = db.getSession(engine)
        user = db_session.query(entities.User).filter(
            entities.User.id == session['logged_user']
            ).first()
        return Response(json.dumps(
                user,
                cls=connector.AlchemyEncoder),
                mimetype='application/json'
            )
    except:
        return render_template('parte2')

@app.route('/logout', methods = ["GET"])
def logout():
    session.clear()
    return render_template('index.html')


@app.route('/messages/<user_from_id>/<user_to_id>', methods = ['GET'])
def get_messages(user_from_id, user_to_id ):
    db_session = db.getSession(engine)
    messages = db_session.query(entities.Message).filter(
        entities.Message.user_from_id == user_from_id).filter(
        entities.Message.user_to_id == user_to_id
    )
    data = []
    for message in messages:
        data.append(message)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/gabriel/messages', methods = ["POST"])
def create_message():
    data = json.loads(request.data)
    user_to_id = data['user_to_id']
    user_from_id = data['user_from_id']
    content = data['content']
    content2 = data['content2']

    message = entities.Message(
    user_to_id = user_to_id,
    user_from_id = user_from_id,
    content = content,
    content2 = content2)


    #2. Save in database
    db_session = db.getSession(engine)
    db_session.add(message)
    db_session.commit()

    response = {'message': 'created'}
    return Response(json.dumps(response, cls=connector.AlchemyEncoder), status=200, mimetype='application/json')


@app.route('/messages', methods = ['GET'])
def get_messages2():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Message)
    data = []
    for message in dbResponse:
        data.append(message)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')




@app.route('/messages', methods = ['PUT'])
def update_message():
        session = db.getSession(engine)
        id = request.form['key']
        message = session.query(entities.Message).filter(entities.Message.id == id).first()
        c =  json.loads(request.form['values'])
        for key in c.keys():
            setattr(message, key, c[key])
        session.add(message)
        session.commit()
        return 'Updated Message Form'



@app.route('/messages', methods = ['DELETE'])
def delete_message():
        id = request.form['key']
        session = db.getSession(engine)
        messages = session.query(entities.Message).filter(entities.Message.id == id).one()
        session.delete(messages)
        session.commit()
        return "Deleted Message"


@app.route('/messages', methods = ['POST'])
def create_():
    c =  json.loads(request.form['values'])
    messages = entities.Message(
        content=c['content'],
        user_to_id=c['user_to_id'],

    )
    session = db.getSession(engine)
    session.add(messages)
    session.commit()
    return 'Created Message'










@app.route('/words', methods = ['POST'])
def create_words():
    c =  json.loads(request.form['values'])
    word = entities.Word(
        question=c['question'],
        answer=c['answer'],
        warning=c['warning'],
        level=c['level']
    )
    session = db.getSession(engine)
    session.add(word)
    session.commit()
    return 'Created words'



@app.route('/words', methods = ['GET'])
def get_words():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Word)
    data = []
    for word in dbResponse:
        data.append(word)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/words', methods = ['PUT'])
def update_word():
    session = db.getSession(engine)
    id = request.form['key']
    word = session.query(entities.Word).filter(entities.Word.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(word, key, c[key])
    session.add(word)
    session.commit()
    return 'Updated Words'


@app.route('/words', methods = ['DELETE'])
def delete_word():
    id = request.form['key']
    session = db.getSession(engine)
    words = session.query(entities.Word).filter(entities.Word.id == id)
    for word in words:
        session.delete(word)
    session.commit()
    return "Deleted Word"



@app.route('/register', methods = ['GET'])
def register():
    return render_template("register.html")

@app.route('/users2', methods = ['POST'])
def do_register():
    c = json.loads(request.form['values'])
    name = c['name']
    fullname = c['fullname']
    password = c['password']
    username = c['username']


    user = entities.User(
        username=username,
        name=name,
        fullname=fullname,
        password=password
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Created User'


@app.route('/words/<id>', methods = ['GET'])
def get_word(id):
    db_session = db.getSession(engine)
    words = db_session.query(entities.Word).filter(entities.Word.id == id)
    for word in words:
        js = json.dumps(word, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { 'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')



@app.route('/gabriel/word', methods = ["POST"])
def create_word():
    data = json.loads(request.data)
    content = data['content']
    texto = data['answer']

    response = {'message': 'created'}

    if content.lower() == texto.lower():
        response = "bien"
    else:
        response = " mal la respuesta es: "+texto


    #2. Save in database

    #db_session = db.getSession(engine)
    #db_session.add(words)
    #db_session.commit()

    return Response(json.dumps(response, cls=connector.AlchemyEncoder), status=200, mimetype='application/json')





if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=5000, threaded=True, host=('127.0.0.1'))
