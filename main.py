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
import easygui
import cv2
import os


app = Flask(__name__)

@app.route('/')
@app.route('/home')
@app.route('/home.html')
def home_page():
    return render_template('home.html')


@app.route('/faces')
@app.route('/faces.html')
def faces():
    return render_template('faces.html')

@app.route('/')
@app.route('/select_target')
def select_target():
	cpt = sum([len(files) for r, d, files in os.walk("images")])


	file = easygui.fileopenbox()
	frame = cv2.imread(file)
	cv2.imshow('frame',frame)
	number=cpt+1
	filename=str(number)+'.jpg'
	path = './images'
	cv2.imwrite(os.path.join(path , filename), frame)
	cv2.destroyAllWindows()
	return render_template('faces.html')    


if __name__ == '__main__':
	app.run(debug=True)    
