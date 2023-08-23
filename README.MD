# 文本转动态漫画
该项目利用ChatGPT对小说进行改写并生成英文SD prompt，利用SD完成配图生成工作，最后通过tts合成语音，moviepy合成视频

执行命令
``` python
python main.py
```
main.py 主函数中的列表填写文本路径，main中会调用一下文件
generate_audio.py 生成音频
generate_image.py 生成图片
generate_prompt.py 生成prompt文本
generate_video.py 生成最终视频
lora.py 包含了lora的模型名称与prompt
config.py 为配置文件，openai key 与微软 key需要在这填写 
