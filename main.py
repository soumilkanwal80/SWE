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
from flask_caching import Cache
from shutil import copyfile


app = Flask(__name__)

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "null", # Flask-Caching related configs
}

app.config.from_mapping(config)
cache = Cache(app)


@app.route('/')
@app.route('/home')
@app.route('/home.html')
def home_page():
    return render_template('home.html')


@app.route('/faces')
@app.route('/faces.html')
@app.route('/faces.html/<number>')
def faces():
    cpt = sum([len(files) for r, d, files in os.walk("static/images")])
    # number=cpt+1
    return render_template('faces.html', number = cpt, flag = 1)

@app.route('/')
@app.route('/select_target')
def select_target():
	cpt = sum([len(files) for r, d, files in os.walk("static/images")])


	file = easygui.fileopenbox()

	if file == None:
		return render_template('faces.html', number = cpt, flag = 0)

	if file.lower().endswith(('.png', '.jpg', '.jpeg')) == False:
		return render_template('faces.html', number = cpt, flag=-1)	
	
	frame = cv2.imread(file)
	
	number=cpt+1
	filename=str(number)+'.jpg'
	path = './static/images'
	cv2.imwrite(os.path.join(path , filename), frame)
	cv2.destroyAllWindows()
	return render_template('faces.html', number = number, flag = 1)    

@app.route('/input')
@app.route('/input.html')
@app.route('/input.html/<number>')
def input():
    cpt = sum([len(files) for r, d, files in os.walk("static/target")])
    return render_template('input.html', number = cpt, flag = 1, video_flag = 0)

@app.route('/')
@app.route('/select_input')
def select_input():
	cpt = sum([len(files) for r, d, files in os.walk("static/target")])


	file = easygui.fileopenbox()
	if file == None:
		# flash('No image selected')
		return render_template('input.html', number = cpt, flag = 0, video_flag = 0)

	if file.lower().endswith(('.png', '.jpg', '.jpeg')) == False:
		return render_template('input.html', number = cpt, flag = -1, video_flag = 0)		
	
	frame = cv2.imread(file)
	
	number=cpt+1
	filename=str(number)+'.jpg'
	path = './static/target'
	cv2.imwrite(os.path.join(path , filename), frame)
	cv2.destroyAllWindows()
	return render_template('input.html', number = number, flag = 1, video_flag = 0)

@app.route('/')
@app.route('/select_input_video')
def select_input_video():
	cpt = sum([len(files) for r, d, files in os.walk("static/target_video")])


	file = easygui.fileopenbox()
	if file == None:
		# flash('No image selected')
		return render_template('input.html', number = cpt, flag = 0, video_flag = 0)

	if file.lower().endswith(('.mp4', '.mkv')) == False:
		return render_template('input.html', number = cpt, flag = -1, video_flag = -1)		
	
	# cap = cv2.VideoCapture(file)
	# frame_width = int(cap.get(3))
	# frame_height = int(cap.get(4))
	
	# number=cpt+1
	# filename=str(number)+'.mp4'
	# path = './static/target'
	# out = cv2.VideoWriter('./static/target_video/output.mp4',cv2.VideoWriter_fourcc('M','J','P','G'),60, (frame_width,frame_height))
	# while(True):
	# 	ret, frame = cap.read()
	# 	if ret==True:
	#   		out.write(frame)
	#   		if cv2.waitKey(1) & 0xFF == ord('q'):
	#   			break
	# 	else:
	# 		break 
	# cv2.destroyAllWindows()
	number = cpt + 1

	copyfile(file, './static/target_video/output.mp4')



	return render_template('input.html', number = number, flag = 1, video_flag = 1)

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
@app.route('/run_workflow/<number>')
def run_workflow():
	person=[]
	folder="static/images"
	for filename in os.listdir(folder):
	    img = cv2.imread(os.path.join(folder,filename))
	    #img= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	    if img is not None:
	        person.append(img)
	target=[]
	folder="static/target"
	for filename in os.listdir(folder):
	    img = cv2.imread(os.path.join(folder,filename))
	    #img= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	    if img is not None:
	        target.append(img)
	flag=0
	folder = 'static/detected'
	for filename in os.listdir(folder):
	    file_path = os.path.join(folder, filename)
	    try:
	        if os.path.isfile(file_path) or os.path.islink(file_path):
	            os.unlink(file_path)
	        elif os.path.isdir(file_path):
	            shutil.rmtree(file_path)
	    except Exception as e:
        	print('Failed to delete %s. Reason: %s' % (file_path, e))

	folder = 'static/images'
	for filename in os.listdir(folder):
	    file_path = os.path.join(folder, filename)
	    try:
	        if os.path.isfile(file_path) or os.path.islink(file_path):
	            os.unlink(file_path)
	        elif os.path.isdir(file_path):
	            shutil.rmtree(file_path)
	    except Exception as e:
        	print('Failed to delete %s. Reason: %s' % (file_path, e))

	folder = 'static/target'
	for filename in os.listdir(folder):
	    file_path = os.path.join(folder, filename)
	    try:
	        if os.path.isfile(file_path) or os.path.islink(file_path):
	            os.unlink(file_path)
	        elif os.path.isdir(file_path):
	            shutil.rmtree(file_path)
	    except Exception as e:
        	print('Failed to delete %s. Reason: %s' % (file_path, e))
	if person is not None and target is not None:
		for i in person:
			if(faceRecognitionImage(target, i)):
				cpt = sum([len(files) for r, d, files in os.walk("static/detected")])
				number=cpt+1
				filename=str(number)+'.jpg'
				path = './static/detected'
				cv2.imwrite(os.path.join(path , filename), i)
				flag=1

		for i in target:
			cv2.imwrite(os.path.join('./static/detected', 'target.jpg'), i)			
				
	if(flag):
		return render_template('workflow1.html', number = number)
	else:
		return render_template('workflow2.html')

