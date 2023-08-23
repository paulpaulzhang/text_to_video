import os
from pathlib import Path
import time
import base64
import json
import io
from PIL import Image
import pandas as pd
import requests
from requests.exceptions import (
    RequestException,
    HTTPError,
    Timeout,
    ProxyError,
    SSLError,
)


class ImageGenerator:
    def __init__(self, config):
        self.config = config

        self.image_dir = os.path.join(self.config.work_dir, "image")
        os.makedirs(self.image_dir, exist_ok=True)

        self.count = 0

    def generate(self, prompt):
        try:
            for i in range(5):
                text2img_html = requests.post(
                    self.config.sd_text2img_api,
                    data=json.dumps(self._get_text2img_config(prompt)),
                )
                img_response = json.loads(text2img_html.text)
                image_base64 = img_response["images"][0]

                # outpainting_html = requests.post(
                #     self.config.sd_img2img_api,
                #     data=json.dumps(self._get_outpainting_config(image_base64)),
                # )
                # outpainting_img_response = json.loads(outpainting_html.text)
                # outpainting_image_base64 = outpainting_img_response["images"][0]

                upscale_html = requests.post(
                    self.config.sd_img2img_api,
                    data=json.dumps(self._get_upscale_config(image_base64)),
                )
                upscale_img_response = json.loads(upscale_html.text)
                upscale_image_base64 = upscale_img_response["images"][0]
                image_bytes = base64.b64decode(upscale_image_base64)
                image = Image.open(io.BytesIO(image_bytes))

                if i == 0:
                    image_path = f"{self.image_dir}/{self.count}.png"
                    image.save(image_path)
                else:
                    image.save(f"{self.image_dir}/{self.count}_{i}.png")
            self.count += 1
            return image_path
        except (
            RequestException,
            HTTPError,
            Timeout,
            ProxyError,
            SSLError,
            KeyError,
            json.decoder.JSONDecodeError,
        ) as e:
            return None

    def _get_text2img_config(self, prompt):
        return {
            "enable_hr": "false",
            "denoising_strength": 0.4,
            "firstphase_width": 0,
            "firstphase_height": 0,
            "hr_scale": 2,
            "hr_upscaler": "R-ESRGAN 4x+ Anime6B",
            "hr_second_pass_steps": 10,
            "hr_resize_x": 0,
            "hr_resize_y": 0,
            "prompt": self.config.sd_prompt + prompt,
            "styles": ["string"],
            "seed": -1,
            "subseed": -1,
            "subseed_strength": 0,
            "seed_resize_from_h": -1,
            "seed_resize_from_w": -1,
            "sampler_name": "DPM++ SDE Karras",
            "batch_size": 1,
            "n_iter": 1,
            "steps": self.config.steps,
            "cfg_scale": self.config.cfg_scale,
            "width": self.config.width,
            "height": self.config.height,
            "restore_faces": "false",
            "tiling": "false",
            "do_not_save_samples": "false",
            "do_not_save_grid": "false",
            "negative_prompt": self.config.sd_negative_prompt,
            "eta": 0,
            "s_churn": 0,
            "s_tmax": 0,
            "s_tmin": 0,
            "s_noise": 1,
            "override_settings": {
                "sd_model_checkpoint": "tmndMix_tmndMixVIPruned.safetensors",
                "sd_vae": "vae-ft-mse-840000-ema-pruned.ckpt",
                "CLIP_stop_at_last_layers": 2,
            },
            "override_settings_restore_afterwards": "true",
            "script_args": [],
            "sampler_index": "DPM++ SDE Karras",
            "script_name": "",
            "send_images": "true",
            "save_images": "true",
            "alwayson_scripts": {},
        }

    def _get_outpainting_config(self, image):
        return {
            "init_images": [image],
            "prompt": self.config.sd_prompt,
            "negative_prompt": self.config.sd_negative_prompt,
            "denoising_strength": 0.8,
            "width": self.config.width,
            "height": self.config.height,
            "cfg_scale": self.config.cfg_scale,
            "sampler_name": "DPM++ SDE Karras",
            "restore_faces": False,
            "steps": self.config.steps,
            "override_settings": {
                "sd_model_checkpoint": "tmndMix_tmndMixVIPruned.safetensors",
                "sd_vae": "vae-ft-mse-840000-ema-pruned.ckpt",
                "CLIP_stop_at_last_layers": 2,
            },
            "script_name": "outpainting mk2",
            "script_args": [None, 128, 16, "up,down", 1, 0.05],
        }

    def _get_upscale_config(self, image):
        return {
            "init_images": [image],
            "prompt": self.config.sd_prompt,
            "negative_prompt": self.config.sd_negative_prompt,
            "denoising_strength": 0.3,
            "width": self.config.width,
            "height": self.config.height,
            "cfg_scale": self.config.cfg_scale,
            "sampler_name": "DPM++ SDE Karras",
            "restore_faces": False,
            "steps": self.config.steps,
            "override_settings": {
                "sd_model_checkpoint": "tmndMix_tmndMixVIPruned.safetensors",
                "sd_vae": "vae-ft-mse-840000-ema-pruned.ckpt",
                "CLIP_stop_at_last_layers": 2,
            },
            "script_name": "ultimate sd upscale",
            "script_args": [
                None,  # _ (not used)
                self.config.width + 64,  # tile_width
                self.config.width + 64,  # tile_height
                16,  # mask_blur
                32,  # padding
                64,  # seams_fix_width
                0.35,  # seams_fix_denoise
                32,  # seams_fix_padding
                6,  # upscaler_index
                True,  # save_upscaled_image a.k.a Upscaled
                1,  # redraw_mode
                False,  # save_seams_fix_image a.k.a Seams fix
                8,  # seams_fix_mask_blur
                0,  # seams_fix_type
                2,  # target_size_type
                self.config.width * 2,  # custom_width
                self.config.height * 2,  # custom_height
                2,  # custom_scale
            ],
        }


if __name__ == "__main__":
    from config import Config

    config = Config()
    config.work_dir = "./"
    gen = ImageGenerator(config)
    gen.generate("1 girl and 1 boy in the playground, school playground background")
