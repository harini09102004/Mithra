import datetime
import winsound
import time

def format_time_input(input_time):
    # Check if the input contains "AM" or "PM"
    if "AM" in input_time.upper() or "PM" in input_time.upper():
        # Remove "AM" or "PM" and strip spaces
        time_part = input_time.split()[0]
        # Handle single-digit hour and minute
        if len(time_part) == 3:  # e.g., "341"
            hour = time_part[0]
            minute = time_part[1:]
            formatted_time = f"{int(hour):02}:{int(minute):02}"
        elif len(time_part) == 4:  # e.g., "0341"
            hour = time_part[:2]
            minute = time_part[2:]
            formatted_time = f"{int(hour):02}:{int(minute):02}"
        else:  # for standard time like "3:41"
            formatted_time = time_part

        return formatted_time
    else:
        return input_time

def alarm(Timing):
    try:
        # Format the input time first
        Timing = format_time_input(Timing)
        
        # Convert the input string time into a datetime object
        alarm_time = datetime.datetime.strptime(Timing, "%H:%M").time()
        print(f"Done, alarm is set for {Timing}")

        # Continuously check if the current time matches the alarm time
        while True:
            current_time = datetime.datetime.now().time()

            # Trigger alarm if the current time matches the alarm time
            if current_time >= alarm_time:
                print("Alarm is running")

                # Play the alarm sound asynchronously
                winsound.PlaySound('C:\\mithra\\Perfect-(Mr-Jat.in).wav', winsound.SND_ASYNC)

                # Let the alarm play for 10 seconds, then stop
                time.sleep(10)
                winsound.PlaySound(None, winsound.SND_PURGE)  # Stop the sound
                break  # Exit the loop after the alarm has triggered

            # Sleep for a second before checking the time again
            time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")

# Example usage:
#alarm("341 PM")  # Call the function with the example input
