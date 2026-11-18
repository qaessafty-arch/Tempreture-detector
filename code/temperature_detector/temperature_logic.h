// temperature_logic.h
// Pure decision logic for the temperature detector.
// Kept free of Arduino functions so it can also be tested on a PC.

#ifndef TEMPERATURE_LOGIC_H
#define TEMPERATURE_LOGIC_H

// Temperature limits in degrees Celsius
const float LOW_LIMIT  = 20.0;   // T <= 20         -> BLUE
const float HIGH_LIMIT = 40.0;   // 20 < T <= 40    -> ORANGE
                                 // T > 40          -> RED

enum LedColor { LED_BLUE, LED_ORANGE, LED_RED };

// Decide which LED must be ON for a given temperature.
inline LedColor chooseLed(float tempC) {
  if (tempC <= LOW_LIMIT) {
    return LED_BLUE;              // cold / normal: 20 °C or below
  } else if (tempC <= HIGH_LIMIT) {
    return LED_ORANGE;            // warm: above 20 up to 40 °C
  } else {
    return LED_RED;               // hot: above 40 °C
  }
}

// Convert a raw 10-bit ADC reading (0..1023) from an LM35 to °C.
// LM35 output = 10 mV per °C.  ADC step = 5 V / 1024.
// T = raw * (5000 mV / 1024) / (10 mV/°C) = raw * 500 / 1024
inline float rawToCelsius(int raw) {
  return raw * 500.0 / 1024.0;
}

#endif
