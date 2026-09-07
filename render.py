import json
import os
import subprocess

# 1. Load the JSON Blueprint
with open('KGU_json.json', 'r') as f:
    data = json.load(f)

width = data['metadata']['width']
height = data['metadata']['height']
fps = data['metadata']['fps']

scene_files = []

# 2. Render each scene individually
for index, scene in enumerate(data['scenes']):
    duration = scene['duration']
    text = scene['text']
    bg_color = scene['bgColor']
    text_color = scene['textColor']
    
    output_filename = f"scene_{index}.mp4"
    scene_files.append(output_filename)
    
    print(f"Rendering Scene {index + 1}...")
    
    # Advanced FFmpeg command to create solid color background and overlay text
    # We use a built-in standard font, center the text, and set resolution
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", f"color=c={bg_color}:s={width}x{height}:d={duration}",
        "-vf", f"drawtext=text='{text}':fontcolor={text_color}:fontsize=70:x=(w-text_w)/2:y=(h-text_h)/2",
        "-c:v", "libx264", "-fpsmax", str(fps), output_filename
    ]
    subprocess.run(cmd, check=True)

# 3. Create a text list of all the scene files for concatenation
with open('concat_list.txt', 'w') as f:
    for scene_file in scene_files:
        f.write(f"file '{scene_file}'\n")

print("Stitching scenes together into final MP4...")

# 4. Merge all scenes into output.mp4
concat_cmd = [
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", 
    "-i", "concat_list.txt", 
    "-c", "copy", "output.mp4"
]
subprocess.run(concat_cmd, check=True)

print("Video generation complete! output.mp4 created.")