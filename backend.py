import cv2
import dlib
import face_recognition

# Generates 128-d encoding for all the faces in the image
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
def faceRecognitionImage(targetImage, personImage):
    personEncoding = generateEncodings(personImage)
    targetEncodings = generateEncodings([targetImage])

    for encoding in targetEncodings:
        matches = face_recognition.compare_faces(personEncoding, encoding)
        if True in matches:
            return True
    return False

# targetVideo - cv2 captured video in which you have to identify a person
# personImage - a list of images of person to be identified
# A function that takes a target video and identifies whether the given person is present in it or not
def faceRecognitionVideo(targetVideo, personImage):
    personEncoding = generateEncodings(personImage)
    while targetVideo.isOpened():
        print("Frame")
        ret, frame = targetVideo.read()
        if not ret:
            break

        target = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        targetEncodings = generateEncodings([target])
        for encoding in targetEncodings:
            matches = face_recognition.compare_faces(personEncoding, encoding)
            print(matches)
            if True in matches:
                return True
    return False

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
if person is not None and target is not None:
    print(faceRecognitionImage(target, person))
