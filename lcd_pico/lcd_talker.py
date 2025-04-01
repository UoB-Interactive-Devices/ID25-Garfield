import serial
class Talker:
    TERMINATOR = '\r' .encode('UTF8')
    def __init__(self, timeout=1):
        self.serial = serial.Serial(port = 'dev/ttyACM0', baudrate=115200, timeout=timeout)
    def send(self, text: str):
        line='%s\r\f' % text
        self.serial.write(line.encode('utf-8'))
        reply = self.receive()
        reply = reply.replace('>>>', '')

    def receive(self) -> str:
        line = self.serial.read_until(self.TERMINATOR)
        return line.decode('UTF8').strip()
    def close(self):
        self.serial.close()

#testing
#t = Talker()
#t.send('signone()')
