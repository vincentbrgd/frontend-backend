import json
from flask import Flask
import requests
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask import request
from flask import render_template
VERSION = "1.0"  
app = Flask(__name__)


db_name = 'chat.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

db = SQLAlchemy(app)

class Note(db.Model):
    __tablename__ = 'notes'
    note_id = db.Column(db.Integer, primary_key=True)
    note_title = db.Column(db.String)
    note_content = db.Column(db.String)
    note_done = db.Column(db.Boolean)



with app.app_context():
    db.create_all()

@app.route('/')
def home():
    
    return redirect('/front/notes')

@app.route('/db/status')
def check_db_status():
    
    try:
        result = db.session.execute(text('SELECT 1'))
        print(result)
        return dict(status="healthy", message="Database is functioning correctly")
    except Exception as err:
        
        error_mess = "<p>The error:<br>" + str(err) + "</p>"
        hed = '<h1>Something went wrong.</h1>'
        return hed + error_mess
    
@app.route('/api/notes', methods=['POST'])
def create_note():
   
    try:
        parameters = json.loads(request.data)
        note_title = parameters['title']
        note_content = parameters['content']
        note_done = parameters['done']
        print("note created successfully")
      
        new_note = Note(note_title=note_title, note_content=note_content, note_done=note_done)
        db.session.add(new_note)
        db.session.commit()
        return "Note created successfully"
    except Exception as exc:
        return dict(error=f"{type(exc)}: {exc}"), 422

@app.route('/api/notes', methods=['GET'])
def get_all_notes():
   
    notes = Note.query.all()
    return [dict(
            note_id=note.id, note_title=note.title, note_content=note.content, note_done=note.done)
        for note in notes]

@app.route('/api/notes/<int:id>/done', methods=['POST'])
def update_note_done_status(id):
    try:
        
        parameters = json.loads(request.data)
        note_done = parameters['done']

        
        note = Note.query.get(id)
        if not note:
            return dict(error="Note not found"), 404

        note.note_done = note_done
        db.session.commit()

        return dict(ok="ok")
    except Exception as exc:
        return dict(error=f"{type(exc)}: {exc}"), 422

@app.route('/api/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    
    try:
        
        note = Note.query.get(id)
        if not note:
            return dict(error="Note not found"), 404

        
        db.session.delete(note)
        db.session.commit()

        return dict(ok="ok")
    except Exception as exc:
        return dict(error=f"{type(exc)}: {exc}"), 422


@app.route('/front/notes')
def front_notes():
    
    url = request.url_root + '/api/notes'
    req = requests.get(url)
    if not (200 <= req.status_code < 300):
     
        return dict(error=f"could not request notes list", url=url,
                    status=req.status_code, text=req.text)
    notes = req.json()
    return render_template('notes.html.j2', notes=notes, version=VERSION)


if __name__ == '__main__':
    app.run()