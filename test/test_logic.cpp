// PC test for the decision logic.  Build & run:
//   g++ -std=c++11 -I code/temperature_detector test/test_logic.cpp -o test_logic && ./test_logic
#include <cstdio>
#include "temperature_logic.h"

static int failures = 0;

static void check(float t, LedColor expected) {
  LedColor got = chooseLed(t);
  const char* names[] = {"BLUE", "ORANGE", "RED"};
  bool ok = (got == expected);
  if (!ok) failures++;
  std::printf("%-5s T = %6.2f C -> %-6s (expected %s)\n",
              ok ? "PASS" : "FAIL", t, names[got], names[expected]);
}

int main() {
  check(-10.0f, LED_BLUE);
  check(0.0f,   LED_BLUE);
  check(19.9f,  LED_BLUE);
  check(20.0f,  LED_BLUE);    // boundary: equal to 20 is BLUE
  check(20.1f,  LED_ORANGE);
  check(30.0f,  LED_ORANGE);
  check(40.0f,  LED_ORANGE);  // boundary: 40 is still ORANGE
  check(40.1f,  LED_RED);
  check(100.0f, LED_RED);

  // ADC conversion: raw 41 ~= 20.0 C, raw 82 ~= 40.0 C
  std::printf("raw 41 -> %.2f C, raw 82 -> %.2f C, raw 205 -> %.2f C\n",
              rawToCelsius(41), rawToCelsius(82), rawToCelsius(205));

  std::printf(failures ? "\n%d test(s) FAILED\n" : "\nAll tests passed\n", failures);
  return failures ? 1 : 0;
}
