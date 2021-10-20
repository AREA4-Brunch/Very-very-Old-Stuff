#include <Arduino.h>

#include "IRremote.h"


//#define F(slit) (reinterpret_cast<const __FlashStringHelper *> (PSTR(slit)))

const uint8_t pinReciever = 11;

IRrecv irrecv(pinReciever);
decode_results data;


void translateIR() {
    /*Serial.print(F("code: "));
    Serial.print(data.value);
    Serial.print(F(" - Button pressed: "));*/
    switch(data.value) {
        // There are two different codes getting mixed up
        // when using power ON/OFF button
        case 0xE85D2639:
            Serial.println(F("Power ON/OFF"));
            break;
        case 0x168A2AEC:
            Serial.println(F("Power ON/OFF"));
            break;
        case 0x3E8CA87D:
            Serial.println(F("MUTE"));
            break;
        case 0x3E8CA87C:
            Serial.println(F("PLAY/PAUSE"));
            break;
        case 0x7DD059E9:
            Serial.println(F("NEXT"));
            break;
        case 0x7DD059EA:
            Serial.println(F("PREVIOUS"));
            break;
        case 0x59CDE2A5:
            Serial.println(F("PLAYER VOL 0"));
            break;
        case 0x59CDE2A4:
            Serial.println(F("PLAYER VOL 1"));
            break;
        case 0x5756836B:
            Serial.println(F("PLAYER VOL 2"));
            break;
        case 0x57568368:
            Serial.println(F("PLAYER VOL 3"));
            break;
        case 0x7F5900F9:
            Serial.println(F("PLAYER VOL 4"));
            break;
        case 0x7F5900F8:
            Serial.println(F("PLAYER VOL 5"));
            break;
        case 0x5EF53087:
            Serial.println(F("PLAYER VOL 6"));
            break;
        case 0x5EF53084:
            Serial.println(F("PLAYER VOL 7"));
            break;
        case 0x3AF2B943:
            Serial.println(F("PLAYER VOL 8"));
            break;
        case 0x3FF:
            Serial.println(F("PLAYER VOL 9"));
            break;
        case 0x56C5CDF1:
            Serial.println(F("PLAYER VOL 10"));
            break;
        case 0x56c5cdf2:
            Serial.println(F("PC VOL 0"));
            break;
        case 0xe6be61db:
            Serial.println(F("PC VOL 1"));
            break;
        case 0xe6be61da:
            Serial.println(F("PC VOL 2"));
            break;
        case 0xfebcf92f:
            Serial.println(F("PC VOL 3"));
            break;
        case 0xfebcf92c:
            Serial.println(F("PC VOL 4"));
            break;
        case 0xdaba81eb:
            Serial.println(F("PC VOL 5"));
            break;
        case 0xdaba81ea:
            Serial.println(F("PC VOL 6"));
            break;
        case 0x9ee6367b:
            Serial.println(F("PC VOL 7"));
            break;
        case 0x9ee63678:
            Serial.println(F("PC VOL 8"));
            break;
        case 0xc6e8b409:
            Serial.println(F("PC VOL 9"));
            break;
        case 0xc6e8b408:
            Serial.println(F("PC VOL 10"));
            break;
        case 0xa684e397:
            Serial.println(F("PC VOL 11"));
            break;
        case 0xa684e394:
            Serial.println(F("PC VOL 12"));
            break;
        case 0x82826c53:
            Serial.println(F("PC VOL 13"));
            break;
        case 0x82826c52:
            Serial.println(F("PC VOL 14"));
            break;
        case 0x207bef0f:
            Serial.println(F("PC VOL 15"));
            break;
        case 0x207bef0c:
            Serial.println(F("PC VOL 16"));
            break;
        default:
            Serial.println(F("Unknown button"));
            break;
    }
}


void setup()
{
    // logging:
    Serial.begin(9600);
    while(!Serial);  // wait for it to connect
    Serial.println(F("setup: in"));

    Serial.println(F("Starting the IR Arduino Decoding reciever.."));
    irrecv.enableIRIn();  // start the reciever

    Serial.println(F("setup: out"));
}

void loop()
{
    if(irrecv.decode(&data)) {
        translateIR();
        delay(500);
        irrecv.resume();
    }
}
