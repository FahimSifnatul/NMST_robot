import face_recognition
import pickle

all_face_encodings = {}

img = face_recognition.load_image_file("miss_tasnim_binte_shawkat_1.jpg")
all_face_encodings["miss_tasnim_binte_shawkat_1"] = face_recognition.face_encodings(img, num_jitters=10)[0]

img = face_recognition.load_image_file("mister_omaer_faruq_1.jpg")
all_face_encodings["mister_omaer_faruq_1"] = face_recognition.face_encodings(img, num_jitters=10)[0]

img = face_recognition.load_image_file("mister_saif_1.jpg")
all_face_encodings["mister_saif_1"] = face_recognition.face_encodings(img, num_jitters=10)[0]

img = face_recognition.load_image_file("mister_fahim_sifnatul_1.jpg")
all_face_encodings["mister_fahim_sifnatul_1"] = face_recognition.face_encodings(img, num_jitters=10)[0]

img = face_recognition.load_image_file("miss_nazmin_islam_1.jpg")
all_face_encodings["miss_nazmin_islam_1"] = face_recognition.face_encodings(img, num_jitters=10)[0]

img = face_recognition.load_image_file("miss_oishi_jyoti_1.jpg")
all_face_encodings["miss_oishi_jyoti_1"] = face_recognition.face_encodings(img, num_jitters=10)[0]

img = face_recognition.load_image_file("mister_akib_1.jpg")
all_face_encodings["mister_akib_1"] = face_recognition.face_encodings(img, num_jitters=10)[0]


with open('dataset_faces.dat', 'wb') as f:
    pickle.dump(all_face_encodings, f)
