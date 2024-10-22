import numpy as np
import cv2
from moviepy.editor import ImageSequenceClip
import os

def process_state_image(state):
    state = state[0:84, 6:90]
    state = cv2.cvtColor(state, cv2.COLOR_BGR2GRAY)
    state = state.astype(np.float32)
    state /= 255.0
    return state

def generate_state_frame_stack_from_queue(deque):
    frame_stack = np.array(deque)
    # Move stack dimension to the channel dimension (stack, x, y) -> (x, y, stack)
    return frame_stack.reshape(3, 84, 84) # np.transpose(frame_stack, (1, 2, 0))


def export_video(frames, file_name):
    clip = ImageSequenceClip(frames, fps=30)
    os.system("export FFMPEG_BINARY=/usr/bin/ffmpeg")
    clip.write_videofile(f"/tmp/{file_name}.mp4",)