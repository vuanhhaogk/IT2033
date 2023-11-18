import sys
import cv2
import math
import numpy as np
from keras.models import load_model
from constants import BASE_SIZE, SECRET
from utils import load_video_to_frames, normalize_batch, denormalize_batch, update_progress, save_frames_to_video, shuffle

def run_hide(cover_frames, secret_frames):
  model = load_model('./models/hide.h5', compile=False)
  num_frames = (min(len(cover_frames), len(secret_frames)) // 4) * 4

  print('Hiding: %d frames' % (num_frames))

  cover_frames = cover_frames[:num_frames]
  secret_frames = secret_frames[:num_frames]

  container_frames = []

  secret_batch=[]
  cover_batch=[]

  secret_frames = shuffle(secret_frames, SECRET)

  for i in range(num_frames):
    cover = cv2.resize(cv2.cvtColor(cover_frames[i], cv2.COLOR_BGR2RGB), (BASE_SIZE, BASE_SIZE) ,interpolation=cv2.INTER_AREA)
    secret = cv2.resize(cv2.cvtColor(secret_frames[i], cv2.COLOR_BGR2RGB), (BASE_SIZE, BASE_SIZE) ,interpolation=cv2.INTER_AREA)

    # Append frames to buffer
    cover_batch.append(cover)  
    secret_batch.append(secret)

    if (i + 1) % 4 == 0:
      # Convert images to float type 
      cover_batch = np.float32(cover_batch)/255.0    
      secret_batch = np.float32(secret_batch)/255.0
      
      # Predict outputs
      container = model.predict([normalize_batch(secret_batch),normalize_batch(cover_batch)])

      # Postprocess cover image output  
      container = denormalize_batch(container)
      container = np.squeeze(container) * 255.0
      container = np.uint8(container)

      # Save cover output video
      for j in range(0, 4):
        container_frames.append(container[j][..., ::-1])

      # Empty temporary buffers
      secret_batch = []
      cover_batch = []

      # Update progress
      update_progress(i + 1, num_frames) 

  print()

  return container_frames

if __name__=="__main__":
  # hide.py cover_path secret_path output_container_path

  cover_frames = load_video_to_frames(sys.argv[1])
  secret_frames = load_video_to_frames(sys.argv[2])

  print('Cover: %d frames' % (len(cover_frames)))
  print('Secret: %d frames' % (len(secret_frames)))

  container_frames = run_hide(cover_frames, secret_frames)

  print('Container: %d frames' % (len(container_frames)))

  save_frames_to_video(container_frames, sys.argv[3])

# python src/hide.py outputs/cover_video.mp4 outputs/secret_video.mp4 outputs/container_video.avi