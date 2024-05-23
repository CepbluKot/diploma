#include <Arduino.h>


long counter1 = 0;
long counter2 = 0;
#define pin_a_1 4
#define pin_b_1 2

#define pin_a_2 5
#define pin_b_2 3

void count_logic_1()
{
    if (digitalRead(pin_a_1) == LOW)
    {
        counter1++;
    }
    else
    {
        counter1--;
    }
}

void count_logic_2()
{
    if (digitalRead(pin_a_2) == LOW)
    {
        counter2++;
    }
    else
    {
        counter2--;
    }
}

void setup()
{
    Serial.begin(9600);
    pinMode(pin_b_1, INPUT_PULLUP);
    pinMode(pin_a_1, INPUT_PULLUP);

    pinMode(pin_b_2, INPUT_PULLUP);
    pinMode(pin_a_2, INPUT_PULLUP);
    attachInterrupt(0, count_logic_1, RISING);
    attachInterrupt(1, count_logic_2, RISING);
}

unsigned long currentMillis;
unsigned long previousMillis;

void loop()
{
    currentMillis = millis();

    if (currentMillis - previousMillis > 100)
    {
        Serial.println("{\"left\":" + String(counter1) + ", \"right\":" + String(counter2) + "}");
        previousMillis = currentMillis;
    }
}
