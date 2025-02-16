import cv2
import numpy as np
import base64
import requests
from object_detection import ObjectDetection
import math

od = ObjectDetection(use_gpu=True)

vehicle_classes = ['car', 'truck', 'bus', 'motorbike']

cap = cv2.VideoCapture("traffic.mp4")

count = 0
center_points_prev_frame = []
tracking_objects = {}
track_id = 0

data = {}

while True:
    ret, frame = cap.read()
    count += 1
    if not ret:
        break

    center_points_cur_frame = []

    (class_ids, scores, boxes) = od.detect(frame)

    filtered_boxes = []
    for i, box in enumerate(boxes):
        detected_class = od.classes[class_ids[i]]
        if detected_class.lower() in vehicle_classes:
            filtered_boxes.append(box)

    for box in filtered_boxes:
        (x, y, w, h) = box
        cx = int(x + w / 2)
        cy = int(y + h / 2)
        center_points_cur_frame.append((cx, cy))
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if count <= 2:
        for pt in center_points_cur_frame:
            for pt2 in center_points_prev_frame:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                if distance < 20:
                    tracking_objects[track_id] = pt
                    track_id += 1
    else:
        tracking_objects_copy = tracking_objects.copy()
        center_points_cur_frame_copy = center_points_cur_frame.copy()

        for object_id, pt2 in tracking_objects_copy.items():
            object_exists = False
            for pt in center_points_cur_frame_copy:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                if distance < 20:
                    tracking_objects[object_id] = pt
                    object_exists = True
                    if pt in center_points_cur_frame:
                        center_points_cur_frame.remove(pt)
                    continue
            if not object_exists:
                tracking_objects.pop(object_id)

        for pt in center_points_cur_frame:
            tracking_objects[track_id] = pt
            track_id += 1

    for object_id, pt in tracking_objects.items():
        cv2.circle(frame, pt, 5, (0, 0, 255), -1)
        cv2.putText(frame, str(object_id), (pt[0], pt[1] - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    print(f"Frame {count} - Tracking Objects: {tracking_objects}")

    cv2.imshow("Frame", frame)
    
    retval, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    data['frameImage'] = jpg_as_text
    data['vehicleCount'] = len(tracking_objects)

    try:
        response = requests.post("http://localhost:3000/api/detections", json=data)
        print("Server response:", response.text)
    except Exception as e:
        print("Error sending data:", e)

    center_points_prev_frame = center_points_cur_frame.copy()

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
