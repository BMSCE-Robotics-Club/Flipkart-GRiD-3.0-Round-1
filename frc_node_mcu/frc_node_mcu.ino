//#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <Servo.h>  
Servo servo;

const uint16_t port = 80;
const char *host = "192.168.43.184";
WiFiClient client;
void setup()
{
    Serial.begin(115200);
    servo.attach(D8);
    servo.write(180);
    delay(100);
    pinMode(D3, OUTPUT);
    pinMode(D4, OUTPUT);
    pinMode(D5, OUTPUT);
    pinMode(D6, OUTPUT);
    Serial.println("Connecting...\n");
    WiFi.mode(WIFI_STA);
    
    //WiFi.begin("honor", "blahblah");
    WiFi.begin("AndroidAP7e41", "12345678"); // change it to your ussid and password
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
    //Serial.println("Connected to server successful!");
    //client.println("Hello From ESP8266");
    //delay(250);
    client.println("Enter something : ");
    delay(250);
    while (client.available() > 0)
    {
        char c = client.read();
        Serial.write(c);
        if(c == 'f')
        {
          analogWrite(D3, 450);
          analogWrite(D6, 450);
          analogWrite(D4, 0);
          analogWrite(D5, 0);
          //digitalWrite(D3, HIGH);
          //digitalWrite(D4, LOW);
          //digitalWrite(D5, LOW);
          //digitalWrite(D6, HIGH);
        }
        else if(c == 'b')
        {
          digitalWrite(D3, 0);
          digitalWrite(D4, 450);
          digitalWrite(D5, 450);
          digitalWrite(D6, 0);
        }
        else if(c == 'l')
        {
          digitalWrite(D3, 450);
          digitalWrite(D4, 0);
          digitalWrite(D5, 0);
          digitalWrite(D6, 450);
        }
        else if(c == 'r')
        {
          digitalWrite(D3, 0);
          digitalWrite(D4, 450);
          digitalWrite(D5, 450);
          digitalWrite(D6, 0);
        }
        else if(c == 'j')
        {
          digitalWrite(D3, LOW);
          digitalWrite(D4, LOW);
          digitalWrite(D5, LOW);
          digitalWrite(D6, LOW);
          servo.write(70);
          delay(2000);
          servo.write(180);
         
        }
        else
        {
          digitalWrite(D3, LOW);
          digitalWrite(D4, LOW);
          digitalWrite(D5, LOW);
          digitalWrite(D6, LOW);
        }
        delay(100);
    }
    Serial.print('\n');
    //client.stop();
    delay(100);
}
