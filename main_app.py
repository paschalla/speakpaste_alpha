import os
import sys
from datetime import datetime

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Static, RichLog

# Import self-contained modules
from recorder import AudioRecorder
from transcriber import Transcriber
from clipboard import copy_to_clipboard

class Speakpaste(App):
    """A hotkey-activated dictation TUI."""

    # MODIFICATION: Disable Textual's mouse capture.
    # This gives control back to the terminal, allowing you to select and
    # copy text from the log with your mouse.
    ENABLE_MOUSE_EVENTS = False

    BINDINGS = [
        ("space", "start_recording", "Record"),
        ("ctrl+q", "quit", "Quit"),
    ]

    CSS_PATH = "main_app.css"

    def __init__(self):
        super().__init__()
        try:
            self.recorder = AudioRecorder()
            self.transcriber = Transcriber()
        except Exception as e:
            print(f"Fatal Error during initialization: {e}", file=sys.stderr)
            sys.exit(1)
        self.is_recording = False

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Container(
            RichLog(highlight=True, markup=True, id="log"),
            Static("Press [b]SPACE[/b] to start recording. Press [b]Ctrl+Q[/b] to quit.", id="status"),
            id="app-grid"
        )
        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is first mounted."""
        self.query_one("#log").write("[bold green]Speakpaste Ready.[/bold green]")

    def update_status(self, message: str):
        """Helper method to update the status bar."""
        self.query_one("#status", Static).update(message)

    def start_recording(self) -> None:
        """Called when the user presses the 'space' key."""
        if self.is_recording:
            return

        self.is_recording = True
        self.update_status("[bold red]Listening...[/bold red] (Silence will stop recording)")
        self.run_worker(self.run_transcription, thread=True)

    def run_transcription(self) -> None:
        """This function runs in the background to handle the full workflow."""
        log = self.query_one("#log", RichLog)
        
        temp_audio_path = self.recorder.record_audio()
        
        if not temp_audio_path:
            self.call_from_thread(self.update_status, "[bold red]Recording failed or was empty.[/bold red] Press [b]SPACE[/b] to try again.")
            self.is_recording = False
            return

        self.call_from_thread(self.update_status, "[bold yellow]Transcribing...[/bold yellow]")
        transcribed_text = self.transcriber.transcribe_audio(temp_audio_path)

        try:
            os.remove(temp_audio_path)
        except OSError as e:
            self.call_from_thread(log.write, f"[red]Warning: Could not delete temp file {temp_audio_path}: {e}[/red]")

        if transcribed_text:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.call_from_thread(log.write, f"[dim]{timestamp}[/dim] - {transcribed_text}")
            copy_to_clipboard(transcribed_text)
            self.call_from_thread(self.update_status, "[bold green]Text copied to clipboard![/bold green] Press [b]SPACE[/b] to record again.")
        else:
            self.call_from_thread(self.update_status, "[bold red]Transcription failed.[/bold red] Press [b]SPACE[/b] to try again.")
            
        self.is_recording = False


def create_fresh_css(css_content):
    # Overwrite the CSS file every time to ensure changes are applied.
    with open("main_app.css", "w") as f:
        f.write(css_content)

if __name__ == "__main__":
    main_css = """
#app-grid {
    layout: vertical;
}

#log {
    height: 90%;
    /* MODIFICATION: Use a specific hex code for purple for consistency. */
    border: tall #9370DB;
}

#status {
    height: 10%;
    content-align: center middle;
    background: $surface-darken-1;
}
"""
    create_fresh_css(main_css)
    app = Speakpaste()
    app.run()