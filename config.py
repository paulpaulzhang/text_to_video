import json


class Config:
    def __init__(self):
        self.root_dir = "./work"

        self.work_dir = None  # 自动生成，不需要设置

        # ChatGPT
        self._openai_key = self._polling_key()
        self.openai_key_list = "\n".join(
            [
                # 存放openai key 字符串列表
            ]
        )
        with open("chatgpt_prompt.json", "r", encoding="utf8") as f:
            self.llm_prompt = json.load(f)

        # Stable Diffusion
        self.sd_text2img_api = "http://172.28.118.203:7860/sdapi/v1/txt2img"
        self.sd_img2img_api = "http://172.28.118.203:7860/sdapi/v1/img2img"
        self.height = 768
        self.width = 768
        self.steps = 25
        self.cfg_scale = 7
        self.sd_prompt = "(best quality), ((masterpiece)), (highres), original, extremely detailed 8K wallpaper,(an extremely delicate and beautiful),hightlight,anime style,"
        self.sd_negative_prompt = "nsfw, bad crotch seam, fused anus, fused pussy,((abnormal eye proportion)),(Abnormal hands),( abnormal legs),(abnormal feet abnormal fingers),(sharp face),bad anatomy,bad hands,text,error,missing fingers,cropped,worst quality,normal quality,watermark,username,blurry,missing arms,long neck,Humpbacked,malformed ,limbs,mutilated,deformed,malformed,multiple breasts,missing fingers,poorly drawn,poorly drawn hands,extra legs,mutated hands and fingers,bad anatomy disfigured malformed mutated,worstquality,too many fingers,malformed hands,Missing limbs,long neck,blurry,missing arms,three arms,long body,more than 2 thighs,more than 2 nipples,missing legs,mutated hands and fingers ,low quality,jpeg artifacts,signature,extra digit,fewer digits,lowres,bad anatomy,extra limbs,"
        # Audio
        self.ms_key = ""  # 微软 api key

    def _polling_key(self):
        keys = self.openai_key_list.strip("\n").strip(" ").split("\n")
        index = 0
        while True:
            yield keys[index]
            index = (index + 1) % len(keys)

    def get_openai_key(self):
        return next(self._openai_key)
