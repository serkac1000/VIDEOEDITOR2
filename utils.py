def format_time(seconds):
    """Format seconds into MM:SS format."""
    if seconds < 0:
        return "00:00"
    
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def validate_time_input(time_str):
    """Validate and convert time input to float."""
    if not time_str or not time_str.strip():
        raise ValueError("Time cannot be empty")
    
    try:
        time_value = float(time_str.strip())
        if time_value < 0:
            raise ValueError("Time cannot be negative")
        return time_value
    except ValueError:
        raise ValueError(f"Invalid time format: '{time_str}'. Please enter a number.")

def ensure_mp4_extension(filename):
    """Ensure filename has .mp4 extension."""
    if not filename.lower().endswith('.mp4'):
        return filename + '.mp4'
    return filename

def sanitize_filename(filename):
    """Remove invalid characters from filename."""
    import re
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    return filename
