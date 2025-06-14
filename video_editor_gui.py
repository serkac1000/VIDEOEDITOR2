import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from video_player import VideoPlayer
from audio_processor import AudioProcessor
from video_processor import VideoProcessor
from utils import format_time, validate_time_input

class VideoEditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice-Controlled Video Editor")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize processors
        self.audio_processor = AudioProcessor()
        self.video_processor = VideoProcessor()
        
        # State variables
        self.current_video_file = None
        self.api_token = tk.StringVar()
        self.start_time = tk.StringVar()
        self.end_time = tk.StringVar()
        self.output_filename = tk.StringVar()
        self.transcribed_command = tk.StringVar()
        
        # Create GUI components
        self.create_widgets()
        
        # Initialize video player
        self.video_player = VideoPlayer(self.video_frame, self.on_position_change)
        
        # Set up logging
        self.setup_logging()
    
    def create_widgets(self):
        """Create and arrange all GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # API Token Section
        self.create_api_section(main_frame)
        
        # File Selection Section
        self.create_file_section(main_frame)
        
        # Video Player Section
        self.create_video_section(main_frame)
        
        # Controls Section
        self.create_controls_section(main_frame)
        
        # Voice Command Section
        self.create_voice_section(main_frame)
        
        # Manual Time Input Section
        self.create_time_section(main_frame)
        
        # Processing Section
        self.create_processing_section(main_frame)
        
        # Log Section
        self.create_log_section(main_frame)
    
    def create_api_section(self, parent):
        """Create API token input section."""
        api_frame = ttk.LabelFrame(parent, text="Hugging Face API Configuration", padding="5")
        api_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        api_frame.columnconfigure(1, weight=1)
        
        ttk.Label(api_frame, text="API Token:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        api_entry = ttk.Entry(api_frame, textvariable=self.api_token, show="*", width=50)
        api_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Set default token from environment or the one in the original script
        default_token = os.getenv("HUGGINGFACE_API_TOKEN", "hf_QDPvjMJZqKKXqRyEHggXMFPDmVTBQELf")
        self.api_token.set(default_token)
        
        ttk.Button(api_frame, text="Test API", command=self.test_api).grid(row=0, column=2, padx=(5, 0))
    
    def create_file_section(self, parent):
        """Create file selection section."""
        file_frame = ttk.LabelFrame(parent, text="File Selection", padding="5")
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="Input Video:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.file_label = ttk.Label(file_frame, text="No file selected", background="white", relief="sunken")
        self.file_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(file_frame, text="Browse", command=self.browse_video_file).grid(row=0, column=2, padx=(5, 0))
        
        ttk.Label(file_frame, text="Output Name:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        ttk.Entry(file_frame, textvariable=self.output_filename).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(5, 0))
        self.output_filename.set("edited_video")
    
    def create_video_section(self, parent):
        """Create video player section."""
        video_frame = ttk.LabelFrame(parent, text="Video Player", padding="5")
        video_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        video_frame.columnconfigure(0, weight=1)
        video_frame.rowconfigure(0, weight=1)
        
        # Video display frame
        self.video_frame = tk.Frame(video_frame, bg='black', height=400)
        self.video_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.video_frame.columnconfigure(0, weight=1)
        self.video_frame.rowconfigure(0, weight=1)
        
        # Video info frame
        info_frame = ttk.Frame(video_frame)
        info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        info_frame.columnconfigure(1, weight=1)
        
        ttk.Label(info_frame, text="Position:").grid(row=0, column=0, sticky=tk.W)
        self.position_label = ttk.Label(info_frame, text="00:00 / 00:00")
        self.position_label.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Position scale
        self.position_scale = ttk.Scale(info_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.on_scale_change)
        self.position_scale.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def create_controls_section(self, parent):
        """Create video control buttons."""
        controls_frame = ttk.Frame(parent)
        controls_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Button(controls_frame, text="Play", command=self.play_video).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="Pause", command=self.pause_video).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="Stop", command=self.stop_video).pack(side=tk.LEFT, padx=(0, 5))
    
    def create_voice_section(self, parent):
        """Create voice command section."""
        voice_frame = ttk.LabelFrame(parent, text="Voice Commands", padding="5")
        voice_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        voice_frame.columnconfigure(1, weight=1)
        
        ttk.Button(voice_frame, text="Record Command (5s)", command=self.record_voice_command).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Label(voice_frame, text="Transcribed:").grid(row=0, column=1, sticky=tk.W, padx=(0, 5))
        transcribed_entry = ttk.Entry(voice_frame, textvariable=self.transcribed_command, state="readonly")
        transcribed_entry.grid(row=0, column=2, sticky=(tk.W, tk.E))
    
    def create_time_section(self, parent):
        """Create manual time input section."""
        time_frame = ttk.LabelFrame(parent, text="Time Markers (seconds)", padding="5")
        time_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(time_frame, text="Start Time:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(time_frame, textvariable=self.start_time, width=10).grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(time_frame, text="End Time:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        ttk.Entry(time_frame, textvariable=self.end_time, width=10).grid(row=0, column=3, padx=(0, 20))
        
        ttk.Button(time_frame, text="Set Current as Start", command=self.set_current_as_start).grid(row=0, column=4, padx=(10, 5))
        ttk.Button(time_frame, text="Set Current as End", command=self.set_current_as_end).grid(row=0, column=5, padx=(5, 0))
    
    def create_processing_section(self, parent):
        """Create processing controls section."""
        process_frame = ttk.LabelFrame(parent, text="Video Processing", padding="5")
        process_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        process_frame.columnconfigure(1, weight=1)
        
        ttk.Button(process_frame, text="Cut and Save Video", command=self.cut_and_save_video).grid(row=0, column=0, padx=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(process_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.status_label = ttk.Label(process_frame, text="Ready")
        self.status_label.grid(row=0, column=2)
    
    def create_log_section(self, parent):
        """Create error/status log section."""
        log_frame = ttk.LabelFrame(parent, text="Log", padding="5")
        log_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Button(log_frame, text="Clear Log", command=self.clear_log).grid(row=1, column=0, pady=(5, 0))
    
    def setup_logging(self):
        """Set up logging functionality."""
        self.log("Video Editor GUI initialized successfully")
    
    def log(self, message, level="info"):
        """Add message to log display."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {level.upper()}: {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        
        # Color coding for different log levels
        if level == "error":
            self.log_text.insert(tk.END, log_message, "error")
        elif level == "warning":
            self.log_text.insert(tk.END, log_message, "warning")
        else:
            self.log_text.insert(tk.END, log_message)
        
        # Configure text tags for colors
        self.log_text.tag_config("error", foreground="red")
        self.log_text.tag_config("warning", foreground="orange")
        
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)
    
    def clear_log(self):
        """Clear the log display."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def test_api(self):
        """Test the Hugging Face API connection."""
        if not self.api_token.get().strip():
            self.log("Please enter a Hugging Face API token", "error")
            return
        
        self.log("Testing Hugging Face API connection...")
        threading.Thread(target=self._test_api_thread, daemon=True).start()
    
    def _test_api_thread(self):
        """Test API in separate thread."""
        try:
            success = self.audio_processor.test_api(self.api_token.get().strip())
            if success:
                self.log("API connection successful")
            else:
                self.log("API connection failed", "error")
        except Exception as e:
            self.log(f"API test error: {str(e)}", "error")
    
    def browse_video_file(self):
        """Open file dialog to select video file."""
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv"),
                ("MP4 files", "*.mp4"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.current_video_file = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.log(f"Selected video file: {os.path.basename(file_path)}")
            
            # Load video in player
            try:
                self.video_player.load_video(file_path)
                duration = self.video_player.get_duration()
                self.log(f"Video loaded successfully. Duration: {format_time(duration)}")
                self.position_scale.config(to=duration)
            except Exception as e:
                self.log(f"Error loading video: {str(e)}", "error")
    
    def play_video(self):
        """Play the loaded video."""
        if self.current_video_file:
            try:
                self.video_player.play()
                self.log("Video playback started")
            except Exception as e:
                self.log(f"Error playing video: {str(e)}", "error")
        else:
            self.log("No video file selected", "warning")
    
    def pause_video(self):
        """Pause video playback."""
        try:
            self.video_player.pause()
            self.log("Video playback paused")
        except Exception as e:
            self.log(f"Error pausing video: {str(e)}", "error")
    
    def stop_video(self):
        """Stop video playback."""
        try:
            self.video_player.stop()
            self.log("Video playback stopped")
        except Exception as e:
            self.log(f"Error stopping video: {str(e)}", "error")
    
    def on_position_change(self, position, duration):
        """Update position display when video position changes."""
        self.position_label.config(text=f"{format_time(position)} / {format_time(duration)}")
        self.position_scale.set(position)
    
    def on_scale_change(self, value):
        """Handle position scale changes."""
        try:
            position = float(value)
            self.video_player.seek(position)
        except Exception as e:
            self.log(f"Error seeking video: {str(e)}", "error")
    
    def record_voice_command(self):
        """Record and transcribe voice command."""
        if not self.api_token.get().strip():
            self.log("Please enter a Hugging Face API token first", "error")
            return
        
        self.log("Starting voice recording (5 seconds)...")
        self.status_label.config(text="Recording...")
        threading.Thread(target=self._record_voice_thread, daemon=True).start()
    
    def _record_voice_thread(self):
        """Record voice in separate thread."""
        try:
            # Set API token for audio processor
            self.audio_processor.set_api_token(self.api_token.get().strip())
            
            # Record audio
            audio_file = self.audio_processor.record_audio(duration=5)
            self.log("Voice recording completed, transcribing...")
            
            # Transcribe audio
            command = self.audio_processor.transcribe_audio(audio_file)
            self.transcribed_command.set(command)
            self.log(f"Transcribed command: '{command}'")
            
            # Parse time codes from command
            start_time, end_time = self.audio_processor.parse_time_codes(command)
            if start_time is not None and end_time is not None:
                self.start_time.set(str(start_time))
                self.end_time.set(str(end_time))
                self.log(f"Parsed time codes: {start_time}s to {end_time}s")
            else:
                self.log("Could not parse time codes from command. Use manual input or try again.", "warning")
            
            # Clean up audio file
            if os.path.exists(audio_file):
                os.remove(audio_file)
            
            self.root.after(0, lambda: self.status_label.config(text="Ready"))
            
        except Exception as e:
            self.log(f"Voice recording error: {str(e)}", "error")
            self.root.after(0, lambda: self.status_label.config(text="Error"))
    
    def set_current_as_start(self):
        """Set current video position as start time."""
        if self.current_video_file:
            try:
                position = self.video_player.get_position()
                self.start_time.set(str(int(position)))
                self.log(f"Start time set to {int(position)} seconds")
            except Exception as e:
                self.log(f"Error getting current position: {str(e)}", "error")
        else:
            self.log("No video file loaded", "warning")
    
    def set_current_as_end(self):
        """Set current video position as end time."""
        if self.current_video_file:
            try:
                position = self.video_player.get_position()
                self.end_time.set(str(int(position)))
                self.log(f"End time set to {int(position)} seconds")
            except Exception as e:
                self.log(f"Error getting current position: {str(e)}", "error")
        else:
            self.log("No video file loaded", "warning")
    
    def cut_and_save_video(self):
        """Cut and save the video based on time markers."""
        if not self.current_video_file:
            self.log("No video file selected", "error")
            return
        
        # Validate time inputs
        try:
            start = validate_time_input(self.start_time.get())
            end = validate_time_input(self.end_time.get())
        except ValueError as e:
            self.log(f"Invalid time input: {str(e)}", "error")
            return
        
        if start >= end:
            self.log("Start time must be less than end time", "error")
            return
        
        output_name = self.output_filename.get().strip()
        if not output_name:
            self.log("Please enter an output filename", "error")
            return
        
        # Ask for save location
        output_path = filedialog.asksaveasfilename(
            title="Save Edited Video",
            defaultextension=".mp4",
            initialname=f"{output_name}.mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        
        if not output_path:
            return
        
        self.log(f"Starting video processing: {start}s to {end}s")
        self.status_label.config(text="Processing...")
        self.progress_var.set(0)
        
        threading.Thread(target=self._cut_video_thread, args=(start, end, output_path), daemon=True).start()
    
    def _cut_video_thread(self, start_time, end_time, output_path):
        """Cut video in separate thread."""
        try:
            def progress_callback(progress):
                self.root.after(0, lambda: self.progress_var.set(progress * 100))
            
            success = self.video_processor.edit_video(
                self.current_video_file, 
                start_time, 
                end_time, 
                output_path, 
                progress_callback
            )
            
            if success:
                self.log(f"Video saved successfully: {os.path.basename(output_path)}")
                self.root.after(0, lambda: messagebox.showinfo("Success", f"Video saved to:\n{output_path}"))
            else:
                self.log("Video processing failed", "error")
            
            self.root.after(0, lambda: self.status_label.config(text="Ready"))
            self.root.after(0, lambda: self.progress_var.set(0))
            
        except Exception as e:
            self.log(f"Video processing error: {str(e)}", "error")
            self.root.after(0, lambda: self.status_label.config(text="Error"))
            self.root.after(0, lambda: self.progress_var.set(0))
