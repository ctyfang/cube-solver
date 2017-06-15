/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo clasp;  // create servo object to control a servo
Servo wrist;
// twelve servo objects can be created on most boards
// variable to store the servo position

void setup() {
  clasp.attach(8);  // attaches the servo on pin 9 to the servo object
  wrist.attach(7);
}

void loop() {
  wrist.write(0);
  delay(1000);
  clasp.write(110);
  delay(1000);
  wrist.write(90);
  delay(1000);
  clasp.write(60);
  delay(1000);
}

