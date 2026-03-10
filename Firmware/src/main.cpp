#include <Arduino.h>
#include <DHT.h>

#define DHTPIN 2     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22   // DHT 22

#define IN_RELAY_PIN 3
#define OUT_RELAY_PIN 4

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();

  pinMode(IN_RELAY_PIN, OUTPUT);
  pinMode(OUT_RELAY_PIN, OUTPUT);
}

void loop() {

  digitalWrite(OUT_RELAY_PIN, HIGH);
  delay(2000);
  digitalWrite(OUT_RELAY_PIN, LOW);
  delay(2000);
  digitalWrite(IN_RELAY_PIN, HIGH);
  delay(2000);
  digitalWrite(IN_RELAY_PIN, LOW);
  delay(2000);

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');

    if (command.equals("HUM")) {
      float humidity = dht.readHumidity();
      if (isnan(humidity)) {
        Serial.println("HUM:ERROR");
      } else {
        Serial.println("HUM:" + String(humidity) + "%");
      }

    } else if (command.equals("TMP")) {
      float temperature = dht.readTemperature();
      if (isnan(temperature)) {
        Serial.println("TMP:ERROR");
      } else {
        Serial.println("TMP:" + String(temperature) + "C");
      }
    }  
  }
}