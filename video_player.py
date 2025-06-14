import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
import time

class VideoPlayer:
    def __init__(self, parent_frame, position_callback=None):
        self.parent_frame = parent_frame
        self.position_callback = position_callback
        
        # Video properties
        self.cap = None
        self.video_path = None
        self.fps = 30
        self.total_frames = 0
        self.current_frame = 0
        self.duration = 0
        
        # Playback control
        self.is_playing = False
        self.playback_thread = None
        
        # Create video display label
        self.video_label = tk.Label(parent_frame, bg='black')
        self.video_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Display placeholder
        self.show_placeholder()
    
    def show_placeholder(self):
        """Show placeholder when no video is loaded."""
        placeholder_text = "No video loaded\nSelect a video file to begin"
        self.video_label.config(text=placeholder_text, fg='white', font=('Arial', 14))
    
    def load_video(self, video_path):
        """Load a video file."""
        try:
            # Release previous video if any
            if self.cap:
                self.cap.release()
            
            self.video_path = video_path
            self.cap = cv2.VideoCapture(video_path)
            
            if not self.cap.isOpened():
                raise Exception("Could not open video file")
            
            # Get video properties
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.duration = self.total_frames / self.fps if self.fps > 0 else 0
            
            # Reset position
            self.current_frame = 0
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            # Display first frame
            self.display_current_frame()
            
            return True
            
        except Exception as e:
            raise Exception(f"Failed to load video: {str(e)}")
    
    def display_current_frame(self):
        """Display the current frame."""
        if not self.cap:
            return
        
        ret, frame = self.cap.read()
        if ret:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Resize frame to fit display
            frame_resized = self.resize_frame(frame_rgb)
            
            # Convert to PhotoImage
            image = Image.fromarray(frame_resized)
            photo = ImageTk.PhotoImage(image)
            
            # Update label
            self.video_label.config(image=photo, text="")
            self.video_label.image = photo  # Keep a reference
            
            # Update position callback
            if self.position_callback:
                position = self.current_frame / self.fps if self.fps > 0 else 0
                self.position_callback(position, self.duration)
    
    def resize_frame(self, frame):
        """Resize frame to fit the display area while maintaining aspect ratio."""
        # Get display area size
        display_width = self.parent_frame.winfo_width()
        display_height = self.parent_frame.winfo_height()
        
        if display_width <= 1 or display_height <= 1:
            # Use default size if window not yet rendered
            display_width = 640
            display_height = 480
        
        # Get frame dimensions
        frame_height, frame_width = frame.shape[:2]
        
        # Calculate scaling factor
        scale_w = display_width / frame_width
        scale_h = display_height / frame_height
        scale = min(scale_w, scale_h, 1.0)  # Don't upscale
        
        # Calculate new dimensions
        new_width = int(frame_width * scale)
        new_height = int(frame_height * scale)
        
        # Resize frame
        return cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    def play(self):
        """Start video playback."""
        if not self.cap:
            raise Exception("No video loaded")
        
        if not self.is_playing:
            self.is_playing = True
            self.playback_thread = threading.Thread(target=self._playback_loop, daemon=True)
            self.playback_thread.start()
    
    def pause(self):
        """Pause video playback."""
        self.is_playing = False
    
    def stop(self):
        """Stop video playback and reset to beginning."""
        self.is_playing = False
        if self.cap:
            self.current_frame = 0
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.display_current_frame()
    
    def seek(self, position_seconds):
        """Seek to specific position in seconds."""
        if not self.cap:
            return
        
        # Calculate frame number
        target_frame = int(position_seconds * self.fps)
        target_frame = max(0, min(target_frame, self.total_frames - 1))
        
        # Set position
        self.current_frame = target_frame
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        
        # Display frame
        self.display_current_frame()
    
    def get_position(self):
        """Get current position in seconds."""
        if not self.cap or self.fps <= 0:
            return 0
        return self.current_frame / self.fps
    
    def get_duration(self):
        """Get video duration in seconds."""
        return self.duration
    
    def _playback_loop(self):
        """Main playback loop running in separate thread."""
        frame_time = 1.0 / self.fps if self.fps > 0 else 1.0 / 30
        
        while self.is_playing and self.cap:
            start_time = time.time()
            
            # Check if we've reached the end
            if self.current_frame >= self.total_frames - 1:
                self.is_playing = False
                break
            
            # Move to next frame
            self.current_frame += 1
            
            # Display frame (need to use after() for thread-safe GUI updates)
            self.parent_frame.after(0, self.display_current_frame)
            
            # Control playback speed
            elapsed = time.time() - start_time
            sleep_time = max(0, frame_time - elapsed)
            time.sleep(sleep_time)
    
    def release(self):
        """Release video resources."""
        self.is_playing = False
        if self.cap:
            self.cap.release()
            self.cap = None
