from flask import render_template,request,redirect,url_for,jsonify,Flask
import osero_main
import json

port = 80
app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)