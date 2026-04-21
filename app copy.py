import gradio as gr
import webbrowser

# -----------------------
# LOGIC
# -----------------------
def change(state, delta):
    if state == "X":
        state = 0
    return state + delta, state + delta


def update_names(*names):
    return [gr.update(label=names[i]) for i in range(8)]

def update_colors(*colors):
    css = ""
    for i, c in enumerate(colors):
        css += f"#counter_{i} textarea {{ background-color: {c}; }}\n"
    return f"<style>{css}</style>"

def update_colors(*colors_and_text):
    colors = colors_and_text[:8]
    text_colors = colors_and_text[8:]

    css = ""

    for i, (c, tc) in enumerate(zip(colors, text_colors)):
        css += f"""
        /* MAIN CARD (whole counter) */
        #group_{i} {{
            background-color: {c} !important;
            padding: 12px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            margin: 6px 0;
            color: {tc} !important;
        }}

        /* FORCE ALL INNER GRADIO WRAPPERS TO MATCH */
        #group_{i} * {{
            background-color: transparent !important;
            color: {tc} !important;
        }}

        /* TEXTBOX (remove white box) */
        #group_{i} textarea {{
            background-color: transparent !important;
            color: {tc} !important;
            border: none !important;
        }}

        /* BUTTON ROW CONTAINER */
        #group_{i} .gr-row {{
            background-color: transparent !important;
        }}

        /* BUTTONS */
        #group_{i} button {{
            background-color: rgba(255,255,255,0.15) !important;
            color: {tc} !important;
            border: 1px solid rgba(0,0,0,0.1);
        }}
        """
    return f"<style>{css}</style>"

def change(state, delta):
    state = int(state)
    new = state + delta
    return new, str(new)


def reset_all(val):
    val = int(val)
    return [val] * 8 + [str(val)] * 8

# -----------------------
# UI
# -----------------------
with gr.Blocks() as demo:
    gr.Markdown("# 🎲 Counter Board")
  # ✅ SINGLE global reset value

    # -----------------------
    # STORAGE
    # -----------------------

    states = []
    displays = []



    # -----------------------
    # RESET (ONE VALUE CONTROLS ALL)
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
    COLORS = ["black","white","lightgray","red","lightcoral","lightpink","green","lightgreen","palegreen","blue","lightblue","skyblue","yellow","lightyellow","orange","purple","pink"]
    color_inputs = []
    color_groups = []

    TEXT_COLORS = ["black", "white"]

    text_color_inputs = []
    text_color_groups = []

    with gr.Row():
        for i in range(8):
            with gr.Group(visible=(i < 4), elem_id=f"text_group_{i}") as g:
                tc = gr.Dropdown(
                    choices=TEXT_COLORS,
                    value="black",
                    label=f"Text Color {i+1}"
                )
                text_color_inputs.append(tc)
                text_color_groups.append(g)

    with gr.Row():
        for i in range(8):
            with gr.Group(visible=(i < 4)) as g:
                name = gr.Textbox(
                    value=f"Counter {i+1}",
                    label=f"Counter Name {i+1}"
                )
                name_inputs.append(name)
                name_groups.append(g)

    with gr.Row():
        
        for i in range(8):
            with gr.Group(visible=(i < 4)) as g:
                color = gr.Dropdown(
                    choices=COLORS,
                    value="white",
                    label=f"Color {i+1}"
                )
                color_inputs.append(color)
                color_groups.append(g)

    # -----------------------
    # COUNTERS
    # -----------------------
    groups = []

    for i in range(8):
        state = gr.State(0)
        states.append(state)

        with gr.Group(visible=(i < 4), elem_id=f"group_{i}") as group:
            groups.append(group)

            display = gr.Textbox(
                value="0",
                interactive=False,
                label=f"Counter {i+1}",
                elem_id=f"counter_{i}"   # required for color styling
            )
            displays.append(display)

            with gr.Row():
                btn_plus = gr.Button("+")
                btn_minus = gr.Button("-")

            btn_plus.click(change, inputs=[state, gr.State(1)], outputs=[state, display])
            btn_minus.click(change, inputs=[state, gr.State(-1)], outputs=[state, display])

    # -----------------------
    # STYLE BOX (for colors)
    # -----------------------
    style_box = gr.HTML()

    # -----------------------
    # EVENTS
    # -----------------------

    # update names
    for name in name_inputs:
        name.change(update_names, inputs=name_inputs, outputs=displays)

    # update colors
    for color in color_inputs:
        color.change(update_colors, inputs=color_inputs, outputs=style_box)

    for color in color_inputs + text_color_inputs:
        color.change(
            update_colors,
            inputs=color_inputs + text_color_inputs,
            outputs=style_box
        )
    # show/hide everything
    def update(n):
        n = int(n)
        return (
            [gr.update(visible=(i < n)) for i in range(8)] +  # counters
            [gr.update(visible=(i < n)) for i in range(8)] +  # names
            [gr.update(visible=(i < n)) for i in range(8)] +   # colors
            [gr.update(visible=(i < n)) for i in range(8)]
        )

    n_counters.change(
        update,
        inputs=n_counters,
        outputs=groups + name_groups + color_groups+text_color_groups
    )
    reset_value = gr.Number(
        value=20,
        precision=0,
        label="Reset Value (applies to all counters)"
    )

    reset_btn = gr.Button("Reset All Counters")
    reset_btn.click(
        reset_all,
        inputs=[reset_value],
        outputs=states + displays
    )

# -----------------------
# AUTO OPEN
# -----------------------
webbrowser.open("http://127.0.0.1:7860")

demo.launch(inbrowser=True)