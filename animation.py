import tkinter as tk

root = tk.Tk()
root.title("Bouncing Ball with Text Background & Pause")
canvas = tk.Canvas(root, width=600, height=400, bg="black")
canvas.pack()

ball_radius = 100  
x, y = 150, 150
dx, dy = 5, 4

ball = canvas.create_oval(x - ball_radius, y - ball_radius,
                          x + ball_radius, y + ball_radius,
                          fill="deep sky blue", outline="white", width=3)

text = "JERICK P. ABELLAR"
initial_font_size = 18
font_family = "Arial"
font_style = "bold"

def create_text_with_bg_stuck_to_edge(x, y, text, font_size):
    font = (font_family, font_size, font_style)
    temp_text = canvas.create_text(x, y, text=text, font=font)
    bbox = canvas.bbox(temp_text)
    canvas.delete(temp_text)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    max_width = ball_radius * 2 * 0.96  # 96% of diameter - very close to edge
    max_height = ball_radius * 2 * 0.28  # slightly smaller height

    scale_factor = min(1, max_width / text_width, max_height / text_height)
    adjusted_font_size = max(8, int(font_size * scale_factor))
    font = (font_family, adjusted_font_size, font_style)

    text_id = canvas.create_text(x, y, text=text, fill="black", font=font)
    bbox = canvas.bbox(text_id)

    # Calculate rectangle coords to "stick" sa loob ng bilog edges
    # We use max_width and max_height to limit rectangle size and position
    rect_left = x - max_width / 2
    rect_right = x + max_width / 2
    rect_top = y - max_height / 2
    rect_bottom = y + max_height / 2

    rect_bg = canvas.create_rectangle(
        rect_left, rect_top,
        rect_right, rect_bottom,
        fill="white", outline=""
    )

    canvas.tag_raise(text_id, rect_bg)

    return text_id, rect_bg

ball_text, rect_bg = create_text_with_bg_stuck_to_edge(x, y, text, initial_font_size)

paused = False

def update():
    global x, y, dx, dy
    if not paused:
        x += dx
        y += dy

        if x - ball_radius <= 0 or x + ball_radius >= 600:
            dx = -dx
        if y - ball_radius <= 0 or y + ball_radius >= 400:
            dy = -dy

        canvas.coords(ball, x - ball_radius, y - ball_radius,
                            x + ball_radius, y + ball_radius)

        current_x, current_y = canvas.coords(ball_text)
        offset_x = x - current_x
        offset_y = y - current_y

        canvas.move(ball_text, offset_x, offset_y)
        canvas.move(rect_bg, offset_x, offset_y)

    root.after(16, update)

def toggle_pause(event=None):
    global paused
    paused = not paused

root.bind("<space>", toggle_pause)

update()
root.mainloop()
