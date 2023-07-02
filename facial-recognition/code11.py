import face_recognition
import cv2
import numpy as np 

import csv
import os
from datetime import datetime

video_capture = cv2.VideoCapture(0)

jobs_image = face_recognition.load_image_file("img/jobs.jpg")
jobs_encoding = face_recognition.face_encodings(jobs_image)[0]

#Fayssal 
Fayssal_image = face_recognition.load_image_file("img/Fayssal.jpg")
Fayssal_encoding = face_recognition.face_encodings(Fayssal_image)[0]

ElonMusk_image = face_recognition.load_image_file("img/ElonMusk.jpg")
ElonMusk_encoding = face_recognition.face_encodings(ElonMusk_image)[0]

Monalisa_image = face_recognition.load_image_file("img/Monalisa.jpg")
Monalisa_encoding = face_recognition.face_encodings(Monalisa_image)[0]

Tesla_image = face_recognition.load_image_file("img/Tesla.jpeg")
Tesla_encoding = face_recognition.face_encodings(Tesla_image)[0]

known_face_encoding = [jobs_encoding, Fayssal_encoding, ElonMusk_encoding, Monalisa_encoding, Tesla_encoding]

known_faces_names = ["jobs", "Elaazouzi Fayssal" ,"Elon Musk", "Monalisa", "Tesla"]

students = known_faces_names.copy()

face_locations = []
face_encodings = []
face_names = []
s=True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

filename = current_date+'.csv'
if not os.path.exists(filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        #writer.writerow(["Name", "Status"])
        writer.writerow(["Name", "Status", "Time"])
        for name in known_faces_names:
            writer.writerow([name, "Absent"])

while True:
    _,frame = video_capture.read()
    small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    # rgb_small_frame = small_frame[:,:,::-1]
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
        # face_encodings = face_recognition.face_encodings(rgb_small_frame, [face_locations])

        face_names = []
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encoding,face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encoding,face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]

            face_names.append(name)
            if name in known_faces_names:
                if name in students:
                    students.remove(name)
                    print(students)
                    current_time = now.strftime("%H:%M:%S")
                    with open(filename, 'r') as f:
                        reader = csv.reader(f)
                        rows = list(reader)
                        # for i in range(1, len(rows)):
                        #     if rows[i][0] == name and rows[i][1] == "Absent":
                        #         rows[i][1] = "Present"
                        for i in range(1, len(rows)):
                            if rows[i][0] == name and rows[i][1] == "Absent":
                                rows[i][1] = "Present"
                                rows[i].append(current_time)  # add current time to row
                    with open(filename, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerows(rows)
                        
            # draw a box around the face
            cv2.rectangle(frame, (left*4, top*4), (right*4, bottom*4), (0, 0, 255), 2)
            # put name label above the box
            cv2.rectangle(frame, (left*4, top*4 - 35), (right*4, top*4), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left*4 + 6, top*4 - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow("attendance system", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

# Close the csv file
f.close()
