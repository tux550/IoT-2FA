// TODO: Add user ID to response of finger and camera from server
// TODO: Add LEDs
#include <Keypad.h>
#include <LiquidCrystal.h>

#define IDLE 0
#define READING_FINGER 50
#define WAITING_IMAGE 2
#define READING_PIN 3
#define WAITING_PIN 4
#define ACCEPT 5
#define REJECT 6

#define ACCEPT_DELAY 5000
#define REJECT_DELAY 5000

#define BUTTON_CAMERA_PIN 47
#define BUTTON_FINGER_PIN 49

// Fingerprint sensor
#include <Adafruit_Fingerprint.h>
#if (defined(__AVR__) || defined(ESP8266)) && !defined(__AVR_ATmega2560__)
// pin #4 is IN from sensor
// pin #5 is OUT from arduino
SoftwareSerial mySerial(4, 5);
#else
#define mySerial Serial1
#endif
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

int STATE = IDLE;
unsigned long LAST_CHANGE_TIME = 0;
const int ROW_NUM = 4;
const int COLUMN_NUM = 4;
char buffer[32];
// LCD display
const int rs = 3, en = 2, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// 4x4 Keypad
char keys[ROW_NUM][COLUMN_NUM] = {
    {'1', '2', '3', 'A'},
    {'4', '5', '6', 'B'},
    {'7', '8', '9', 'C'},
    {'*', '0', '#', 'D'}};


byte pin_rows[ROW_NUM] = {23, 25, 27, 29};
byte pin_column[COLUMN_NUM] = {31, 33, 35, 37};

Keypad keypad = Keypad(makeKeymap(keys), pin_rows, pin_column, ROW_NUM, COLUMN_NUM);

// PIN input
String inputString = "";
String serverStringResponse = "";

// State management
void initLCD()
{
  lcd.begin(16, 2);
  setStates(IDLE);
}

void setStates(int state)
{
  STATE = state;
  LAST_CHANGE_TIME = millis();
  lcd.clear();

  Serial.println("El estado es" + String(STATE));
  switch (state)
  {
  case READING_PIN:
    lcd.print("INSERT PASS");
    break;
  case IDLE:
      lcd.print("IDLE");
      break;
  case WAITING_IMAGE:
      lcd.print("TAKING IMG");
      break;
  case ACCEPT:
    lcd.print("ACCEPT");
    
    break;
  case REJECT:
    lcd.print("REJECT");
    
    break;
  }
}

bool isCameraButtonPressed()
{
  // Serial.println("aqui: " + digitalRead(BUTTON_CAMERA_PIN));
  return digitalRead(BUTTON_CAMERA_PIN) == HIGH;
}

bool isFingerButtonPressed()
{
  return false;
  return digitalRead(BUTTON_FINGER_PIN) == HIGH;
}

bool isTimeout(unsigned long delay)
{
  return millis() - LAST_CHANGE_TIME > delay;
}

bool readKeypadInput() // return true if input is done
{
  // GetKey
  char key = keypad.getKey();
  if (key)
  {
    // NumberInput
    char currentInputChar = key;
    if (key - '0' >= 0 && key - '0' <= 9)
    {
      inputString += (char)key;
      return false;
    }
    // RegisterInput
    else if (key == '#')
    {
      return true;
    }
  }
  else
  {
    return false;
  }
}


// Main function
void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(10000);
  initLCD();
  pinMode(BUTTON_CAMERA_PIN, INPUT);
  pinMode(BUTTON_FINGER_PIN, INPUT);
  
}
void loop()
{

  if (STATE == IDLE)
  {

    if (isCameraButtonPressed())
    {
      // Send request to server to take image
      Serial.println("TAKE_IMAGE");
      // Wait for response
      setStates(WAITING_IMAGE);
    }
    else if (isFingerButtonPressed())
    {
      // Wait for response
      setStates(READING_FINGER);
    }
  }
  else if (STATE == READING_FINGER)
  {

    // Read finger
    int id = getFingerprintIDez();
    if (id != -1)
    {
      // Send id to server
      Serial.println("FINGER:" + id);
      setStates(WAITING_PIN);
    }
  }
  else if (STATE == WAITING_IMAGE)
  {
    // Wait for image
    if (Serial.available() != 0)
    {
      // Wait for response
      Serial.readBytesUntil('\0', buffer, 32);

      String response = String(buffer);

      //Serial.println("respuesta es "+ response);
      
      if (response == "ACCEPT")
      {
        setStates(READING_PIN);
      }
      else
      {
        setStates(REJECT);
      }
    }
  }
  else if (STATE == READING_PIN)
  {
    // Read PIN. If # is pressed, send PIN to server
    
    if (readKeypadInput())
    {
      // Send pin to server
      Serial.println("PIN:" + inputString);
      inputString = "";
      setStates(WAITING_PIN);
    }
  }
  else if (STATE == WAITING_PIN)
  {
    // Wait for response
    //Serial.println("waiting pin" );

    if (Serial.available() != 0)
    {
      // Wait for response
      Serial.readBytesUntil('\0', buffer, 32);

      String response = String(buffer);
      //Serial.println("waiting pin" + response);
      if (response == "ACCEPT")
      {
        setStates(ACCEPT);
      }
      else
      {
        
        setStates(REJECT);
      }
    }
  }
  else if (STATE == ACCEPT)
  {
    // Display accept message for 5 seconds
    if (isTimeout(ACCEPT_DELAY))
    {
      setStates(IDLE);
    }
  }
  else if (STATE == REJECT)
  {
    // Display reject message for 5 seconds
    if (isTimeout(REJECT_DELAY))
    {
      setStates(IDLE);
    }
  }
}

int getFingerprintIDez()
{
  // If finger is detected return the ID
  // Else return -1

  uint8_t p = finger.getImage();
  if (p != FINGERPRINT_OK)
    return -1;

  p = finger.image2Tz();
  if (p != FINGERPRINT_OK)
    return -1;

  p = finger.fingerFastSearch();
  if (p != FINGERPRINT_OK)
    return -1;

  // Serial.print("Found ID #"); Serial.print(finger.fingerID);
  // Serial.print(" with confidence of "); Serial.println(finger.confidence);
  return finger.fingerID;
}