class Girl1:
    """校服风金发女孩 shokuhou_misaki_v2.safetensors"""

    def __init__(self):
        self.name = "<lora:shokuhou_misaki_v2:0.7>,"
        self.prompt = "hmmisaki,((1girl,solo)), long hair, symbol-shaped pupils, +_+, large breasts, tokiwadai school uniform, red bow, white shirt, collared shirt, blazer, white gloves, long sleeves, plaid skirt, white thighhighs,"
        self.preview = "./lora_preview/shokuhou_misaki.jpeg"


class Girl2:
    """粉色头发粉色运动衣女孩 gotou_hitori_v1.safetensors"""

    def __init__(self):
        self.name = "<lora:gotou_hitori_v1:0.7>,"
        self.prompt = "gotou1, gotou hitori, ((1girl,solo)), skirt, pink jacket, track jacket, bangs, hair between eyes, long sleeves, medium breasts,"
        self.preview = "./lora_preview/gotou_hitori.jpeg"


class Girl3:
    """黑色头发风衣衣女孩 AZKi_v10.safetensors"""

    def __init__(self):
        self.name = "<lora:AZKi_v10:0.7>,"
        self.prompt = "azki_(hololive), ((1girl,solo)), multicolored hair, pink hair, purple eyes, black hair, dress, hair between eyes, white dress, brown dress, brown jacket, jewelry, long sleeves, x hair ornament, bangs, bracelet, very long hair, streaked hair, hairclip, large breasts,"
        self.preview = "./lora_preview/AZKi.jpeg"


class Girl4:
    """白发白衣女孩 shirogane_kei_v10.safetensors"""

    def __init__(self):
        self.name = "<lora:shirogane_kei_v10:0.7>,"
        self.prompt = "kei1, ((1girl,solo)), blue eyes, long hair, white dress, short sleeves, ribbon, bangs, collarbone, grey hair, white skirt, hair ornament, black hairband, black pantyhose, neck ribbon, hair between eyes, medium breasts, sailor collar,"
        self.preview = "./lora_preview/shirogane_kei.jpeg"


class Boy1:
    """黑色头发男孩 aru_akise.safetensors"""

    def __init__(self):
        self.name = "<lora:aru_akise:0.78>,"
        self.prompt = "((1boy, solo)),aru_akise,jacket,1boy, black hair,"
        self.preview = "./lora_preview/aru_akise.jpeg"


class Boy2:
    """棕色头发男孩 mizuto_irido.safetensors"""

    def __init__(self):
        self.name = "<lora:mizuto_irido:0.62>,"
        self.prompt = "((1boy, solo)),mizuto_irido, brown eyes, brown hair, hair between eyes, jacket,"
        self.preview = "./lora_preview/mizuto_irido.jpeg"


class Lora:
    def __init__(self):
        self.girl1 = Girl1()
        self.girl2 = Girl2()
        self.girl3 = Girl3()
        self.girl4 = Girl4()

        self.boy1 = Boy1()
        self.boy2 = Boy2()
