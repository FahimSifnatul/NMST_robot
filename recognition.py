import time
start = time.time()
import face_recognition
import pickle
import numpy as np
end=time.time()
d=end-start
print("i slept {} for".format(d))

# Load face encodings
with open('dataset_faces.dat', 'rb') as f:
	all_face_encodings = pickle.load(f)

# Grab the list of names and the list of encodings
face_names = list(all_face_encodings.keys())
face_encodings = np.array(list(all_face_encodings.values()))

# Try comparing an unknown image
start = time.time()
unknown_image = face_recognition.load_image_file("/home/pi/Desktop/SciRobot/1.jpg")
unknown_face = face_recognition.face_encodings(unknown_image)
end=time.time()
d=end-start
print("i slept {} for".format(d))
start = time.time()
result = face_recognition.compare_faces(face_encodings, unknown_face, tolerance = 0.5)
end=time.time()
d=end-start
print("i slept {} for".format(d))
# Print the result as a list of names with True/False
names_with_result = list(zip(face_names, result))
print(names_with_result)
