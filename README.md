# AI-Powered-Driver-Alert-and-Intoxication-Detection-System

## 1. Introduction
Road accidents caused by alcohol consumption and driver fatigue are major public safety concerns worldwide. Drivers under the influence of alcohol or experiencing drowsiness have reduced reaction time, poor judgment, and impaired motor skills.

This project presents a Smart Driver Safety and Monitoring System that integrates alcohol detection using an MQ-3 sensor and AI-based drowsiness detection using computer vision techniques. The system provides real-time monitoring and generates alerts when unsafe driving conditions are detected.

---

## 2. Objectives

The primary objectives of this project are:

1. To detect alcohol consumption using an MQ-3 gas sensor.
2. To detect driver drowsiness using facial landmark analysis.
3. To generate real-time alerts through LED indication and audio alarm.
4. To send remote notifications using WhatsApp via Twilio API.
5. To improve driver safety through continuous monitoring.

---

## 3. System Overview

The system is divided into two major modules:

### 3.1 Alcohol Detection Module (Hardware-Based)

This module uses an MQ-3 alcohol sensor connected to an Arduino UNO. The sensor measures alcohol concentration in breath samples and produces an analog voltage proportional to the alcohol level.

The Arduino reads the analog value from pin A0 and compares it with a predefined threshold.

* If the sensor value exceeds the threshold, alcohol is considered detected.
* A red LED is activated to indicate an unsafe condition.
* If the value is below the threshold, a green LED indicates a safe condition.

This module provides a simple and effective hardware-based alcohol detection mechanism.

---

### 3.2 Drowsiness Detection Module (Software-Based)

The drowsiness detection module is implemented using Python and computer vision libraries.

The system captures live video using a webcam and processes facial landmarks using MediaPipe Face Mesh. From the detected landmarks, two important ratios are calculated:

1. Eye Aspect Ratio (EAR) – Used to determine whether the eyes are closed.
2. Mouth Aspect Ratio (MAR) – Used to detect yawning.

If:

* Eyes remain closed for more than a defined duration, drowsiness is detected.
* Mouth remains open for an extended duration, yawning is detected.

When either condition is satisfied:

* An alarm sound is played.
* A warning message is displayed.
* A WhatsApp alert is sent to a predefined number.

---

## 4. Working Principle

### 4.1 Eye Aspect Ratio (EAR)

The Eye Aspect Ratio is calculated using the distances between specific eye landmarks. When the eyes are open, the ratio remains relatively constant. When the eyes close, the ratio decreases significantly.

By setting a threshold value, the system can determine whether the driver’s eyes are closed for a dangerous duration.

---

### 4.2 Mouth Aspect Ratio (MAR)

The Mouth Aspect Ratio is calculated using inner lip landmarks. When a person yawns, the vertical distance between lips increases, causing the ratio to rise above a defined threshold.

Sustained high MAR values indicate yawning behavior.

---

## 5. Alert Mechanism

The system uses multiple alert mechanisms:

1. Visual Alert – LED indicators (Red/Green).
2. Audio Alert – Alarm sound using simpleaudio library.
3. Remote Alert – WhatsApp notification using Twilio API.

A cooldown mechanism is implemented to prevent repeated message sending within a short time interval.

---

## 6. Technologies Used

### Hardware

* Arduino UNO
* MQ-3 Alcohol Sensor
* LEDs (Red and Green)

### Software

* Python
* OpenCV
* MediaPipe
* NumPy
* SimpleAudio
* Twilio API
* Arduino IDE

---

## 7. Advantages

1. Real-time monitoring system.
2. Combines hardware and AI-based detection.
3. Remote alert capability.
4. Low-cost and scalable solution.
5. Can be integrated into smart vehicle systems.

---

## 8. Limitations

1. MQ-3 sensor requires calibration.
2. Detection accuracy may vary with lighting conditions.
3. Internet connection is required for WhatsApp alerts.
4. Camera-based detection depends on proper face visibility.

---

## 9. Future Scope

1. Integration with vehicle ignition control system.
2. Addition of GPS tracking during alerts.
3. Cloud-based data logging and analytics.
4. Mobile application integration.
5. Deployment using embedded AI hardware (e.g., Raspberry Pi).

---

## 10. Conclusion

The Smart Driver Safety and Monitoring System combines embedded systems and artificial intelligence to create a real-time safety solution. By integrating alcohol detection and drowsiness monitoring, the system enhances road safety and demonstrates practical application of IoT and computer vision technologies in transportation safety.

---

