import serial
import sys
import time

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
    
    def open(self):
        """
        Open serial connection to Arduino.
        Args:
            port (str): Serial port to connect to
        """
        self.close()  # Close existing connection if open
        try:
            if not self.port:
                raise ValueError("Port must be specified either in __init__ or open()")
            
            self.serial_conn = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
            print(f"Connected to Arduino on {self.port} at {self.baudrate} baud")
            time.sleep(2)  # Give Arduino time to initialize
        
        except serial.SerialException as e:
            print(f"Error opening serial port {self.port}: {e}", file=sys.stderr)
            raise
    
    def close(self):
        """Close the serial connection"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Serial connection closed")

    def read_data(self, num_samples=None):
        """
        Read temperature and humidity data from Arduino.
        
        Args:
            num_samples (int): Number of data samples to read (None for continuous)
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise RuntimeError("Serial connection not open. Call open() first.")
        
        if num_samples is not None:
            print(f"Reading {num_samples} samples from Arduino...")
        else:
            print("Reading non-stop data from Arduino (press Ctrl+C to stop)...")

        sample_count = 0
        
        try:
            while True:
                if num_samples and sample_count >= num_samples:
                    break
                
                # Read a line from serial
                if self.serial_conn.in_waiting > 0:
                    line = self.serial_conn.readline().decode('utf-8').strip()
                    
                    if line:
                        print(line)
                        sample_count += 1
                
                time.sleep(0.1)  # Small delay to prevent CPU spinning
        
        except KeyboardInterrupt:
            print("\nStopped reading data")
        except Exception as e:
            print(f"Error reading serial data: {e}", file=sys.stderr)
            raise

arduino_interface = ArduinoInterface(port='COM3')  # Update with your port
arduino_interface.open()
arduino_interface.read_data(num_samples=100)  # Read 100 samples, or set to None for continuous
arduino_interface.close()