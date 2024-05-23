#include "DHT.h"

#define DHTPIN 7
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

float latest_humidity;
float latest_temperature;
unsigned long currentMillis;
unsigned long previousMillis;

void setup()
{
    Serial.begin(9600);

    dht.begin();
}

void loop()
{
    currentMillis = millis();

    if (currentMillis - previousMillis > 1000)
    {
        latest_humidity = dht.readHumidity();
        latest_temperature = dht.readTemperature();

        if (!(isnan(latest_humidity) || isnan(latest_temperature)))
        {
            Serial.println("{\"temperature\":" + String(latest_temperature) + ", \"humidity\":" + String(latest_humidity) + "}");
            return;
        }

        previousMillis = currentMillis;
    }
}