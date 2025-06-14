import os
import requests
import numpy as np
import re
import tempfile

# Try to import audio libraries, handle gracefully if not available
try:
    import sounddevice as sd
    import scipy.io.wavfile as wavfile
    AUDIO_AVAILABLE = True
except (ImportError, OSError) as e:
    AUDIO_AVAILABLE = False
    print(f"Audio recording not available: {e}")
    # Create dummy modules to prevent import errors
    class DummyModule:
        def __getattr__(self, name):
            def dummy_func(*args, **kwargs):
                raise RuntimeError("Audio recording is not available on this system")
            return dummy_func
    sd = DummyModule()
    wavfile = DummyModule()

class AudioProcessor:
    def __init__(self):
        self.api_token = None
        self.api_url = "https://api-inference.huggingface.co/models/facebook/wav2vec2-base-960h"
    
    def set_api_token(self, token):
        """Set the Hugging Face API token."""
        self.api_token = token
    
    def test_api(self, token):
        """Test the Hugging Face API connection."""
        if not token:
            return False
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create a small test audio file
        sample_rate = 16000
        duration = 1  # 1 second
        frequency = 440  # A4 note
        
        # Generate a simple sine wave
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio_data = np.sin(2 * np.pi * frequency * t) * 0.3
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        try:
            wavfile.write(temp_file.name, sample_rate, audio_data.astype(np.float32))
            
            # Test API
            with open(temp_file.name, "rb") as f:
                data = f.read()
            
            response = requests.post(self.api_url, headers=headers, data=data, timeout=30)
            
            # Clean up
            os.unlink(temp_file.name)
            
            return response.status_code == 200
            
        except Exception:
            # Clean up on error
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
            return False
    
    def record_audio(self, duration=5, samplerate=16000):
        """Record audio for the specified duration and save as WAV."""
        if not AUDIO_AVAILABLE:
            raise RuntimeError("Audio recording is not available on this system")
        
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.float32)
        sd.wait()  # Wait for recording to complete
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        wavfile.write(temp_file.name, samplerate, recording)
        
        return temp_file.name
    
    def transcribe_audio(self, audio_file):
        """Transcribe audio using Hugging Face API."""
        if not self.api_token:
            raise Exception("API token not set")
        
        headers = {"Authorization": f"Bearer {self.api_token}"}
        
        with open(audio_file, "rb") as f:
            data = f.read()
        
        response = requests.post(self.api_url, headers=headers, data=data, timeout=60)
        
        if response.status_code != 200:
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")
        
        try:
            result = response.json()
        except ValueError:
            raise Exception(f"Invalid JSON response: {response.text}")
        
        if "text" in result:
            return result["text"].lower().strip()
        elif "error" in result:
            raise Exception(f"API error: {result['error']}")
        else:
            raise Exception(f"Unexpected response format: {result}")
    
    def parse_time_codes(self, command):
        """Parse time codes from voice command (e.g., 'cut from 10 to 20 seconds')."""
        # Try different patterns
        patterns = [
            r"cut from (\d+) to (\d+) seconds?",
            r"from (\d+) to (\d+) seconds?",
            r"(\d+) to (\d+) seconds?",
            r"start (\d+) end (\d+)",
            r"begin (\d+) finish (\d+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command.lower())
            if match:
                start_time = int(match.group(1))
                end_time = int(match.group(2))
                if start_time < end_time:
                    return start_time, end_time
        
        return None, None
