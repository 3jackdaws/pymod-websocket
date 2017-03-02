import pymysql
import settings
import pymod_ws.util as util
import json


endpoint = "stickynotes"
clients = set()



def on_request(request, arguments):
    global stickynotes
    return {"stickynotes": stickynotes}

def on_message(websocket, message):
    global stickynotes, deleted_notes
    message = json.loads(message)
    action = message['action']
    if action == "new":
        note = get_note(message)
        note = create_note(note)
        stickynotes[note['id']] = note
        util.send_to_all(clients, create_alter_message(note))

    elif action == "alter":
        note = get_note(message)
        if note['id'] in stickynotes:
            content = stickynotes[note['id']]['content']
            text_changed = True
            if content == note['content']:
                text_changed = False
            stickynotes[note['id']] = note
            util.send_to_all(clients, create_alter_message(note, text_changed))
    elif action == "fetch":
        for noteid in stickynotes:
            websocket.write_message(create_alter_message(stickynotes[noteid]))

    elif action == "delete":
        id = message['id']
        deleted_notes.append(id)
        del stickynotes[id]
        util.send_to_all(clients, create_delete_message(id))
    else:
        print(message)



def on_close(websocket):
    clients.remove(websocket)

def on_open(websocket):
    clients.add(websocket)

def get_note(note):
    if "px" in note['x']:
        note['x'] = note['x'][:-2]
    if "px" in note['y']:
        note['y'] = note['y'][:-2]
    if "action" in note:
        del note['action']
    return note





stickynotes = {}
deleted_notes = []
db = settings.DATABASE['enyo']
connection = pymysql.Connect(host=db['HOST'],
                             user=db['USER'],
                             password=db['PASSWORD'],
                             database=db['NAME'],
                             cursorclass=pymysql.cursors.DictCursor)


cursor = connection.cursor()

def fetch_all_notes():
    global stickynotes
    cursor.execute("SELECT * FROM shinobu_stickynote")
    for note in cursor.fetchall():
        stickynotes[note['id']] = note

def create_note(note):
    sql = "INSERT INTO shinobu_stickynote (x,y,z,style,content) VALUES(%s,%s,%s,%s,%s)"
    cursor.execute(sql,
                   (note['x'], note['y'], note['z'], note['style'], note['content'])
                   )
    note['id'] = cursor.lastrowid
    connection.commit()
    return note

def create_alter_message(note, text_changed=True):
    note["action"] = "alter"
    if not text_changed:
        note['content'] = 0
    return json.dumps(note)

def create_delete_message(id):
    return json.dumps({
        "action":"delete",
        "id":id
    })

fetch_all_notes()
