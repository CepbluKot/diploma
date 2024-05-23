#include "Arduino.h"
#include "LoRa_E220.h"

LoRa_E220 e220ttl(&Serial2, 18, 21, 19);

void printModuleInformation(struct ModuleInformation moduleInformation);

#define DESTINATION_ADDL 0

void setup()
{
    Serial.begin(9600);
    e220ttl.begin();

    ResponseStructContainer c;
    c = e220ttl.getConfiguration();
    Configuration configuration = *(Configuration *)c.data;

    configuration.ADDL = 0x01;
    configuration.ADDH = 0x00;

    configuration.CHAN = 19;                               // Communication channel
    configuration.SPED.airDataRate = AIR_DATA_RATE_000_24; // Air baud rate
    configuration.OPTION.transmissionPower = POWER_22;     // Device power
    configuration.TRANSMISSION_MODE.fixedTransmission = FT_FIXED_TRANSMISSION;
    configuration.OPTION.subPacketSetting = SPS_200_00;

    ResponseStatus rs = e220ttl.setConfiguration(configuration, WRITE_CFG_PWR_DWN_SAVE);

    c.close();
}

ResponseStatus rs;
ResponseContainer received_message;
String msg_to_send;

void loop()
{

    if (e220ttl.available())
    {
        received_message = e220ttl.receiveMessage();

        while (Serial.available())
        {
            Serial.readStringUntil('\0');
        }
        Serial.println(received_message.data);
    }
    else
    {
        if (Serial.available())
        {
            msg_to_send = Serial.readStringUntil('\r');
            rs = e220ttl.sendFixedMessage(0, 0x02, 19, msg_to_send);
        }
    }
}