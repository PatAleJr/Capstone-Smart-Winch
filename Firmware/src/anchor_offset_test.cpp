#include <Arduino.h>

#define rotaryEncoderOutputA 6
#define rotaryEncoderOutputB 7

#define IN_RELAY_PIN 3
#define OUT_RELAY_PIN 4

int tickCounter = 0; 
int aState;
int aLastState;

int ticksPerRevolution = 40;

float desiredLength = -5;
float currentLength = 0;

float r0 = 2.25; // initial winch radius in inches (when its full)
float cordDiameter = 0.25;
int wrapsPerLayer = 15;

void setup() { 
    pinMode(rotaryEncoderOutputA,INPUT);
    pinMode(rotaryEncoderOutputB,INPUT);
    pinMode(IN_RELAY_PIN, OUTPUT);
    pinMode(OUT_RELAY_PIN, OUTPUT);

    Serial.begin(9600);
    // Reads the initial state of the outputA
    aLastState = digitalRead(rotaryEncoderOutputA);   
} 

int read_tick() {
    int returnVal = 0;
    aState = digitalRead(rotaryEncoderOutputA); // Reads the "current" state of the outputA
    // If the previous and the current state of the outputA are different, that means a Pulse has occured
    if (aState != aLastState){     
        // If the outputB state is different to the outputA state, that means the encoder is rotating clockwise
        if (digitalRead(rotaryEncoderOutputB) != aState) { 
        returnVal = 1;
        } else {
        returnVal = -1;
        }
    } 
    aLastState = aState; // Updates the previous state of the outputA with the current state
    return returnVal;
}

float lastLayerRadius = 0;

float pi = 3.14159;
float counter_to_length() {
    float totalTheta = tickCounter * 2 * pi / ticksPerRevolution; // in radians
    float theta = fmod(totalTheta, 2*pi); // in radians
    int totalRevolutions = tickCounter / ticksPerRevolution;
    int revolutionsLastLayer = totalRevolutions % wrapsPerLayer;
    int layerOffset = (int)(totalRevolutions / wrapsPerLayer); // Topmost layer is 0, second layer is 1...

    float L = 0;
    for (int layer = 0; layer <= layerOffset; layer++) {
        float layerRadius = r0 - layer * cordDiameter;
        lastLayerRadius = layerRadius;
        if (layer == layerOffset) {
            L += revolutionsLastLayer * 2*pi * layerRadius + theta * layerRadius;
        } else {
            L += wrapsPerLayer * 2*pi * layerRadius;
        }
    }
    return L;
}

int lastLoggingTime = millis();
int loggingIntervalMillis = 2000;
void handleLogging() {
    int currentTime = millis();
    if (currentTime - lastLoggingTime > loggingIntervalMillis) {
        Serial.print("Current length released = ");
        Serial.print(currentLength);
        Serial.print("   Current number of ticks = ");
        Serial.print(tickCounter);
        Serial.print("Last layer radius = ");
        Serial.println(lastLayerRadius);

        Serial.print("Desired length: ");
        Serial.println(desiredLength);

        lastLoggingTime = currentTime;
    }
}

float tolerance = 1;

void loop() {
    handleLogging();
    tickCounter += read_tick();
    currentLength = counter_to_length();
    if (abs(desiredLength - currentLength) > tolerance) {
        if (desiredLength < currentLength) {
            digitalWrite(IN_RELAY_PIN, LOW);
            digitalWrite(OUT_RELAY_PIN, HIGH);
        } else {
            digitalWrite(OUT_RELAY_PIN, LOW);
            digitalWrite(IN_RELAY_PIN, HIGH);
        }
    } else {
        digitalWrite(IN_RELAY_PIN, LOW);
        digitalWrite(OUT_RELAY_PIN, LOW);
    }
}