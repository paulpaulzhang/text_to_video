# -*- coding: utf-8 -*-
import os, requests, time
from xml.etree import ElementTree

import pandas as pd


class AudioGenerator(object):
    def __init__(self, config):
        self.config = config
        self.ms_key = self.config.ms_key
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = self.get_token()

        self.audio_dir = os.path.join(self.config.work_dir, "audio")
        os.makedirs(self.audio_dir, exist_ok=True)

        self.count = 0

    def get_token(self):
        fetch_token_url = (
            "https://southeastasia.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
        )
        headers = {"Ocp-Apim-Subscription-Key": self.ms_key}
        response = requests.post(fetch_token_url, headers=headers)
        return str(response.text)

    def save_audio(self, data, child_path):
        base_url = "https://southeastasia.tts.speech.microsoft.com/"
        path = "cognitiveservices/v1"
        constructed_url = base_url + path
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
            "User-Agent": "TTSForPython",
        }
        xml_body = ElementTree.Element("speak", version="1.0")
        xml_body.set("{http://www.w3.org/XML/1998/namespace}lang", "en-us")
        voice = ElementTree.SubElement(xml_body, "voice")
        voice.set("{http://www.w3.org/XML/1998/namespace}lang", "en-US")
        voice.set("name", "zh-CN-YunxiNeural")
        voice.set("rate ", "1.25")
        voice.text = data
        body = ElementTree.tostring(xml_body)
        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
            with open(child_path, "wb") as audio:
                audio.write(response.content)
                # print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
        else:
            print(
                "\nStatus code: "
                + str(response.status_code)
                + "\nSomething went wrong. Check your subscription key and headers.\n"
            )
            print("Reason: " + str(response.reason) + "\n")

    def get_voices_list(self):
        base_url = "https://southeastasia.tts.speech.microsoft.com/"
        path = "cognitiveservices/voices/list"
        constructed_url = base_url + path
        headers = {
            "Authorization": "Bearer " + self.access_token,
        }
        response = requests.get(constructed_url, headers=headers)
        if response.status_code == 200:
            print("\nAvailable voices: \n" + response.text)
        else:
            print(
                "\nStatus code: "
                + str(response.status_code)
                + "\nSomething went wrong. Check your subscription key and headers.\n"
            )

    def generate(self, text):
        audio_path = f"{self.audio_dir}/{self.count}.wav"
        self.save_audio(text, audio_path)
        self.count += 1
        return audio_path


if __name__ == "__main__":
    from config import Config

    config = Config()
    config.work_dir = "./"
    gen = AudioGenerator(config)
    gen.generate("重新回到18岁，我上辈子舔了三年的高中女神竟开始反舔，而我却选择安静的白月光，这一世绝对不做舔狗了！")
