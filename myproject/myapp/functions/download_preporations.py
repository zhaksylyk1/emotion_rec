import cv2
import os
from moviepy.editor import VideoFileClip


def add_predictions_to_video(video_path, predictions, output_folder):
    # Extract the filename from the input path and append "_new" before the extension
    filename = os.path.basename(video_path)
    base, extension = os.path.splitext(filename)
    output_filename = f"{base}_new{extension}"
    
    # Construct the output path using the output folder and the new filename
    output_path = os.path.join(output_folder, output_filename)
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    # Check if video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    # Get video properties
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)
    position = (50, 50)
    
    # Define the codec and create a VideoWriter object to write the video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # For an mp4 file
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    text = ""
    frame_count = 1
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Initialize text for each frame to avoid carrying over previous frames' text
            # Assuming 'predictions' is a dictionary with frame number as key and prediction as value
            if frame_count in predictions:
                # Write the prediction text on the bottom right of the frame
                text = predictions[frame_count]
            cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 2, (1, 1, 1), 2, cv2.LINE_AA)
            out.write(frame)
            frame_count += 1
        else:
            break
    
    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    final_output_path = os.path.join(output_folder, f"{base}_final{extension}")
    original_video = VideoFileClip(video_path)
    processed_video = VideoFileClip(output_path)
    # Extract audio from the original video
    audio = original_video.audio
    # Add the audio to the processed video
    processed_video_with_audio = processed_video.set_audio(audio)
    # Write the final video file with audio
    processed_video_with_audio.write_videofile(final_output_path, codec='libx264', audio_codec='aac')

    # Optionally, you might want to remove the intermediate video file without audio
    os.remove(output_path)