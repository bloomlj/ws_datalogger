int analogValue = 0;    // variable to hold the analog value

void setup() {
  // open the serial port at 9600 bps:
  Serial.begin(9600);
}

void loop() {
  // read the analog input on pin 0:
  analogValue = analogRead(0);

  // print it out in many formats:
  Serial.print("T:"); 
  Serial.print("103.123|"); 
  Serial.print("34.123|"); 
  Serial.println(analogValue);  // print as an ASCII-encoded decimal

  // delay 10 milliseconds before the next reading:
  delay(10);
}
