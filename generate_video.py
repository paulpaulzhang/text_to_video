# -*- coding: utf-8 -*-
import os
from moviepy.editor import (
    ImageSequenceClip,
    AudioFileClip,
    concatenate_videoclips,
    VideoFileClip,
)
from moviepy.video.fx.all import scroll, fadein, fadeout
import numpy as np
import cv2
import random
import subprocess


def fl_left(gf, t):
    # 获取原始图像帧
    frame = gf(t)

    height, width = frame.shape[:2]
    scroll_x = int(t * 5)  # 根据时间t计算偏移的像素数
    new_frame = np.zeros_like(frame)

    # 控制偏移的范围，避免偏移超出图像的边界
    if scroll_x < width:
        new_frame[:, : width - scroll_x] = frame[:, scroll_x:]

    return new_frame


def fl_right(gf, t):
    # 获取原始图像帧
    frame = gf(t)

    height, width = frame.shape[:2]
    scroll_x = int(t * 5)  # 根据时间t计算滚动的像素数
    new_frame = np.zeros_like(frame)

    # 控制滚动的范围，避免滚动超出图像的边界
    if scroll_x < width:
        new_frame[:, scroll_x:] = frame[:, : width - scroll_x]

    return new_frame


def fl_up(gf, t):
    # 获取原始图像帧
    frame = gf(t)

    height, width = frame.shape[:2]
    scroll_y = int(t * 15)  # 根据时间t计算滚动的像素数
    new_frame = np.zeros_like(frame)

    # 控制滚动的范围，避免滚动超出图像的边界
    if scroll_y < height:
        new_frame[: height - scroll_y, :] = frame[scroll_y:, :]
        new_frame[height - max(scroll_y, 1) :, :] = cv2.GaussianBlur(
            frame[height - max(scroll_y, 1) :, :], (0, 0), sigmaX=50
        )
    else:
        new_frame = frame

    return new_frame


def fl_down(gf, t):
    # 获取原始图像帧
    frame = gf(t)

    height, width = frame.shape[:2]
    scroll_y = int(t * 15)  # 根据时间t计算滚动的像素数
    new_frame = np.zeros_like(frame)

    # 控制滚动的范围，避免滚动超出图像的边界
    if scroll_y < height:
        new_frame[scroll_y:, :] = frame[: height - scroll_y, :]
        new_frame[: max(scroll_y, 1) :, :] = cv2.GaussianBlur(
            frame[: max(scroll_y, 1) :, :], (0, 0), sigmaX=50
        )
    else:
        new_frame = frame

    return new_frame


class VideoGenerator:
    def __init__(self, config):
        self.config = config
        self.scroll_func = None

    def generate_video(self, image_paths, audio_paths):
        cached_clips = []  # 用于缓存视频剪辑的列表
        for i, (image_path, audio_path) in enumerate(zip(image_paths, audio_paths)):
            print(image_path, audio_path)
            audio_clip = AudioFileClip(audio_path)
            img_clip = ImageSequenceClip(
                [image_path], fps=30, durations=audio_clip.duration
            )
            if i % 2 == 0:
                img_clip = (
                    img_clip.set_position(("center", "center"))
                    .fl(fl_up, apply_to=["mask"])
                    .set_duration(audio_clip.duration)
                )
            else:
                img_clip = (
                    img_clip.set_position(("center", "center"))
                    .fl(fl_down, apply_to=["mask"])
                    .set_duration(audio_clip.duration)
                )
            clip = img_clip.set_audio(audio_clip)

            # 生成一个临时文件名，用于缓存当前视频剪辑
            os.makedirs(f"{self.config.work_dir}/cache", exist_ok=True)
            temp_file = f"{self.config.work_dir}/cache/temp_{i}.mp4"
            clip.write_videofile(temp_file, fps=30, audio_codec="aac")
            cached_clips.append(temp_file)  # 将临时文件名添加到缓存列表中
            audio_clip.close()

        with open(f"{self.config.work_dir}/cache/temp.txt", "w") as file_list:
            for file_path in cached_clips:
                file_name = file_path.split("/")[-1]
                file_list.write(f"file '{file_name}'\n")

        if os.path.exists(f"{self.config.work_dir}/draft.mp4"):
            os.remove(f"{self.config.work_dir}/draft.mp4")
        self.concatenate_videos(
            f"{self.config.work_dir}/cache/temp.txt",
            f"{self.config.work_dir}/draft.mp4",
        )

        # 删除临时文件
        for temp_file in cached_clips:
            os.remove(temp_file)
        os.remove(f"{self.config.work_dir}/cache/temp.txt")
        os.removedirs(f"{self.config.work_dir}/cache")

    def concatenate_videos(self, path_file, output_file):
        # 使用concat协议将视频文件直接拼接
        cmd = [
            "ffmpeg",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            path_file,
            "-c",
            "copy",
            output_file,
        ]
        subprocess.run(cmd)
