/*
  ============================================================
   TEMPERATURE DETECTOR WITH 3 LED INDICATORS
  ============================================================
   Course : Electrical Engineering - Computer and Control Algorithms
   Board  : Arduino UNO
   Sensor : LM35 analog temperature sensor (10 mV / °C)

   Rule:
     T <= 20 °C          -> BLUE   LED ON
     20 °C < T <= 40 °C  -> ORANGE LED ON
     T > 40 °C           -> RED    LED ON
   Only one LED is ON at a time.

   Wiring:
     LM35 +Vs  -> 5V
     LM35 Vout -> A0
     LM35 GND  -> GND
     D8  -> 220 ohm -> BLUE   LED (+) , LED (-) -> GND
     D9  -> 220 ohm -> ORANGE LED (+) , LED (-) -> GND
     D10 -> 220 ohm -> RED    LED (+) , LED (-) -> GND
  ============================================================
*/

#include "temperature_logic.h"

// ---------- Pin assignment ----------
const int SENSOR_PIN     = A0;
const int BLUE_LED_PIN   = 8;
const int ORANGE_LED_PIN = 9;
const int RED_LED_PIN    = 10;

// ---------- Settings ----------
const int  SAMPLES        = 10;    // readings averaged to reduce noise
const long LOOP_DELAY_MS  = 500;   // time between measurements

// ---------- Function prototypes ----------
void allLedsOff();
void showLed(LedColor color);
const char* colorName(LedColor color);

void setup() {
  pinMode(BLUE_LED_PIN,   OUTPUT);
  pinMode(ORANGE_LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN,    OUTPUT);
  allLedsOff();

  Serial.begin(9600);
  Serial.println("Temperature detector started");
}

void loop() {
  // 1) Read the sensor (average of several samples)
  long sum = 0;
  for (int i = 0; i < SAMPLES; i++) {
    sum += analogRead(SENSOR_PIN);
    delay(5);
  }
  int raw = sum / SAMPLES;

  // 2) Convert reading to degrees Celsius
  float tempC = rawToCelsius(raw);

  // 3) Decide which LED to turn on
  LedColor color = chooseLed(tempC);

  // 4) Drive the LEDs
  showLed(color);

  // 5) Report on the Serial Monitor
  Serial.print("Temperature: ");
  Serial.print(tempC, 1);
  Serial.print(" C  ->  ");
  Serial.println(colorName(color));

  // 6) Wait, then repeat
  delay(LOOP_DELAY_MS);
}

// Turn every LED off
void allLedsOff() {
  digitalWrite(BLUE_LED_PIN,   LOW);
  digitalWrite(ORANGE_LED_PIN, LOW);
  digitalWrite(RED_LED_PIN,    LOW);
}

// Turn on exactly one LED
void showLed(LedColor color) {
  digitalWrite(BLUE_LED_PIN,   color == LED_BLUE   ? HIGH : LOW);
  digitalWrite(ORANGE_LED_PIN, color == LED_ORANGE ? HIGH : LOW);
  digitalWrite(RED_LED_PIN,    color == LED_RED    ? HIGH : LOW);
}

const char* colorName(LedColor color) {
  switch (color) {
    case LED_BLUE:   return "BLUE   (T <= 20 C)";
    case LED_ORANGE: return "ORANGE (20 C < T <= 40 C)";
    default:         return "RED    (T > 40 C)";
  }
}
