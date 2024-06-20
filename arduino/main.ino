int x; 

#define IDLE 0
#define WAITING_IMAGE 1
#define READING_PIN 2
#define WAITING_PIN 3
#define ACCEPT 4
#define REJECT 5

#define ACCEPT_DELAY 5000
#define REJECT_DELAY 5000

#define BUTTON_PIN 2

int STATE = IDLE;
unsigned long LAST_CHANGE_TIME = 0;

// LCD display
const int rs = 12, en = 11, d4 = 2, d5 = 3, d6 = 4, d7 = 5;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// 4x4 Keypad
char keys[ROW_NUM][COLUMN_NUM] = {
    {'1', '2', '3', 'A'},
    {'4', '5', '6', 'B'},
    {'7', '8', '9', 'C'},
    {'*', '0', '#', 'D'}};

byte pin_rows[ROW_NUM] = {39, 41, 43, 45};
byte pin_column[COLUMN_NUM] = {47, 49, 51, 53};

Keypad keypad = Keypad(makeKeymap(keys), pin_rows, pin_column, ROW_NUM, COLUMN_NUM);

// PIN input
String inputString = "";

// State management
void initLCD() {
  lcd.begin(16, 2);
  setStates(IDLE);
}

void setStates(int state) {
  STATE = state;
  LAST_CHANGE_TIME = millis();
  lcd.clear();
  switch (state) {
    case IDLE:
      lcd.print("IDLE");
      break;
    case ACCEPT:
      lcd.print("ACCEPT");
      break;
    case REJECT:
      lcd.print("REJECT");
      break;
  }
}

bool isButtonPressed() {
  return digitalRead(BUTTON_PIN) == HIGH;
}

bool isTimeout(unsigned long delay) {
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
void setup() { 
	Serial.begin(115200); 
	Serial.setTimeout(1); 
  initLCD();
  pinMode(BUTTON_PIN, INPUT);
} 
void loop() {
  switch (state) {
    case IDLE:
      if (isButtonPressed()) {
        // Send request to server to take image
        Serial.println("TAKE_IMAGE");
        // Wait for response
        setStates(WAITING_IMAGE);
      }
    case WAITING_IMAGE:
      // Wait for image
      if (Serial.available() > 0) {
        // Wait for response
        String response = Serial.readString();
        if (response == "ACCEPT") {
          setStates(READING_PIN)
        } else {
          setStates(REJECT);
        }
      }
    case READING_PIN:
      // Read PIN. If # is pressed, send PIN to server
      if (readKeypadInput()) {
        // Send pin to server
        Serial.println("PIN:" + inputString);
        inputString = "";
        setStates(WAITING_PIN);
      }
    case WAITING_PIN:
      // Wait for response
      if (Serial.available() != 0) {
        // Wait for response
        String response = Serial.readString();
        if (response == "ACCEPT") {
          setStates(ACCEPT)
        } else {
          setStates(REJECT);
        }
      }
    case ACCEPT:
      // Display accept message for 5 seconds
      if (isTimeout(ACCEPT_DELAY)) {
        setStates(IDLE);
      }
    case REJECT:
      // Display reject message for 5 seconds
      if (isTimeout(REJECT_DELAY)) {
        setStates(IDLE);
      }
  }
} 
