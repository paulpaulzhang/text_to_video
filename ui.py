import gradio as gr
from PIL import Image
from presets import small_and_beautiful_theme
from config import Config
import pandas as pd

config = Config()


def change_root_dir(path):
    config.root_dir = path


def test(name):
    print(name.value)


df = pd.read_csv("./work/月下甜蜜1/data.csv")[:10]

with gr.Blocks(theme=small_and_beautiful_theme) as demo:
    with gr.Row():
        work_dir_tb = gr.Textbox(label="工作路径", value=config.root_dir, interactive=True)

    with gr.Accordion("小说文本", open=False):
        with gr.Column(variant="panel"):
            novel_name_tb = gr.Textbox(
                label="名称",
                value="",
                interactive=True,
            )
            novel_content_tb = gr.Textbox(
                label="内容", value="", lines=8, interactive=True
            )

    with gr.Accordion("ChatGPT", open=True):
        with gr.Row(variant="panel"):
            chatgpt_key_tb = gr.Textbox(
                label="ChatGPT KEY",
                value=config.openai_key_list,
                lines=3,
                placeholder="一行一个，多个key就会进行轮询，突破免费key每分钟3次的限制\n务必删除所有空行！",
                interactive=True,
            )

        with gr.Column(variant="panel"):
            llm_prompt_tb = gr.Textbox(
                label="提示语",
                value=config.llm_prompt,
                lines=10,
                placeholder="用于生成SD prompt 的提示语",
                interactive=True,
            )

    with gr.Accordion("Stable Diffusion", open=True):
        with gr.Row(variant="panel"):
            sd_api_tb = gr.Textbox(
                label="Stable Diffusion API服务",
                value=config.sd_text2img_api,
                interactive=True,
            )

        with gr.Column(variant="panel"):
            sd_prompt_tb = gr.Textbox(
                label="正向全局提示词",
                value=config.sd_prompt,
                lines=2,
                interactive=True,
            )
            sd_neg_prompt_tb = gr.Textbox(
                label="反向全局提示词",
                value=config.sd_negative_prompt,
                lines=2,
                interactive=True,
            )

        with gr.Row(variant="panel"):
            with gr.Column():
                width_slider = gr.Slider(
                    value=config.width,
                    minimum=64,
                    maximum=2048,
                    label="宽",
                    interactive=True,
                )
                height_slider = gr.Slider(
                    value=config.height,
                    minimum=64,
                    maximum=2048,
                    label="高",
                    interactive=True,
                )

            with gr.Column():
                cfg_slider = gr.Slider(
                    value=config.cfg_scale,
                    minimum=0,
                    maximum=100,
                    label="CFG",
                    interactive=True,
                )
                steps_slider = gr.Slider(
                    value=config.steps,
                    minimum=0,
                    maximum=100,
                    label="步数",
                    interactive=True,
                )

    with gr.Accordion("微软 TTS", open=True):
        with gr.Row(variant="panel"):
            ms_key_tb = gr.Textbox(
                label="微软API KEY",
                value=config.ms_key,
                lines=1,
                interactive=True,
            )

    with gr.Row():
        storyboard_btn = gr.Button(value="一键分镜")
        generate_video_btn = gr.Button(value="一键生成提示词")
        generate_image_btn = gr.Button(value="一键生成配图")
        generate_audio_btn = gr.Button(value="一键生成配音")
        composite_btn = gr.Button(value="视频合成")
        onekey_btn = gr.Button(value="一条龙", variant="primary")

    with gr.Accordion(f"生成结果", open=True) as result_part:
        for i, row in df.iterrows():
            with gr.Row(variant="panel"):
                with gr.Column(scale=3):
                    paragraph_tb = gr.Textbox(
                        value=row["paragraph"],
                        show_label=False,
                        interactive=True,
                        lines=2,
                    )
                    prompt_tb = gr.Textbox(
                        value=row["prompt"], show_label=False, interactive=True, lines=2
                    )
                    audio = gr.Audio(
                        value=row["audio_path"],
                        show_label=False,
                        interactive=False,
                    )
                    audio_path = gr.Textbox(row["audio_path"], visible=False)

                with gr.Column(min_width=256):
                    image = gr.Image(
                        value=row["image_path"],
                        interactive=False,
                        show_label=False,
                        width=256,
                        height=256,
                    )
                    image_path = gr.Textbox(row["image_path"], visible=False)
                with gr.Column(min_width=64):
                    regen_image_btn = gr.Button(value="🌃重新生成配图")
                    regen_audio_btn = gr.Button(value="🎙️重新生成配音")
                    regen_all_btn = gr.Button(value="🔄全部重新生成")
                    del_btn = gr.Button(value="🗑️删除分镜")
                    # regen_all_btn.click(fn=test, inputs=t6)

    def get_storyboard(novel):
        storyboards = novel.split("\n")
        children = result_part.children
        return gr.Row.update(children=children.append(gr.Audio()))

    def result_part_func(storyboards):
        with gr.Accordion(f"生成结果", open=True) as result_part:
            for storyboard in storyboards:
                with gr.Row(variant="panel"):
                    with gr.Column(scale=3):
                        t1 = gr.Textbox(
                            value=storyboards,
                            show_label=False,
                            interactive=True,
                            lines=2,
                        )
                        t4 = gr.Textbox(
                            value="", show_label=False, interactive=True, lines=2
                        )
                        t5 = gr.Audio(
                            # value="./work/月下甜蜜1/audio/0.wav",
                            show_label=False,
                            interactive=False,
                        )

                    with gr.Column(min_width=256):
                        t6 = gr.Image(
                            # value="./work/月下甜蜜1/image/0.png",
                            interactive=False,
                            show_label=False,
                            width=256,
                            height=256,
                        )
                    with gr.Column(min_width=64):
                        regen_image_btn = gr.Button(value="🌃重新生成配图")
                        regen_audio_btn = gr.Button(value="🎙️重新生成配音")
                        regen_all_btn = gr.Button(value="🔄全部重新生成")
                        del_btn = gr.Button(value="🗑️删除分镜")
                        # regen_all_btn.click(fn=test, inputs=t6)
        return result_part

    work_dir_tb.change(change_root_dir, [work_dir_tb])
    # storyboard_btn.click(
    #     fn=get_storyboard, inputs=[novel_content_tb], outputs=result_part
    # )


if __name__ == "__main__":
    demo.launch()
