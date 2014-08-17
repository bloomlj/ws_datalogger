//xiongmaogu  gps info is 103.598217,30.969961

int analogValue = 0;    // variable to hold the analog value

void setup() {
  // open the serial port at 9600 bps:
  Serial.begin(9600);
}

void loop() {
  // read the analog input on pin 0:
  analogValue = analogRead(0);

  // print it out in many formats:
  Serial.print("T|"); 
  Serial.print("103.598|"); 
  Serial.print("30.969|"); 
  Serial.println(analogValue);  // print as an ASCII-encoded decimal

  // delay 10 milliseconds before the next reading:
  delay(5000);
}
