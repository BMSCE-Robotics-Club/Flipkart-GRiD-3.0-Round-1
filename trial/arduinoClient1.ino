#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>

const uint16_t port = 12345;
const char *host = "192.168.144.173";
WiFiClient client;
void setup()
{
    Serial.begin(115200);
    pinMode(D3, OUTPUT);
    pinMode(D4, OUTPUT);
    pinMode(D5, OUTPUT);
    pinMode(D6, OUTPUT);
    Serial.println("Connecting...\n");
    WiFi.mode(WIFI_STA);
    
    WiFi.begin("Nanma", "12345678");
    //WiFi.begin("AndroidAP7e41", "12345678"); // change it to your ussid and password
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
}

void loop()
{
    if (!client.connect(host, port))
    {
        Serial.println("Connection to host failed");
        delay(1000);
        return;
    }
    Serial.println("Connected to server successful!");
    client.println("Hello From ESP8266");
    //delay(250);
    client.println("Enter something : ");
    delay(250);
    while (client.available() > 0)
    {
        char c = client.read();
        Serial.write(c);
        if(c == 'f')
        {
          analogWrite(D3, 255);
          analogWrite(D6, 255);
          //digitalWrite(D3, HIGH);
          digitalWrite(D4, LOW);
          digitalWrite(D5, LOW);
          //digitalWrite(D6, HIGH);
        }
        else if(c == 'b')
        {
          digitalWrite(D3, LOW);
          digitalWrite(D4, HIGH);
          digitalWrite(D5, HIGH);
          digitalWrite(D6, LOW);
        }
        else if(c == 'l')
        {
          digitalWrite(D3, HIGH);
          digitalWrite(D4, LOW);
          digitalWrite(D5, HIGH);
          digitalWrite(D6, LOW);
        }
        else if(c == 'r')
        {
          digitalWrite(D3, LOW);
          digitalWrite(D4, HIGH);
          digitalWrite(D5, LOW);
          digitalWrite(D6, HIGH);
        }
        else
        {
          digitalWrite(D3, LOW);
          digitalWrite(D4, LOW);
          digitalWrite(D5, LOW);
          digitalWrite(D6, LOW);
        }
    }
    Serial.print('\n');
    client.stop();
    delay(100);
}
