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
import dlib
import face_recognition

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
	cpt = sum([len(files) for r, d, files in os.walk("static/images")])


	file = easygui.fileopenbox()
	frame = cv2.imread(file)
	
	number=cpt+1
	filename=str(number)+'.jpg'
	path = './static/images'
	cv2.imwrite(os.path.join(path , filename), frame)
	cv2.destroyAllWindows()
	return render_template('faces.html', number = number)    

@app.route('/input')
@app.route('/input.html')
def input():
    return render_template('input.html')

@app.route('/')
@app.route('/select_input')
def select_input():
	cpt = sum([len(files) for r, d, files in os.walk("static/target")])


	file = easygui.fileopenbox()
	frame = cv2.imread(file)
	
	number=cpt+1
	filename=str(number)+'.jpg'
	path = './static/target'
	cv2.imwrite(os.path.join(path , filename), frame)
	cv2.destroyAllWindows()
	return render_template('input.html')

@app.route('/workflow')
@app.route('/workflow.html')
def workflow():
    return render_template('workflow.html')

@app.route('/')
@app.route('/generateEncodingsSingle')
def generateEncodingsSingle(personImage):
    finalEncodings = []
    boxes = face_recognition.face_locations(personImage, model = 'hog')
    encodings = face_recognition.face_encodings(personImage, boxes)
    for encoding in encodings:
        finalEncodings.append(encoding)    
    return finalEncodings

@app.route('/')
@app.route('/generateEncodings')
def generateEncodings(personImages):
    finalEncodings = []
    for i in personImages:
        boxes = face_recognition.face_locations(i, model = 'hog')
        encodings = face_recognition.face_encodings(i, boxes)
        for encoding in encodings:
            finalEncodings.append(encoding)
    return finalEncodings

# targetImage - cv2 image in which you have to identify a person
# personImage - a list of images of person to be identified
# A function that takes a target image and list of images of a person and returns True or False depending on person is present in target image or not
@app.route('/')
@app.route('/faceRecognitionImage')
def faceRecognitionImage(targetImage, personImage):
    personEncoding = generateEncodingsSingle(personImage)
    targetEncodings = generateEncodings(targetImage)

    for encoding in targetEncodings:
        matches = face_recognition.compare_faces(personEncoding, encoding)
        if True in matches:
            return True
    return False
@app.route('/')
@app.route('/run_workflow')
def run_workflow():
	person=[]
	folder="static/images"
	for filename in os.listdir(folder):
	    img = cv2.imread(os.path.join(folder,filename))
	    img= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	    if img is not None:
	        person.append(img)
	target=[]
	folder="static/target"
	for filename in os.listdir(folder):
	    img = cv2.imread(os.path.join(folder,filename))
	    img= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	    if img is not None:
	        target.append(img)
	flag=0
	if person is not None and target is not None:
		for i in person:
			if(faceRecognitionImage(target, i)):
				cpt = sum([len(files) for r, d, files in os.walk("static/detected")])
				number=cpt+1
				filename=str(number)+'.jpg'
				path = './static/detected'
				cv2.imwrite(os.path.join(path , filename), i)
				flag=1
				
	if(flag):
		return render_template('workflow1.html')
	else:
		return render_template('workflow2.html')

if __name__ == '__main__':
	app.run(debug=True)    