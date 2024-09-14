from flask import Flask, render_template, request, redirect, url_for, g, session,jsonify
import os
import mysql.connector
import tt


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.secret_key = "69583420385748392098"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# temproary api keys

apikey = "CTNA5663344643F6"
passkey = "56563535F54tAAVBF"

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            user='root',
            host='localhost',
            password='8307802643',
            database='chetna',
            charset="utf8",
            port="3306",
        )
    return g.db

@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

def execute_query(query, data=None):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(query, data)
        db.commit()


def fetch_data(query, data=None, one=False):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(query, data)
        if one:
            return cursor.fetchone()
        return cursor.fetchall()


# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Home route to serve the HTML page
@app.route('/')
def index():
    return render_template('dboard.html')

@app.route('/landing')
def landing():
    return render_template('landing.html')



@app.route('/verf',methods=['GET','POST'])
def verify():
    return render_template('dboard.html',name = session.get('name'))


@app.route('/fetchcon',methods=["POST","GET"])
def fetchcon():
    name  = tt.faceauth()
    uname = session.get('name')
    
    if uname == name:
        print("User Authenticated")
        # return render_template('dboard.html',name = name)

        return '', 200
    else:
        print("ERROR")
        return '', 404
    # response = {
    #     'status': 'success',
    #     'received': name
    # }
   
    return jsonify(response) 
#    return name
   





@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        name  = request.form['name']
        password = request.form['password']
        cmd = "select * from user" 
        data = fetch_data(cmd)
        uname = data[0][0]
        upass = data[0][1]
       
        print(uname,upass,name,password)

        return "ok"
    return render_template('login.html')




@app.route("/getcap",methods=['POST','GET'])
def getcapp():
    uname = request.form['uname']
    session['name'] = uname
    
    return render_template('trial.html')

@app.route('/face_auth/<apikey>/<passkey>/<uname>',methods=['POST','GET'])
def faceauth(apikey, passkey, uname):
    return "ok"
   



@app.route('/flogin',methods=['POST','GET'])
def flogin():
  

       
    return render_template('f_login.html')







# Endpoint to handle video upload
@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return 'No video file uploaded', 400
    
    video = request.files['video']
    if video.filename == '':
        return 'No selected file', 400
    
    # Save the video file
    video.save(os.path.join(app.config['UPLOAD_FOLDER'], video.filename))
    return 'Video uploaded successfully', 200

if __name__ == '__main__':
    app.run(debug=True)
