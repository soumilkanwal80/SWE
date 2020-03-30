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
	
	number=cpt+1
	filename=str(number)+'.jpg'
	path = './images'
	cv2.imwrite(os.path.join(path , filename), frame)
	cv2.destroyAllWindows()
	return render_template('faces.html')    

@app.route('/input')
@app.route('/input.html')
def input():
    return render_template('input.html')

@app.route('/')
@app.route('/select_input')
def select_input():
	cpt = sum([len(files) for r, d, files in os.walk("target")])


	file = easygui.fileopenbox()
	frame = cv2.imread(file)
	
	number=cpt+1
	filename=str(number)+'.jpg'
	path = './target'
	cv2.imwrite(os.path.join(path , filename), frame)
	cv2.destroyAllWindows()
	return render_template('input.html')

@app.route('/workflow')
@app.route('/workflow.html')
def workflow():
    return render_template('workflow.html')

@app.route('/')
@app.route('/run_workflow')
def run_workflow():
	person=[]
	folder="images"
	for filename in os.listdir(folder):
	    img = cv2.imread(os.path.join(folder,filename))
	    img= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	    if img is not None:
	        person.append(img)
	target=[]
	folder="target"
	for filename in os.listdir(folder):
	    img = cv2.imread(os.path.join(folder,filename))
	    img= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	    if img is not None:
	        target.append(img)
	return render_template('workflow.html')

if __name__ == '__main__':
	app.run(debug=True)    