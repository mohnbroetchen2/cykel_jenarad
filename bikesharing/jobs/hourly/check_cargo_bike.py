from django_extensions.management.jobs import HourlyJob
import json
from urllib.request import urlopen
from datetime import date, datetime

class Job(HourlyJob):
    help = "Checks the reservation for the Cargobike located at the Jeninchen"

    def execute(self):
        # executing empty sample job
        from django.core import management
        import logging
        from bikesharing.models import (
            Bike,
        )
        logger = logging.getLogger('mylogger')
        url = "https://cargo.reparier-cafe.de/rest/reservierungen/all"
        try:
            cargobike = Bike.objects.get(vehicle_identification_number="12345")
            if cargobike.state == "US":
                response = urlopen(url)
                data_json = json.loads(response.read())
                now = datetime.now()
                cargobikeinuse = 0

                if cargobike.availability_status == "AV": # prüfe ob eine Ausleihe in der nächsten Stunde geplant ist oder bereits begonnen hat
                    for entry in data_json:
                        daterange = entry["zeitraum"]
                        stop = len(daterange)
                        snake = daterange.find("~")
                        startrent = daterange[0:snake-1]
                        endrent = daterange[snake+2:stop]
                        t_start = datetime.strptime(startrent,"%Y-%m-%d %H:%M:%S")
                        t_end = datetime.strptime(endrent,"%Y-%m-%d %H:%M:%S")
                        diff = t_start - datetime.now()
                        diff_min = (diff.days * 24 * 60) + (diff.seconds/60)
                        
                        if diff_min > 0 and diff_min < 61: # Fahrrad wird in der nächsten Stunde ausgeliehen
                            cargobike.state = "IU"
                            cargobike.save()
                            cargobikeinuse = 1

                        if (now > t_start and now < t_end): # Fahrrad ist ausgeliehen
                            cargobike.state = "IU"
                            cargobike.save()
                            cargobikeinuse = 1
                        
                if cargobikeinuse == 0 and cargobike.availability_status == "IU":
                    cargobike.state = "AV"
                    cargobike.save()

        except BaseException as e:
            logger.error("Fehler check_cargo_bike: {}".format(e))
            management.call_command("clearsessions")

        management.call_command("clearsessions")
