from moviepy.editor import ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip
from PIL import Image
import numpy as np
import io

def create_storyboard_video(images_with_prompts, duration=3, resolution=(768, 768)):
    clips = []

    for idx, (prompt, image_bytes) in enumerate(images_with_prompts):
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            image_np = np.array(image)
            image_clip = ImageClip(image_np).resize(newsize=resolution).set_duration(duration)

            text = TextClip(prompt, fontsize=24, color='white', bg_color='black', size=resolution).set_duration(duration)
            text = text.set_position(("center", "bottom"))

            final_clip = CompositeVideoClip([image_clip, text])
            clips.append(final_clip)
        except Exception as e:
            print(f"❌ Error creating clip for Scene {idx + 1}: {e}")

    if not clips:
        raise Exception("⚠️ No valid clips were created.")

    video = concatenate_videoclips(clips, method="compose")
    output_path = "storyboard_video.mp4"
    video.write_videofile(output_path, fps=24, codec="libx264")
    return output_path
