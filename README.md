# A Smart AI-based Solution for Traffic Management

## Introduction

The AI Traffic Management System is a real-time traffic light control dashboard that uses object detection and tracking to dynamically adjust traffic signal timings. This project leverages a YOLOv4 model for vehicle detection and tracks vehicles across video frames to compute the green and red light durations. 

### Repository Structure

```
/ai_traffic_management_system
│
├── public
│   ├── index.html           # Dashboard UI
│   └── (other static files)
│
├── traffic_detection
│   ├── object_detection.py  # YOLOv4-based object detection
│   ├── object_tracking.py   # Object tracking and HTTP POST to server
|   |__traffic.mp4           # Video file of traffic
│   └── dnn_model            # YOLOv4 weights, config, and classes (model files)
│
├── server.js                # Node.js backend server
├── package.json             # Node.js dependencies
├── .gitignore               # Files and folders to ignore
└── README.md                # Project documentation
```

### Step 1: Clone the Repository

Clone the repository using Git:

```bash
git clone https://github.com/satyamrai553/ai_traffic_management_system.git
cd ai_traffic_management_system
```

### Step 2: Install Node.js Dependencies

Install required Node.js packages by running:

```bash
npm install
```

The project uses Express, Socket.IO, Cors, and Morgan among others.

### Step 3: Install Python Dependencies

Ensure you have Python installed and install the required packages:

```bash
pip install opencv-python numpy requests
```

### Step 4: Setup the YOLOv4 Model Files

**Download YOLOv4 files:**  
   Download the following files and place them in `traffic_detection/dnn_model`:
   - `yolov4.weights` (Note: This file is larger than GitHub's file size limit. Use Git LFS or download it separately.)
   - `yolov4.cfg`
   - `classes.txt`


### Step 5: Running the Project

#### Start the Node.js Server

Start the server from the project root:

```bash
node server.js
```

This will launch the server on [http://localhost:3000](http://localhost:3000) and serve the dashboard.

#### Start the Python Object Tracking Script

This script processes the video (e.g., `traffic.mp4`), detects vehicles, and sends the data (including a live image feed) to the Node.js server.
add the `traffic.mp4` in the [traffic_detection/traffic.mp4] path.

In another terminal, navigate to the `traffic_detection` folder and run the object tracking script:

```bash
python object_tracking.py
```


#### Viewing the Dashboard

Open your web browser and navigate to [http://localhost:3000](http://localhost:3000) to view the real-time dashboard. You can monitor the traffic data, live video feed, and traffic light simulation (green, yellow, red cycles).


## Conclusion

This project demonstrates an end-to-end solution combining real-time video processing with a dynamic traffic light control system. Contributions and improvements are welcome!
