#include <Arduino.h>
#include <DHT.h>

#define DHTPIN 2     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22   // DHT 22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
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