import serial
import sys
import asyncio

class ArduinoInterface:
    def __init__(self, port=None, baudrate=9600, timeout=1):
        """
        Args:
            port (str): Serial port (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
            baudrate (int): Baud rate (default 9600 to match Arduino)
            timeout (int): Serial read timeout in seconds
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
    
    async def open(self):
        self.close()
        try:
            if not self.port:
                raise ValueError("Port must be specified either in __init__ or open()")
            
            self.serial_conn = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
            print(f"Connected to Arduino on {self.port} at {self.baudrate} baud")
            
            try:
                await asyncio.sleep(2)  # Give Arduino time to initialize
            except asyncio.CancelledError:
                self.close()
                print("Error sleeping after opening serial port", file=sys.stderr)
        
        except serial.SerialException as e:
            print(f"Error opening serial port {self.port}: {e}", file=sys.stderr)
            raise
    
    def close(self):
        """Close the serial connection"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Serial connection closed")

    async def read_humidity(self) -> float:
        self.serial_conn.write("HUMIDITY\n".encode())
        try:
            await asyncio.sleep(1)  # Give Arduino time to respond
        except asyncio.CancelledError:
            self.close()
            raise
        return float(self.read_a_line())

    def read_a_line(self):
        if not self.serial_conn or not self.serial_conn.is_open:
            raise RuntimeError("Serial connection not open. Call open() first.")
        
        try:
            if self.serial_conn.in_waiting > 0:
                line = self.serial_conn.readline().decode('utf-8').strip()
                if line == "ERROR":
                    print("Received error message from Arduino")
                    return None
                return line
        except Exception as e:
            print(f"Error reading serial data: {e}", file=sys.stderr)
            raise