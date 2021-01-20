from allauth.socialaccount.models import SocialApp
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.utils.timezone import now, timedelta
from rest_framework import serializers
from rest_framework.response import Response
from bikesharing.models import (
    Bike,
    Location,
    LocationTracker,
    Lock,
    LockType,
    Rent,
    Station,
    InvoxiaTrackerUpdate,
)
from cykel.models import CykelLogEntry

class ListInvoxiaLocationTrackerUpdateSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        tracker_updates = [InvoxiaTrackerUpdate(**item) for item in validated_data]
        tracker_update = InvoxiaTrackerUpdate.objects.bulk_create(tracker_updates)
        for update in tracker_update:
            tracker = LocationTracker.objects.get(device_id=update.serial)
            tracker.last_reported = now()
            tracker.battery_voltage = update.energy_level
            tracker.save()
            if (
                tracker.battery_voltage is not None
                and tracker.tracker_type is not None
            ):
                data = {"voltage": self.instance.battery_voltage}
                action_type = None
                action_type_prefix = "cykel.tracker"

                if tracker.bike:
                    data["bike_id"] = self.instance.bike.pk
                    action_type_prefix = "cykel.bike.tracker"

                if (
                    tracker.tracker_type.battery_voltage_critical is not None
                    and tracker.battery_voltage
                    <= tracker.tracker_type.battery_voltage_critical
                ):
                    action_type = "battery.critical"
                elif (
                    tracker.tracker_type.battery_voltage_warning is not None
                    and tracker.battery_voltage
                    <= tracker.tracker_type.battery_voltage_warning
                ):
                    action_type = "battery.warning"

                if action_type is not None:
                    action_type = "{}.{}".format(action_type_prefix, action_type)
                    somehoursago = now() - timedelta(hours=48)
                    CykelLogEntry.create_unless_time(
                        somehoursago,
                        content_object=self.instance,
                        action_type=action_type,
                        data=data,
                    )
                
                lat = update.lat
                lng = update.lng
                accuracy = update.precision
                loc = None

                if lat and lng:
                    loc = Location(
                        source=Location.Source.TRACKER,
                        reported_at=now(),
                        tracker=tracker,
                        geo=Point(float(lng), float(lat), srid=4326),
                    )
                    if tracker.bike:
                        loc.bike = tracker.bike
                    if accuracy:
                        loc.accuracy = accuracy
                    loc.save()

                if tracker.bike:
                    bike = tracker.bike
                    bike.last_reported = now()

                    if loc and not loc.internal:
                        # check if bike is near station and assign it to that station
                        # distance ist configured in prefernces
                        max_distance = preferences.BikeSharePreferences.station_match_max_distance
                        station_closer_than_Xm = Station.objects.filter(
                            location__distance_lte=(loc.geo, D(m=max_distance)),
                            status=Station.Status.ACTIVE,
                        ).first()
                        if station_closer_than_Xm:
                            bike.current_station = station_closer_than_Xm
                        else:
                            bike.current_station = None

                    bike.save()

                someminutesago = now() - timedelta(minutes=15)
                data = {}
                if loc:
                    data = {"location_id": loc.id}

                if tracker.tracker_status == LocationTracker.Status.MISSING:
                    action_type = "cykel.tracker.missing_reporting"
                    CykelLogEntry.create_unless_time(
                        someminutesago, content_object=tracker, action_type=action_type, data=data
                    )

                if tracker.bike and tracker.bike.state == Bike.State.MISSING:
                    action_type = "cykel.bike.missing_reporting"
                    CykelLogEntry.create_unless_time(
                        someminutesago,
                        content_object=tracker.bike,
                        action_type=action_type,
                        data=data,
                        )
        return tracker_update

class InvoxiaLocationTrackerUpdateSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if (data.get("lat") is None and data.get("lng") is not None) or (
            data.get("lat") is not None and data.get("lng") is None
        ):
            raise serializers.ValidationError("lat and lng must be defined together")
        return data

    class Meta:
        list_serializer_class = ListInvoxiaLocationTrackerUpdateSerializer
        model = InvoxiaTrackerUpdate
        fields = '__all__'