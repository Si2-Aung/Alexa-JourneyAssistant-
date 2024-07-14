from datetime import datetime, timedelta
import pytz

def get_currentTime_with_delta(delta):
    desired_timezone = pytz.timezone('Europe/Berlin')
    # Erhalten Sie die aktuelle UTC-Zeit
    current_utc_time = datetime.now(pytz.utc)
    # Konvertieren Sie die UTC-Zeit in die gewünschte Zeitzone
    current_time_in_desired_timezone = current_utc_time.astimezone(desired_timezone)
    # Zeitspanne (Delta) definieren, die Sie hinzufügen möchten (z.B. 5 Minuten)
    time_delta = timedelta(minutes=delta)
    # Fügen Sie die Zeitspanne zur aktuellen Zeit hinzu
    result_time = current_time_in_desired_timezone + time_delta

    return result_time
    