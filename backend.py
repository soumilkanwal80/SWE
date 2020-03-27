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


# person = cv2.imread('./person.png')
# person = cv2.cvtColor(person, cv2.COLOR_BGR2RGB)
# target = cv2.imread('./target2.jpg')
# target = cv2.cvtColor(target, cv2.COLOR_BGR2RGB)
# if person is not None and target is not None:
#     print(faceRecognitionImage(target, [person]))