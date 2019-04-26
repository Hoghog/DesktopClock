int TempAPin = A0;      // 温度センサーアナログピン番号
int RhAPin   = A1;      // 湿度センサーアナログピン番号
int RhDPin   = 2;       // 湿度センサーデジタルピン番号

int TempPinValue = 0;   // 温度センサーピン出力値
int RhPinValue   = 0;   // 湿度センサーピン出力値

float Temp = 0.0;       // 温度実測値
float Rh   = 0.0;       // 湿度実測値

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  // 温度センサーから値を読み取る
  TempPinValue = analogRead(TempAPin);
  Temp = modTemp(TempPinValue);

  // 湿度センサーから値を読み取る
  Rh = modRh();

  // 温度と湿度を CSV 出力
  Serial.println(String(Temp) + "," + String(Rh));

  delay(1000);
}

// 温度センサーから値を読み取る
float modTemp(int analog_val) {
  float tempV = 5000;
  float tempC = (((tempV * analog_val) / 1024) - 600) / 10;
  return tempC;
}

// 湿度センサーから値を読み取る
float modRh() {
  #define CAP 0.022e-6    // 湿度測定用コンデンサ C の容量（0.022uF）

  float Vc;               // コンデンサ C に充電された電圧の値
  float R;                // HR202L の抵抗の測定値
  long t = 1;             // 充電パルス幅（uSec）

  // レンジを変えながら最大で 5 回測定
  for(int i = 0; i < 5; i++) {
    // 充電パルスの時間をリトライの度に 10 倍ずつ増やす
    t *= 10;

    // コンデンサ C の電圧を読み取る
    Vc = GetVc(t);

    // 1024 の 1/10 を超えれば測定完了
    // ただし、若干余裕をもたせて 70 としている
    if(Vc > 70) break;
  }

  // HR202L の抵抗値を求める
  R = ((float)t / 1000000) / (CAP * log(1 - Vc / 1024)) * -1;

  // HR202L の抵抗値を対数化
  R = log10(R);

  // 温度補正
  // ※補正値はデータシートのグラフより目測にて推定
  R = R + Temp * (0.008363 * R + 0.007695);

  // リニアリティ補正
  // ※補正値はデータシートのグラフより目測にて推定
  Rh = 1.998 * R * R - 40.74 * R + 222.13;

  // 一応、湿度の上限を 100% に制限しておく
  Rh = min(Rh, 100);
  return Rh;
}

// コンデンサ C の電圧を取得
int GetVc(long t) {
  // t で指定されたパルス幅（uSec）でコンデンサ C を充電後
  // C の電圧を A/D 変換し戻り値とする
  pinMode(RhDPin, OUTPUT);

  // まずは C を放電しておかなければならない（条件によっては結構時間がかかるので注意）
  digitalWrite(RhDPin, LOW);

  // 2 以下なら放電完了と見なす
  while(analogRead(RhAPin) > 2);

  // 充電パルス生成ここから
  noInterrupts();

  // delayMicroseconds() は扱える時間に上限があるので、長時間の場合には分割する
  if(t <= 10000) {
    // そのままだと充電パルス幅が 5 uSec 程度長めになってしまうので補正
    // （クロック 16 MHz 用の値なので、それ以外の場合には要調整）
    t -= 5;

    digitalWrite(RhDPin, HIGH);
    delayMicroseconds(t);

    // 充電パルス終了
    // ピンをハイインピーダンスに設定
    pinMode(RhDPin, INPUT);

  } else {

    // 充電パルス幅 t を10回払いに分割
    t /= 10;

    digitalWrite(RhDPin, HIGH);
    for(int i = 0; i < 10; i++) delayMicroseconds(t);

    // 充電パルス終了
    // ピンをハイインピーダンスに設定
    pinMode(RhDPin, INPUT);
  }

  // 充電パルス生成ここまで
  interrupts();

  // コンデンサ C の電圧を A/D 変換
  RhPinValue = analogRead(RhAPin);
  return RhPinValue;
}
