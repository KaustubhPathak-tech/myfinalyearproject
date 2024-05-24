# projectapi/management/commands/run_sensor_data.py
from django.core.management.base import BaseCommand
from projectapi.models import SensorData 
import sqlite3
from datetime import datetime
import telnetlib

class Command(BaseCommand):
    help = 'Runs a script to fetch sensor data and store it in the SQLite database'

    def handle(self, *args, **options):
        # Connect to the SQLite database
        conn = sqlite3.connect('db.sqlite3') 
        c = conn.cursor()

        # # Create table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS projectapi_sensordata
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      timestamp TEXT,
                      temperature REAL,
                      humidity REAL)''')

        # Telnet parameters
        host = '192.168.137.226'
        port = 8080 

        # Connect to Telnet server
        tn = telnetlib.Telnet(host, port)

        try:
            while True:
                try:
                    # Read data from Telnet connection
                    data = tn.read_until(b'\r\n').decode().strip()
                    print(data)
                    # Split the data into temperature, humidity
                    temp_str, humidity_str = data.split(',')                      
                    temperature = float(temp_str.split(' ')[0].strip())
                    humidity = float(humidity_str.split(' ')[0].strip())

                    # Get current timestamp
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # Insert data into the database
                    # c.execute("INSERT INTO projectapi_sensordata (timestamp, temperature, humidity) VALUES (?, ?, ?)", (timestamp, temperature, humidity))
                    # conn.commit()
                    SensorData.objects.create(timestamp=timestamp, temperature=temperature, humidity=humidity)

                    self.stdout.write(self.style.SUCCESS(f'Data inserted at {timestamp}: Temperature={temperature}, Humidity={humidity}'))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Error: {e}'))
                    # Handle errors as needed

        finally:
            # Close the Telnet connection and database connection when done
            tn.close()
            conn.close()
