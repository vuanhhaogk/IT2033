import sys
import cv2
import math
import numpy as np
from keras.models import load_model
from constants import BASE_SIZE, SECRET
from utils import load_video_to_frames, normalize_batch, denormalize_batch, update_progress, save_frames_to_video, unshuffle

def run_reveal(container_frames):
  model = load_model('./models/reveal.h5', compile=False)
  num_frames = len(container_frames) // 4 * 4

  print('Reveal: %d frames' % (num_frames))

  container_frames = container_frames[:num_frames]

  secret_frames = []

  container_batch = []

  for i in range(num_frames):
    container = cv2.cvtColor(container_frames[i], cv2.COLOR_BGR2RGB)

    # Append frames to buffer
    container_batch.append(container)

    if (i + 1) % 4 == 0:
      # Convert images to float type 
      container_batch = np.float32(container_batch)/255.0
      
      # Predict outputs
      secret = model.predict([normalize_batch(container_batch)])

      # Postprocess secret image output  
      secret = denormalize_batch(secret)
      secret = np.squeeze(secret) * 255.0
      secret = np.uint8(secret)

      # Save secret output video
      for j in range(0, 4):
        secret_frames.append(secret[j][..., ::-1])

      # Empty temporary buffers
      container_batch = []

      # Update progress
      update_progress(i + 1, num_frames) 

  print()

  secret_frames = unshuffle(secret_frames, SECRET)

  return secret_frames

if __name__=="__main__":
  # reveal.py container_path output_secret_path

  container_frames = load_video_to_frames(sys.argv[1])

  print('Container: %d frames' % (len(container_frames)))

  secret_frames = run_reveal(container_frames)

  print('Secret: %d frames' % (len(secret_frames)))

  save_frames_to_video(secret_frames, sys.argv[2])

# python src/reveal.py outputs/container_video.avi outputs/output_secret_video.avi