@app.route('/')
@app.route('/faceRecognitionVideo')
def faceRecognitionVideo(targetVideo, personImage):
    personEncoding = generateEncodingsSingle(personImage)
    while targetVideo.isOpened():
        ret, frame = targetVideo.read()
        if not ret:
            return "Error"

        target = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        targetEncodings = generateEncodingsSingle(target)
        for encoding in targetEncodings:
            matches = face_recognition.compare_faces(personEncoding, encoding)
            if True in matches:
                return True
    return False


@app.route('/')
@app.route('/run_workflow_video')
@app.route('/run_workflow_video/<number>')
def run_workflow_video():
	person=[]
	folder="static/images"
	for filename in os.listdir(folder):
	    img = cv2.imread(os.path.join(folder,filename))
	    #img= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	    if img is not None:
	        person.append(img)
	folder="static/target_video"
	targetVideo=cv2.VideoCapture("./static/target_video/output.mp4")
	flag=0
	folder = 'static/detected_video'
	for filename in os.listdir(folder):
	    file_path = os.path.join(folder, filename)
	    try:
	        if os.path.isfile(file_path) or os.path.islink(file_path):
	            os.unlink(file_path)
	        elif os.path.isdir(file_path):
	            shutil.rmtree(file_path)
	    except Exception as e:
        	print('Failed to delete %s. Reason: %s' % (file_path, e))

	folder = 'static/images'
	for filename in os.listdir(folder):
	    file_path = os.path.join(folder, filename)
	    try:
	        if os.path.isfile(file_path) or os.path.islink(file_path):
	            os.unlink(file_path)
	        elif os.path.isdir(file_path):
	            shutil.rmtree(file_path)
	    except Exception as e:
        	print('Failed to delete %s. Reason: %s' % (file_path, e))

	

	if person is not None and targetVideo is not None:
		cpt=0
		for i in person:
			if(faceRecognitionVideo(targetVideo, i)):
				cpt = sum([len(files) for r, d, files in os.walk("static/detected_video")])
				number=cpt+1
				filename=str(number)+'.jpg'
				path = './static/detected_video'
				cv2.imwrite(os.path.join(path , filename), i)
				flag=1		

	if(flag):
		return render_template('workflow3.html', number = number)
	else:
		number = 0
		return render_template('workflow3.html', number = number)

@app.route('/test.html')
def test_css():
	return render_template('test.html')	


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
	app.run(debug=True)    