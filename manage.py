#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import subprocess

def run_sensor_script():
    """Function to run the start_sensor.py script."""
    try:
        print("Running start_sensor.py script...")
        subprocess.run([sys.executable, 'F:\\Study\\B. Tech\\Semester 8\\My Project\\projectapi\\projectapi\\management\\commands\\start_sensor.py'])
    except Exception as e:
        print(f"Failed to run start_sensor.py: {e}")





def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectapi.settings')
    try:
        from django.core.management import execute_from_command_line
        
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        
    # Start the sensor script in a new thread
    sensor_thread = threading.Thread(target=run_sensor_script)
    sensor_thread.start()
    
    
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
