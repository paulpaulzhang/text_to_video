import pandas as pd
import numpy as np
import os
from pathlib import Path
import gc
from tqdm import tqdm
import time

from config import Config
from lora import Lora

from generate_prompt import PromptGenerator
from generate_image import ImageGenerator
from generate_audio import AudioGenerator
from generate_video import VideoGenerator


config = Config()
lora = Lora()


def novel_preprocess(novel_path):
    with open(novel_path, "r", encoding="utf8") as f:
        lines = f.readlines()
        paras = []
        for line in lines:
            line = line.strip()
            if len(line) > 10:
                paras.append(line)
            else:
                if len(paras) == 0:
                    continue
                paras[-1] = paras[-1] + line

    return paras


def generate_storyboard_info(storyboards, style=""):
    print("生成分镜信息(分镜，场景，人物，提示词)...")
    with open(f"{config.work_dir}/storyboard_info.txt", "w", encoding="utf8") as f:
        f.write(
            "storyboard,style,scenery,character,character_num,lens_angle,content,lora_prompt\n"
        )
    prompt_generator = PromptGenerator(config)
    prompts = []
    lora_prompts = []
    sceneries = []
    characters = []
    character_nums = []
    lens_angles = []
    contents = []

    for storyboard in tqdm(storyboards):
        lora_prompt = ""

        for name in []:
            if name in storyboard:
                lora_prompt = ""
                lora_prompt += lora.boy1.name + lora.boy1.prompt  # 黑色头发男孩
                break
        for name in ["秦天"]:
            if name in storyboard:
                lora_prompt += lora.boy2.name + lora.boy2.prompt  # 棕色头发男孩
                break
        for name in []:
            if name in storyboard:
                lora_prompt = ""
                lora_prompt += lora.girl1.name + lora.girl1.prompt  # 校服风金发女孩
                break
        for name in []:
            if name in storyboard:
                lora_prompt = ""
                lora_prompt += lora.girl2.name + lora.girl2.prompt  # 粉色头发粉色运动衣女孩
                break
        for name in []:
            if name in storyboard:
                lora_prompt = ""
                lora_prompt += lora.girl3.name + lora.girl3.prompt  # 黑色头发风衣衣女孩
                break
        for name in ["鱼幼薇"]:
            if name in storyboard:
                lora_prompt = ""
                lora_prompt += lora.girl4.name + lora.girl4.prompt  # 白发白衣女孩
                break

        lora_prompts.append(lora_prompt)
        result = prompt_generator.generate(storyboard)
        if result is None:
            print("分镜信息生成失败，重新生成")
            for _ in range(3):
                result = prompt_generator.generate(storyboard)
                if result is not None:
                    break

        if result is not None:
            scenery = result.get("scenery", "").replace('"', ",")
            character = result.get("character", "").replace('"', ",")
            character_num = result.get("character_num", "").replace('"', ",")
            lens_angle = result.get("lens_angle", "").replace('"', ",")
            content = result.get("content", "A lot of people").replace('"', ",")

            sceneries.append(scenery)
            characters.append(character)
            character_nums.append(character_num)
            lens_angles.append(lens_angle)
            contents.append(content)
        else:
            raise ValueError("重复三次执行失败，已退出")

        with open(f"{config.work_dir}/storyboard_info.txt", "a", encoding="utf8") as f:
            f.write(
                f'"{storyboard}","{style}","{scenery}","{character}","{character_num}","{lens_angle}","{content}","{lora_prompt}"\n'
            )
    # 场景补齐
    for i in range(len(sceneries)):
        if i == 0 and sceneries[i] == "":
            sceneries[i] = "indoor"
        elif sceneries[i] == "":
            sceneries[i] = sceneries[i - 1]

    for i in range(len(lens_angles)):
        if i == 0 and lens_angles[i] == "":
            lens_angles[i] = "scenery close by"
        elif lens_angles[i] == "":
            lens_angles[i] = lens_angles[i - 1]

    def gen_prompt(row):
        if row["lora_prompt"] == "":
            prompt = f"{row['style']},{row['scenery']},{row['lens_angle']},{row['character_num']} {row['character']},{row['content']}"
        else:
            prompt = f"{row['style']},{row['scenery']},{row['lens_angle']},{row['lora_prompt']},{row['content']}"
        return prompt

    df = pd.DataFrame(
        {
            "storyboard": storyboards,
            "style": style,
            "scenery": sceneries,
            "character": characters,
            "character_num": character_nums,
            "lens_angle": lens_angles,
            "content": contents,
            "lora_prompt": lora_prompts,
        }
    )
    df["prompt"] = df.apply(gen_prompt, axis=1)
    df.to_csv(f"{config.work_dir}/data.csv", index=None)
    return df


def generate_audio(df):
    print("生成配音...")
    audio_generator = AudioGenerator(config)
    audio_paths = []
    for paragraph in tqdm(df["storyboard"].tolist()):
        for name in ["鱼幼薇", "秦天"]:
            paragraph = paragraph.replace(f"<{name}>", "")

        audio_paths.append(audio_generator.generate(paragraph))
    df["audio_path"] = audio_paths
    df.to_csv(f"{config.work_dir}/data.csv", index=None)
    return df


def generate_image(df):
    print("生成配图...")
    image_generator = ImageGenerator(config)
    image_paths = []
    for prompt in tqdm(df["prompt"].tolist()):
        image_path = image_generator.generate(prompt)
        if image_path is None:
            print("图片生成失败，重新生成")
            for _ in range(3):
                image_path = image_generator.generate(prompt)
                if image_path is not None:
                    break
        if image_path is not None:
            image_paths.append(image_path)
        else:
            raise ValueError("重复三次执行失败，已退出")
    df["image_path"] = image_paths
    df.to_csv(f"{config.work_dir}/data.csv", index=None)
    return df


def generate_video(df):
    video_generator = VideoGenerator(config)
    video_generator.generate_video(df["image_path"], df["audio_path"])


if __name__ == "__main__":
    novel_paths = [
        "novel/羡鱼之恋1.txt",
    ]
    for path in novel_paths:
        print("正在生成", path)
        config.work_dir = os.path.join(
            config.root_dir, path.split("/")[-1].split(".")[0]
        )
        os.makedirs(config.work_dir, exist_ok=True)

        # storyboards = novel_preprocess(path)
        # df = generate_storyboard_info(storyboards, style="")
        df = pd.read_csv(f"{config.work_dir}/data.csv")
        df = generate_image(df)
        # df = generate_audio(df)

        # generate_video(df)
