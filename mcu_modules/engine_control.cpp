#include <Arduino.h>
#include <GSON.h>

int relay_a = 6;
int relay_b = 7;

void setup()
{
    pinMode(relay_a, OUTPUT);
    pinMode(relay_b, OUTPUT);
    Serial.begin(9600);
}

String received_message;

void loop()
{
    if (Serial.available())
    {
        received_message = Serial.readStringUntil('\r');

        if (received_message == "f")
        {
            digitalWrite(relay_a, 0);
            digitalWrite(relay_b, 1);
        }
        else if (received_message == "b")
        {
            digitalWrite(relay_a, 1);
            digitalWrite(relay_b, 0);
        }
        else if (received_message == "s")
        {
            digitalWrite(relay_a, 0);
            digitalWrite(relay_b, 0);
        }
    }
}
