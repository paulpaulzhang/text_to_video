import gradio as gr

# 创建一个初始的示例列表
initial_list = [["项1"], ["项2"], ["项3"]]
new_item_input = gr.Textbox(value="", label="新增项")


def add_item_to_list():
    new_item = new_item_input.value
    if new_item:
        initial_list.append([new_item])
        update_ui()


def update_ui():
    with gr.Blocks() as demo:
        with gr.Row():
            new_item_input
            add_btn = gr.Button(value="新增项", click=add_item_to_list)
        with gr.Row():
            with gr.Column():
                for item in initial_list:
                    gr.Textbox(item[0], show_label=False)


# 初始化界面
update_ui()

if __name__ == "__main__":
    demo.launch()
