int mq3Pin = A0;       // MQ-3 analog output
int redLed = 8;        // LED for "YES" (alcohol detected)
int greenLed = 9;      // LED for "NO" (no alcohol)
int threshold = 400;   // Adjust based on your environment

void setup() {
  Serial.begin(9600);
  pinMode(redLed, OUTPUT);
  pinMode(greenLed, OUTPUT);
  Serial.println("MQ-3 Alcohol Sensor with LED Output");
}

void loop() {
  int sensorValue = analogRead(mq3Pin);

  if (sensorValue > threshold) {
    Serial.println("YES");
    digitalWrite(redLed, HIGH);    // Turn on red LED
    digitalWrite(greenLed, LOW);   // Turn off green LED
  } else {
    Serial.println("NO");
    digitalWrite(redLed, LOW);     // Turn off red LED
    digitalWrite(greenLed, HIGH);  // Turn on green LED
  }

  delay(1000);  // Update every second
}