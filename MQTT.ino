#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const int B=4275; // B value of the thermistor
const int R0 = 100000; // R0 = 100k
const int pinTempSensor = A0; // Grove - Temperature Sensor connect to A5
const int light = D4; // Grove - Temperature Sensor connect to A5
const int light1 = D8; // Grove - Temperature Sensor connect to A5
const int light2 = D9; // Grove - Temperature Sensor connect to A5
int Status = 12;  // Digital pin D6
int sensor = 13;  // Digital pin D7

char msg[50];


// Change the credentials below, so your ESP8266 connects to your router
const char* ssid = "POCO";
const char* password = "12345678";

// Change the variable to your Raspberry Pi IP address, so it connects to your MQTT broker
const char* mqtt_server = "192.168.95.137";

// Initializes the espClient. You should change the espClient name if you have multiple ESPs running in your home automation system
WiFiClient espClient;
PubSubClient client(espClient);



// Timers auxiliar variables
long now = millis();
long lastMeasure = 0;

// Don't change the function below. This functions connects your ESP8266 to your router
void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP IP address: ");
  Serial.println(WiFi.localIP());
}

// This functions is executed when some device publishes a message to a topic that your ESP8266 is subscribed to
// Change the function below to add logic to your program, so when a device publishes a message to a topic that 
// your ESP8266 is subscribed you can actually do something
void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }  
  
  if (messageTemp == "off") 
  {
     digitalWrite(light, LOW);  
  }  
  if (messageTemp == "on") 
  { 
     digitalWrite(light, HIGH);  
     Serial.print("Rojo");                
                   
  }  
  if (messageTemp == "off1") 
  {
     digitalWrite(light1, LOW);       
  }  
  if (messageTemp == "on1") 
  { 
     digitalWrite(light1, HIGH);
     Serial.print("Verde");                
            
  }  
  if (messageTemp == "off2") 
  {
     digitalWrite(light1, LOW);       
  }  
  if (messageTemp == "on2") 
  { 
     digitalWrite(light1, HIGH);
     Serial.print("Azul");                
            
  } 
}

// This functions reconnects your ESP8266 to your MQTT broker
// Change the function below if you want to subscribe to more topics with your ESP8266 
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");  
      // Subscribe or resubscribe to a topic
      // You can subscribe to more topics (to control more LEDs in this example)
      client.subscribe("Light/0");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

// The setup function sets your ESP GPIOs to Outputs, starts the serial communication at a baud rate of 115200
// Sets your mqtt broker and sets the callback function
// The callback function is what receives messages and actually controls the LEDs
void setup() {
  
  pinMode(light, OUTPUT); 
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  pinMode(sensor, INPUT);   // declare sensor as input

}

// For this project, you don't need to change anything in the loop function. Basically it ensures that you ESP is connected to your broker
void loop() {

  if (!client.connected()) {
    reconnect();
  }
  if(!client.loop())
    client.connect("ESP8266Client");

  
  now = millis();
  // Publishes new temperature and humidity every 30 seconds
  if (now - lastMeasure > 3000) {
    lastMeasure = now;
    long state = digitalRead(sensor);
    String mov = "";
    if(state == HIGH) {
      digitalWrite (Status, HIGH);
      mov = "Motion detected!";
      Serial.println(mov);
      delay(1000);
      }
    else {
      digitalWrite (Status, LOW);
      mov = "Motion absent!";
      Serial.println(mov);
      delay(1000);
      }   
    int a = analogRead(pinTempSensor );
    float R = 1023.0/((float)a)-1.0;
    R = 100000.0*R;
    //convert to temperature via datasheet ;
    float temperature = 1.0/(log(R/100000.0)/B+1/298.15)-273.15;
    snprintf (msg, 50, "%.2f", temperature);
    client.publish("lis/temperatura", msg);
    Serial.print("temperature = ");
    Serial.println(temperature);
    delay(100);
  }
} 
