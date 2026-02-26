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
  delay(500);

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');

    if (command == "HUMIDITY") {
      float humidity = dht.readHumidity();
      if (isnan(humidity)) {
        Serial.println("ERROR");
      } else {
        Serial.println(humidity);
      }
    }

  }
}