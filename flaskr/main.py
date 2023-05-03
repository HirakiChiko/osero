from flaskr import app
from flask import render_template,request,redirect,url_for,jsonify
from flaskr import osero_main
import json

osero = osero_main.Osero()

@app.route('/')
def index():
    return render_template(
        'index.html' 
    )

@app.route('/get_board')
def get_board():
    response_data = {
        'board' : osero.board,
        'e_message' : osero.error_message,
        'q_message' : osero.question_message,
        'end_message' : osero.end_message
    }
    return jsonify(response_data)

@app.route('/reset', methods = ['POST'])
def reset():
    osero.__init__()
    return redirect(url_for('index'))


@app.route('/register',methods=['POST'])  
def register():
    if request.method == "POST":
        try:
            loc = request.form["data"]
            osero.check_answer(loc)
            message = loc
        except Exception as e:
            message = str(e)
        dict = {"answer": message}     
    return json.dumps(dict)  

