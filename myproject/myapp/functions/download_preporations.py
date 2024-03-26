import cv2
import os

def add_predictions_to_video(video_path, predictions, output_path):
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
    
    # Define the codec and create a VideoWriter object to write the video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # For an mp4 file
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Assuming 'predictions' is a dictionary with frame number as key and prediction as value
            if frame_count in predictions:
                # Write the prediction text on the bottom right of the frame
                text = predictions[frame_count]
                position = (frame_width - 400, frame_height - 10)  # Adjust position accordingly
                cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            out.write(frame)
            frame_count += 1
        else:
            break
    
    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()