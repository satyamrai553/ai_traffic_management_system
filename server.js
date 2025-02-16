const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb', extended: true }));
app.use(cors());

app.use(express.static(path.join(__dirname, 'public')));
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = 3000;
let cycleInProgress = false;  

io.on('connection', (socket) => {
  console.log('New client connected');

  socket.on('manualOverride', (data) => {
    console.log('Manual override received:', data);
    let manualGreenTime = parseInt(data.manualGreenTime, 10);
    let maxCycle = 90;
    let redTime = maxCycle - manualGreenTime;

   
    if (!cycleInProgress) {
      cycleInProgress = true;
     
      io.emit('lightUpdate', { state: 'green', duration: manualGreenTime });
      setTimeout(() => {
        io.emit('lightUpdate', { state: 'yellow', duration: 3 });
        setTimeout(() => {
          io.emit('lightUpdate', { state: 'red', duration: redTime });
          
          cycleInProgress = false;
        }, 3000);
      }, manualGreenTime * 1000);
    }
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});

app.post('/api/detections', (req, res) => {
  try {
    const trackingData = req.body;
    console.log("✅ Received tracking data:", JSON.stringify(trackingData, null, 2));

    let { vehicleCount, frameImage } = trackingData;
    
    let baseTime = 20;
    let multiplier = 3;
    let maxCycle = 90;
    let greenTime = Math.min(maxCycle, baseTime + vehicleCount * multiplier);
    let redTime = maxCycle - greenTime;

    
    io.emit('trafficUpdate', { greenTime, redTime, vehicleCount, frameImage });

    
    if (!cycleInProgress) {
      cycleInProgress = true;
     
      io.emit('lightUpdate', { state: 'green', duration: greenTime });
      
      setTimeout(() => {
        io.emit('lightUpdate', { state: 'yellow', duration: 3 });
        
        setTimeout(() => {
          io.emit('lightUpdate', { state: 'red', duration: redTime });
         
          cycleInProgress = false;
        }, 3000);
      }, greenTime * 1000);
    }

    res.status(200).send("✅ Data received successfully");
  } catch (error) {
    console.error("❌ Error processing data:", error);
    res.status(500).send("Server Error");
  }
});

server.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
