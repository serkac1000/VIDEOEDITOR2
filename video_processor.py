import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import tempfile

class VideoProcessor:
    def __init__(self):
        pass
    
    def edit_video(self, input_video, start_time, end_time, output_path, progress_callback=None):
        """Cut video segment and save as new MP4 file."""
        video = None
        edited_video = None
        
        try:
            # Load video
            if progress_callback:
                progress_callback(0.1)
            
            video = VideoFileClip(input_video)
            
            # Validate time codes
            if start_time < 0 or end_time <= start_time:
                raise Exception("Invalid time codes")
            
            if end_time > video.duration:
                raise Exception(f"End time {end_time}s exceeds video duration {video.duration:.1f}s")
            
            if progress_callback:
                progress_callback(0.2)
            
            # Create video clip
            edited_video = video.subclip(start_time, end_time)
            
            if progress_callback:
                progress_callback(0.3)
            
            # Write video file with progress callback
            def write_progress_callback(progress):
                if progress_callback:
                    # Map moviepy progress (0-1) to our progress (0.3-1.0)
                    mapped_progress = 0.3 + (progress * 0.7)
                    progress_callback(mapped_progress)
            
            # Write the video file
            edited_video.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                temp_audiofile=tempfile.mktemp(suffix='.m4a'),
                remove_temp=True,
                verbose=False,
                logger=None
            )
            
            if progress_callback:
                progress_callback(1.0)
            
            return True
            
        except Exception as e:
            raise Exception(f"Video processing failed: {str(e)}")
        
        finally:
            # Clean up video objects
            if edited_video:
                try:
                    edited_video.close()
                except:
                    pass
            
            if video:
                try:
                    video.close()
                except:
                    pass
    
    def get_video_info(self, video_path):
        """Get basic information about a video file."""
        video = None
        try:
            video = VideoFileClip(video_path)
            info = {
                'duration': video.duration,
                'fps': video.fps,
                'size': video.size,
                'has_audio': video.audio is not None
            }
            return info
        except Exception as e:
            raise Exception(f"Could not get video info: {str(e)}")
        finally:
            if video:
                try:
                    video.close()
                except:
                    pass
