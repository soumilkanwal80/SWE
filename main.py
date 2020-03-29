# # import eel

# eel.init('front-end')


# @eel.expose
# def add(num1, num2):
#     return int(num1) + int(num2)


# @eel.expose
# def subtract(num1, num2):
#     return int(num1) - int(num2)


# eel.start('home.html', size=(1000, 600))

from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')   


if __name__ == '__main__':
	app.run(debug=True)    
