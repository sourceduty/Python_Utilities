import cv2
import numpy as np
from moviepy.editor import VideoFileClip
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None

    frame_diffs = []
    prev_frame = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if prev_frame is not None:
            frame_diff = cv2.absdiff(frame, prev_frame)
            non_zero_count = np.count_nonzero(frame_diff)
            frame_diffs.append(non_zero_count)

        prev_frame = frame

    cap.release()
    return frame_diffs

def split_video_into_clips(video_path, output_dir, text_widget, threshold_factor=0.1):
    text_widget.insert(tk.END, "Analyzing video...\n")
    frame_diffs = analyze_video(video_path)
    if frame_diffs is None:
        text_widget.insert(tk.END, "Error opening video file\n")
        return

    text_widget.insert(tk.END, "Video analysis complete. Processing...\n")

    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    clip_start_frame = 0
    clip_index = 0

    threshold = np.mean(frame_diffs) + np.std(frame_diffs) * threshold_factor

    def save_clip(start_frame, end_frame, clip_index):
        clip = VideoFileClip(video_path).subclip(start_frame / frame_rate, end_frame / frame_rate)
        output_path = os.path.join(output_dir, f"clip_{clip_index}.mp4")
        clip.write_videofile(output_path, codec="libx264")
        text_widget.insert(tk.END, f"Saved {output_path}\n")

    frame_number = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_number > 0:
            frame_diff = frame_diffs[frame_number - 1]
            # If the difference is significant, we assume it's a new clip
            if frame_diff > threshold:
                save_clip(clip_start_frame, frame_number, clip_index)
                clip_index += 1
                clip_start_frame = frame_number

        frame_number += 1

    # Save the last clip
    save_clip(clip_start_frame, frame_number, clip_index)
    cap.release()
    text_widget.insert(tk.END, "Video processing completed\n")

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Processor")

        self.frame = tk.Frame(root, bg="gray")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self.frame, bg="gray")
        self.button_frame.pack(pady=10)

        button_padding = {'padx': 5, 'pady': 5}

        self.load_video_button = tk.Button(self.button_frame, text="Load Video", command=self.load_video)
        self.load_video_button.pack(side=tk.LEFT, **button_padding)

        self.select_output_button = tk.Button(self.button_frame, text="Select Output", command=self.select_output)
        self.select_output_button.pack(side=tk.LEFT, **button_padding)

        self.clip_video_button = tk.Button(self.button_frame, text="Clip Video", command=self.clip_video)
        self.clip_video_button.pack(side=tk.LEFT, **button_padding)

        self.text_area = tk.Text(self.frame, bg="black", fg="yellow", height=10)
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=10)

        self.video_path = None
        self.output_dir = None

    def load_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
        if self.video_path:
            self.text_area.insert(tk.END, f"Loaded video: {self.video_path}\n")

    def select_output(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            self.text_area.insert(tk.END, f"Selected output folder: {self.output_dir}\n")

    def clip_video(self):
        if self.video_path and self.output_dir:
            threading.Thread(target=self.process_video).start()
        else:
            messagebox.showwarning("Input Missing", "Please load a video and select an output folder before clipping.")

    def process_video(self):
        try:
            self.text_area.insert(tk.END, "Starting video processing...\n")
            split_video_into_clips(self.video_path, self.output_dir, self.text_area)
        except Exception as e:
            self.text_area.insert(tk.END, f"An error occurred: {e}\n")
            messagebox.showerror("Error", f"An error occurred: {e}")

def main():
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.geometry("600x400")
    root.mainloop()

if __name__ == "__main__":
    main()
