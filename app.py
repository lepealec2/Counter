import gradio as gr

# -----------------------
# LOGIC
# -----------------------

def change(state, delta):
    new = int(state) + int(delta)
    return new, str(new)


def reset_all(val):
    val = int(val)
    return [val] * len(states) + [str(val)] * len(displays)


def update_names(*names):
    return names


def update_colors(*args):
    return ""  # placeholder for your CSS system


# -----------------------
# UI
# -----------------------

with gr.Blocks() as demo:

    gr.Markdown("# 🎲 Counter Board")

    # -----------------------
    # GLOBAL RESET VALUE
    # -----------------------

    reset_value = gr.Number(
        value=20,
        precision=0,
        label="Reset Value (applies to all counters)"
    )

    reset_btn = gr.Button("Reset All Counters")

    # -----------------------
    # COUNTERS STORAGE
    # -----------------------

    states = []
    displays = []

    groups = []

    # -----------------------
    # COUNTERS (MUST COME BEFORE reset_btn.click)
    # -----------------------

    for i in range(8):

        state = gr.State(0)
        states.append(state)

        with gr.Group(visible=(i < 4), elem_id=f"group_{i}") as group:
            groups.append(group)

            display = gr.Textbox(
                value="0",
                interactive=False,
                label=f"Counter {i+1}",
                elem_id=f"counter_{i}"
            )
            displays.append(display)

            with gr.Row():
                btn_plus = gr.Button("+")
                btn_minus = gr.Button("-")

            btn_plus.click(
                change,
                inputs=[state, gr.State(1)],
                outputs=[state, display]
            )

            btn_minus.click(
                change,
                inputs=[state, gr.State(-1)],
                outputs=[state, display]
            )

    # -----------------------
    # RESET (NOW SAFE — ALL COMPONENTS EXIST)
    # -----------------------

    reset_btn.click(
        reset_all,
        inputs=[reset_value],
        outputs=states + displays
    )

    # -----------------------
    # OPTIONAL UI CONTROLS (PLACEHOLDERS)
    # -----------------------

    n_counters = gr.Number(
        value=4,
        precision=0,
        minimum=1,
        maximum=8,
        label="Number of Counters"
    )

    name_inputs = []
    name_groups = []
    color_inputs = []
    color_groups = []
    text_color_inputs = []
    text_color_groups = []

    COLORS = ["black","white","lightgray","red","lightcoral","lightpink",
              "green","lightgreen","palegreen","blue","lightblue","skyblue",
              "yellow","lightyellow","orange","purple","pink"]

    TEXT_COLORS = ["black", "white"]

    with gr.Row():
        for i in range(8):
            with gr.Group(visible=(i < 4), elem_id=f"text_group_{i}") as g:
                tc = gr.Dropdown(TEXT_COLORS, value="black", label=f"Text Color {i+1}")
                text_color_inputs.append(tc)
                text_color_groups.append(g)

    with gr.Row():
        for i in range(8):
            with gr.Group(visible=(i < 4)) as g:
                name = gr.Textbox(value=f"Counter {i+1}", label=f"Counter Name {i+1}")
                name_inputs.append(name)
                name_groups.append(g)

    with gr.Row():
        for i in range(8):
            with gr.Group(visible=(i < 4)) as g:
                color = gr.Dropdown(COLORS, value="white", label=f"Color {i+1}")
                color_inputs.append(color)
                color_groups.append(g)

    style_box = gr.HTML()

    # -----------------------
    # EVENTS
    # -----------------------

    for name in name_inputs:
        name.change(update_names, inputs=name_inputs, outputs=displays)

    for color in color_inputs + text_color_inputs:
        color.change(update_colors, inputs=color_inputs + text_color_inputs, outputs=style_box)

    def update(n):
        n = int(n)
        return (
            [gr.update(visible=(i < n)) for i in range(8)] +
            [gr.update(visible=(i < n)) for i in range(8)] +
            [gr.update(visible=(i < n)) for i in range(8)] +
            [gr.update(visible=(i < n)) for i in range(8)]
        )

    n_counters.change(
        update,
        inputs=n_counters,
        outputs=groups + name_groups + color_groups + text_color_groups
    )

import webbrowser
webbrowser.open("http://127.0.0.1:7860")

demo.launch(inbrowser=True)