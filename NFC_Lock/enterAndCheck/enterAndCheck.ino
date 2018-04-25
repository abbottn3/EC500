/*
  Tag format: 1 JSON-formatted text record:
  {
  name: username,
  room: room number (long int),
  checkin: checkin time (unix time, long int),
  checkout: checkout time (unix time, long int),
  }
*/

// Uncomment the SEEED or ADAFRUIT sections below based on which shield you are using

// SEEED STUDIO
//#include <SPI.h>
//#include <PN532_SPI.h>
//#include <PN532.h>
//#include <NfcAdapter.h>
//#include <Time.h>
//
//PN532_SPI pn532spi(SPI, 10);
//NfcAdapter nfc = NfcAdapter(pn532spi);
// end SEEED STUDIO

// ADAFRUIT
#include <Wire.h>
#include <PN532_I2C.h>
#include <PN532.h>
#include <NfcAdapter.h>
#include <Time.h>

PN532_I2C pn532_i2c(Wire);
NfcAdapter nfc = NfcAdapter(pn532_i2c);
// end ADAFRUIT

const int greenLed = 5;         // pin for the green LED
const int redLed = 6;           // pin for the red LED
const int button = 3;

String inputString = "";        // string for input from serial port
long lightOnTime = 0;           // last time the LEDs were turned on, in ms
int buttonVal = 0;
int pressTime;
int relTime;
String uids[10];
int totalIDs = 0;

boolean readyToWrite = false;   // true when you are ready to write to NFC tag

void setup() {
  Serial.begin(9600);           // initialize serial communications
  nfc.begin();                  // initialize NfcAdapter
  pinMode(greenLed, OUTPUT);    // make pin 9 an output
  pinMode(redLed, OUTPUT);      // make pin 8 an output
  pinMode(button, INPUT);
}

void loop() {
  // if there's incoming data, read it into a string:
  buttonVal = digitalRead(button);
  digitalWrite(redLed, LOW);
  digitalWrite(greenLed, LOW);
  if (buttonVal == LOW) {
    pressTime = millis();
    while (buttonVal == LOW) {
      buttonVal = digitalRead(button);
    }
    relTime = millis();
    if (relTime - pressTime > 1000) {
      digitalWrite(redLed, HIGH);
      Serial.println("start");
      enterID();
    }
    else {
      digitalWrite(greenLed, HIGH);
      checkID();
    }
  }
  //lookForTag();

}
void enterID() {
  /*
    int uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
    int uidLength;                        // Length of the UID (4 or 7 bytes depending on ISO14443A card type)
    //boolean success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, &uid[0], &uidLength);
    for (int i=0; i < uidLength; i++) {
      Serial.print(" 0x");Serial.print(uid[i], HEX);
    }
    for (int z = 0; z < 7; z++) {
    uids[totalIDs][z] = uid[z];
    }
  */
  int whilecnt = 0;
  while (!nfc.tagPresent() && whilecnt < 100000) {
    whilecnt += 1;
  }
  NfcTag tag = nfc.read();
  Serial.println("mid");
  Serial.print('&');
  Serial.print(tag.getUidString());
  Serial.print('$');
  uids[totalIDs] = tag.getUidString();
  totalIDs += 1;
  int flashcount = 0;
  while (flashcount < 10) {
    digitalWrite(greenLed, HIGH);
    digitalWrite(redLed, LOW);
    delay(200);
    digitalWrite(greenLed, LOW);
    digitalWrite(redLed, HIGH);
    delay(200);
    flashcount += 1;
  }
}

void checkID() {
  /*
    int uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
    int uidLength;                        // Length of the UID (4 or 7 bytes depending on ISO14443A card type)
    //boolean success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, &uid[0], &uidLength);
    bool isLogged = false;
    for (int i=0; i < uidLength; i++) {
      Serial.print(" 0x");Serial.print(uid[i], HEX);
    }
    for (int j = 0; j < totalIDs; j++) {
    for (int z = 0; z < 7; z++) {
      if (uid[z] != uids[j][z]) {
        break;
      }
      else {
        if (z == 6) {
          isLogged = true;
        }
        else {
          continue;
        }
      }
    }
    if (isLogged) break;
    }
  */
  bool isLogged = false;
  int whilecnt = 0;
  while (!nfc.tagPresent() && whilecnt < 100000) {
    whilecnt += 1;
  }
  NfcTag tag = nfc.read();
  String tagstr = tag.getUidString();
  for (int i = 0; i < totalIDs; i++) {
    if (tagstr != uids[i]) {
      continue;
    }
    else {
      isLogged = true;
      break;
    }
  }
  int flashcount = 0;
  if (isLogged) {
    while (flashcount < 5) {
      digitalWrite(greenLed, HIGH);
      delay(500);
      digitalWrite(greenLed, LOW);
      delay(500);
      flashcount += 1;
    }
  }
  else {
    digitalWrite(greenLed, LOW);
    while (flashcount < 5) {
      digitalWrite(redLed, HIGH);
      delay(500);
      digitalWrite(redLed, LOW);
      delay(500);
      flashcount += 1;
    }
  }
}

void lookForTag() {
  if (nfc.tagPresent()) {                 // if there's a tag present
    NdefMessage message;                  // make a new NDEF message
    // add the input string as a record:
    message.addMimeMediaRecord("text/secretpassword", inputString);
    boolean success = nfc.write(message); // attempt to write to the tag

    if (success) {
      // let the desktop app know you succeeded:
      Serial.println("Result: tag written.");
      digitalWrite(redLed, LOW);          // turn off the failure light if on
      digitalWrite(greenLed, HIGH);       // turn on the success light
      lightOnTime = millis();
      readyToWrite = false;               // clear write flag
    }
    else {
      // let the desktop app know you failed:
      Serial.println("Result: failed to write to tag");
      digitalWrite(greenLed, LOW);       // turn off the success light if on
      digitalWrite(redLed, HIGH);        // turn on the failure light
      lightOnTime = millis();
    }
  }
}
