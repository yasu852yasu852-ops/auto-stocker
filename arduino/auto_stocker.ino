// Simple Arduino sketch: listen on Serial for 'IN <slot> <sku>' or 'OUT <slot> <sku>'
// and toggle LEDs on pins 2..9 accordingly.

const int pins[8] = {2,3,4,5,6,7,8,9};

void setup(){
  Serial.begin(115200);
  for(int i=0;i<8;i++) pinMode(pins[i], OUTPUT);
}

void loop(){
  if(Serial.available()){
    String line = Serial.readStringUntil('\n');
    line.trim();
    if(line.length()==0) return;
    // parse
    if(line.startsWith("IN ")){
      int sp1 = line.indexOf(' ',3);
      String sslot = line.substring(3, sp1);
      int slot = sslot.toInt();
      if(slot>=1 && slot<=8) digitalWrite(pins[slot-1], HIGH);
      Serial.println("ACK IN " + String(slot));
    } else if(line.startsWith("OUT ")){
      int sp1 = line.indexOf(' ',4);
      String sslot = line.substring(4, sp1);
      int slot = sslot.toInt();
      if(slot>=1 && slot<=8) digitalWrite(pins[slot-1], LOW);
      Serial.println("ACK OUT " + String(slot));
    }
  }
}
