import sys
import time
import threading


class ProgressIndicator:
    """Display a progress indicator with elapsed time for long-running operations."""

    def __init__(self, message: str = "Processing"):
        self.message = message
        self.running = False
        self.start_time = None
        self.thread = None
        self.frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.frame_index = 0

    def _format_time(self, seconds: float) -> str:
        """Format elapsed time as MM:SS."""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

    def _animate(self):
        """Animation loop that runs in a separate thread."""
        while self.running:
            elapsed = time.time() - self.start_time
            frame = self.frames[self.frame_index % len(self.frames)]
            time_str = self._format_time(elapsed)

            # Write to stderr to avoid mixing with stdout
            sys.stderr.write(f'\r{frame} {self.message}... ({time_str})')
            sys.stderr.flush()

            self.frame_index += 1
            time.sleep(0.1)

    def start(self):
        """Start the progress indicator."""
        self.running = True
        self.start_time = time.time()
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop the progress indicator and clear the line."""
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()
            # Clear the line
            sys.stderr.write('\r' + ' ' * 80 + '\r')
            sys.stderr.flush()

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
        return False
