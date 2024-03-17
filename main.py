from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
# Consider using MDFileManager from KivyMD
# from kivymd.uix.filemanager import MDFileManager
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.clock import Clock
from requests.exceptions import RequestException
import requests

class DiscordFileSenderApp(App):
    selected_file = StringProperty("")
    webhook_url = StringProperty("https://discord.com/api/webhooks/1218750401319403581/yNudkDzklXBVmHLE33U8CBzhQvlELjPt9c1srIo-d4ERqWLqUhn3B2u6UHjynW5C0320")  # Replace with your webhook URL

    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=dp(20), padding=dp(20))

        layout.add_widget(Label(text="Select a File", font_size=dp(20), size_hint=(1, 0.1)))

        try:
            self.file_chooser = FileChooserListView(size_hint=(1, 0.7))
            self.file_chooser.bind(selection=self.update_confirm_button_state)
            layout.add_widget(self.file_chooser)
        except PermissionError:
            layout.add_widget(Label(text="Permission denied to access files"))

        self.confirm_button = Button(text="Confirm", disabled=True,
                                     background_color=(0.1, 0.6, 0.1, 1),
                                     size_hint=(1, 0.1))
        self.confirm_button.bind(on_release=self.send_file)
        layout.add_widget(self.confirm_button)

        return layout

    def update_confirm_button_state(self, instance, value):
        self.confirm_button.disabled = not value
        self.selected_file = value and value[0] or ""

    def send_file(self, instance):
        if self.selected_file:
            payload = {"content": f"File selected: {self.selected_file}"}
            

            try:
                with open(self.selected_file, 'rb') as f:
                    file_data = f.read()
                files = {'file': (self.selected_file.split('/')[-1], file_data)}

                response = requests.post(self.webhook_url, data=payload, files=files)
                response.raise_for_status()

                self.success_popup("File sent successfully!")
                self.selected_file = ""
                self.confirm_button.disabled = True
            except RequestException as e:
                self.error_popup(f"Error sending file: {str(e)}")
            finally:
                Clock.schedule_once(lambda dt: setattr(self.confirm_button, 'disabled', False))

    def success_popup(self, message):
        popup = Popup(title="Success", content=Label(text=message),
                      size_hint=(None, None), size=(400, 100))
        popup.open()

    def error_popup(self, message):
        popup = Popup(title="Error", content=Label(text=message),
                      size_hint=(None, None), size=(400, 100))
        popup.open()

if __name__ == '__main__':
    DiscordFileSenderApp().run()
