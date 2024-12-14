from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
import instaloader
import os

KV = '''
ScreenManager:
    MainScreen:

<MainScreen>:
    name: "main"
    MDBoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 20

        MDLabel:
            text: "Instagram Reel Downloader"
            halign: "center"
            font_style: "H4"

        MDTextField:
            id: url_input
            hint_text: "Enter Instagram Reel URL"
            helper_text: "Paste the reel link here"
            helper_text_mode: "on_focus"
            size_hint_x: None
            width: 300
            pos_hint: {"center_x": 0.5}

        MDRaisedButton:
            text: "Download Reel"
            pos_hint: {"center_x": 0.5}
            on_release: app.download_reel()

        MDProgressBar:
            id: progress_bar
            value: 0
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.8
'''

class MainScreen(Screen):
    pass

class ReelDownloaderApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def download_reel(self):
        url_input = self.root.get_screen('main').ids.url_input.text
        progress_bar = self.root.get_screen('main').ids.progress_bar

        if not url_input.strip():
            self.show_dialog("Error", "Please enter a valid Instagram Reel URL.")
            return

        try:
            progress_bar.value = 25  # Indicate progress
            # Initialize Instaloader
            loader = instaloader.Instaloader(
                download_pictures=False,
                download_video_thumbnails=False,
                download_geotags=False,
                save_metadata=False
            )
            # Extract shortcode
            shortcode = url_input.split("/")[-2]
            post = instaloader.Post.from_shortcode(loader.context, shortcode)

            # Create 'reels' folder if it doesn't exist
            if not os.path.exists("reels"):
                os.makedirs("reels")

            # Download the reel
            loader.download_post(post, target="reels")

            # Remove any .txt files generated in the 'reels' folder
            for file in os.listdir("reels"):
                if file.endswith(".txt"):
                    os.remove(os.path.join("reels", file))

            progress_bar.value = 100  # Indicate completion
            self.show_dialog("Success", "Reel downloaded successfully!")

        except Exception as e:
            progress_bar.value = 0
            self.show_dialog("Error", f"Failed to download reel: {e}")

    def show_dialog(self, title, text):
        if not self.dialog:
            self.dialog = MDDialog(
                title=title,
                text=text,
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=lambda x: self.dialog.dismiss()
                    )
                ]
            )
        else:
            self.dialog.title = title
            self.dialog.text = text

        self.dialog.open()

if __name__ == "__main__":
    ReelDownloaderApp().run()