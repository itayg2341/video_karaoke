import json
import sys
from moviepy.editor import *

def main(json_file, background_image, output_video, audio_file=None):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    duration = data['duration']
    segments = data['segments']
    
    # Background image
    bg = ImageClip(background_image).set_duration(duration)
    
    # Video parameters (adjust as needed)
    screen_width = 1920  # Assume 1920x1080 video
    screen_height = 1080
    font = 'Arial'  # Font that supports Hebrew
    fontsize = 70
    color_gray = 'gray'
    color_highlight = 'yellow'
    y_pos = screen_height - 200  # Position near bottom
    
    all_clips = []
    
    space_clip = TextClip(" ", font=font, fontsize=fontsize, color=color_gray)
    space_width = space_clip.w
    
    for segment in segments:
        words = segment['words']
        if not words:
            continue
        
        word_texts = [w['word'] for w in words]
        gray_clips = [TextClip(txt, font=font, fontsize=fontsize, color=color_gray) for txt in word_texts]
        highlight_clips = [TextClip(txt, font=font, fontsize=fontsize, color=color_highlight) for txt in word_texts]
        
        widths = [c.w for c in gray_clips]
        
        # Calculate total width including spaces
        num_spaces = len(words) - 1 if len(words) > 1 else 0
        total_width = sum(widths) + space_width * num_spaces
        
        # For RTL (Hebrew): Start from the right
        line_right = screen_width / 2 + total_width / 2
        current_x = line_right - widths[0]
        
        line_gray = []
        line_highlight = []
        
        # Place first word
        g = gray_clips[0].set_pos((current_x, y_pos))
        h = highlight_clips[0].set_pos((current_x, y_pos))
        end = words[1]['start'] if len(words) > 1 else segment['end']
        h = h.set_start(words[0]['start']).set_end(end)
        line_gray.append(g)
        line_highlight.append(h)
        
        # Place subsequent words to the left
        for i in range(1, len(words)):
            current_x -= space_width + widths[i]
            g = gray_clips[i].set_pos((current_x, y_pos))
            h = highlight_clips[i].set_pos((current_x, y_pos))
            end = words[i+1]['start'] if i+1 < len(words) else segment['end']
            h = h.set_start(words[i]['start']).set_end(end)
            line_gray.append(g)
            line_highlight.append(h)
        
        # Set duration for gray clips (whole segment)
        line_gray = [g.set_start(segment['start']).set_end(segment['end']) for g in line_gray]
        
        # Combine into segment clip
        segment_clip = CompositeVideoClip(line_gray + line_highlight)
        all_clips.append(segment_clip)
    
    # Final video
    video = CompositeVideoClip([bg] + all_clips).set_duration(duration)
    
    if audio_file:
        audio = AudioFileClip(audio_file)
        video = video.set_audio(audio)
    
    # Write video (install ImageMagick for TextClip to work)
    video.write_videofile(output_video, fps=24, codec='libx264', audio_codec='aac' if audio_file else None)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python karaoke_script.py lyrics.json background.jpg output.mp4 [audio.mp3]")
        sys.exit(1)
    
    json_file = sys.argv[1]
    bg_image = sys.argv[2]
    out_video = sys.argv[3]
    audio = sys.argv[4] if len(sys.argv) > 4 else None
    
    main(json_file, bg_image, out_video, audio)