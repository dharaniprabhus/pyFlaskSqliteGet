from flask import Flask, Response, request, render_template, g, send_file
import sys
import sqlite3
import io

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("static/db/images.db")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, arg):
    cur = get_db().execute(query, [arg])
    row = cur.fetchone()
    cur.close()
    return row[0] if row else None

@app.route("/download/<id>")
def download(id):
    cur = get_db().cursor()
    img = query_db('SELECT data from images where id = ?', id)
    if img is None:
        print ("Image with id = 2 not found", file=sys.stderr)
        return render_template("index.html")
    else:
        print ("Image with id = 2 found", file=sys.stderr)
        print (type(img), file=sys.stderr)
        return send_file(io.BytesIO(img), attachment_filename='img.png', as_attachment=True, mimetype='application/blob')

if __name__ == "__main__":
    app.run(debug=True)
