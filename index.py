from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from plyer import gps
from plyer import notification

class TrenSit(App):

    CHANNEL_ID = "location_channel"
    DISTANCE_THRESHOLD = 100  # Distance threshold in meters

    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Waiting for GPS signal...")
        self.layout.add_widget(self.label)

        # Create notification channel
        notification.create_channel(self.CHANNEL_ID, name="Location Channel",
                                     description="Channel for location notifications")

        # Start GPS
        gps.configure(on_location=self.on_location)
        gps.start()

        return self.layout

    def on_location(self, **kwargs):
        latitude = kwargs.get('lat')
        longitude = kwargs.get('lon')
        accuracy = kwargs.get('accuracy')

        if latitude is not None and longitude is not None:
            self.label.text = f"Latitude: {latitude}, Longitude: {longitude}, Accuracy: {accuracy}m"

            # Check if the current location is close to the arrival location
            distance = self.calculate_distance(latitude, longitude)
            if distance <= self.DISTANCE_THRESHOLD:
                self.send_notification("You are close to the arrival location!")

    def calculate_distance(self, latitude, longitude):
        # Here you can calculate the distance using Haversine formula or any other method
        # For simplicity, let's assume a linear distance calculation
        return ((latitude - arrival_latitude) ** 2 + (longitude - arrival_longitude) ** 2) ** 0.5

    def send_notification(self, message):
        # Send notification
        notification.notify(title="Location Notification", message=message, app_icon='', app_name='Location App', timeout=10, channel_id=self.CHANNEL_ID)

    def on_stop(self):
        # Stop GPS when the app is closed
        gps.stop()


if __name__ == '__main__':
    TrenSit().run()
