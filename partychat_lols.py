from flask import Flask, render_template
from connect_mongo import connect_db
from gridfs import GridFS
from bson import objectid
import os

app = Flask(__name__)

@app.route("/")
def index():
    db = connect_db().message
    items = list(db.find({ '$or' : [ {'urls':{'$exists':True}}, {'imgs':{'$exists':True}}] }, sort=[('time', -1)], limit=15))
    for i in items:
        if "tags" in i:
            i["tags"] = ", ".join(["#%s" % (x) for x in i["tags"]])
    return render_template("index.html", title="Home", items=items, items_len=len(items))

@app.route("/thumb/<thumb_id>")
def thumb(thumb_id):
    fs = connect_db()
    fs = GridFS(fs, "thumbnail")
    f = fs.get(objectid.ObjectId(thumb_id))
    f = f.read()
    return app.response_class(f, mimetype="image/png")

if __name__ == "__main__":
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)