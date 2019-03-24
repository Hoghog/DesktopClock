int sensorPin = A0;
int sensorValue = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  sensorValue = analogRead(sensorPin);
  float temp = modTemp(sensorValue);
  Serial.println(temp);
  delay(1000);
}

float modTemp(int analog_val) {
  float v = 5000;
  float tempC = (((v * analog_val) / 1024) - 600) / 10;
  return tempC;
}
