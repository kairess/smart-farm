#include <WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <WebServer.h>

const char* ssid     = "WiFi SSID";
const char* password = "PASSWORD";
String ip_address    = "";

const int relay_led  = 26;
const int relay_pump = 25;
const int ON   = 0;
const int OFF  = 1;
const int AUTO = 2;

int LED_STATUS  = AUTO; // 0(on), 1(off), 2(auto)
int PUMP_STATUS = AUTO; // 0(on), 1(off), 2(auto)

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP);
WebServer server(80);

void setup() {
  Serial.begin(115200);

  pinMode(relay_led, OUTPUT);
  pinMode(relay_pump, OUTPUT);

  digitalWrite(relay_led, OFF);
  digitalWrite(relay_pump, OFF);

  Serial.print("Connecting to " + String(ssid));

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println(".");
  }

  ip_address = WiFi.localIP().toString();
  Serial.println("WiFi connected. IP address: " + ip_address);

  timeClient.begin();
  timeClient.setTimeOffset(3600 * 9);
  while(!timeClient.forceUpdate()) {
    delay(100);
  }

  server.on("/", handleOnConnect);
  server.on("/led", handleLed);
  server.on("/pump", handlePump);
  server.begin();
}

void handleOnConnect() {
  server.send(200, "text/html", "success");
}

void handleLed() {
  LED_STATUS = server.arg("status").toInt();
  server.send(200, "text/html", String(LED_STATUS));
}

void handlePump() {
  PUMP_STATUS = server.arg("status").toInt();
  server.send(200, "text/html", String(PUMP_STATUS));
}

void loop() {
  server.handleClient();

  int minute = timeClient.getMinutes();
  int hour = timeClient.getHours();
  int sec = timeClient.getSeconds();

  Serial.println(ip_address + " :: " + String(hour) + " " + String(minute) + " " + String(sec));

  if (hour >= 6 && hour < 18) {
    if (LED_STATUS == AUTO) {
      digitalWrite(relay_led, ON);
    } else {
      digitalWrite(relay_led, LED_STATUS);
    }

    if (PUMP_STATUS == AUTO) {
      if (minute % 60 == 0 && sec < 15) {
        digitalWrite(relay_pump, ON);
      } else {
        digitalWrite(relay_pump, OFF);
      }
    } else {
      digitalWrite(relay_pump, PUMP_STATUS);
    }
  } else {
    if (LED_STATUS == AUTO) {
      digitalWrite(relay_led, OFF);
    } else {
      digitalWrite(relay_led, LED_STATUS);
    }

    if (PUMP_STATUS == AUTO) {
      digitalWrite(relay_pump, OFF);
    } else {
      digitalWrite(relay_pump, PUMP_STATUS);
    }
  }

  delay(1000);
}
