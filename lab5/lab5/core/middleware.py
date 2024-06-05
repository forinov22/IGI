import requests
from datetime import datetime, timezone, timedelta
from django.utils.deprecation import MiddlewareMixin
import pytz


class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        response = requests.get("https://api.ipify.org/?format=json")

        if response.status_code == 200:
            data = response.json()
            ip_address = data.get("ip")

            if ip_address:
                response = requests.get(f"https://ipinfo.io/{ip_address}/json")

                if response.status_code == 200:
                    data = response.json()
                    tz = data.get("timezone")

                    if tz:
                        # Get the time zone offset
                        tz_offset = pytz.timezone(tz).utcoffset(datetime.utcnow())
                        tz_offset_minutes = int(tz_offset.total_seconds() / 60)

                        # Get the current time in UTC
                        utc_time = datetime.utcnow()

                        # Create a timezone object with the offset
                        tz = timezone(timedelta(minutes=tz_offset_minutes))

                        # Convert the UTC time to the specified timezone
                        current_time = utc_time.replace(tzinfo=timezone.utc).astimezone(tz)
                        request.current_time = current_time
