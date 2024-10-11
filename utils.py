from cairosvg import svg2png

def svg_to_png(svg_content, output_filename, width=None, height=None):
    svg2png(bytestring=svg_content, write_to=output_filename, output_width=width, output_height=height)

def save_svg(svg_content, output_filename):
    with open(output_filename, 'w') as f:
        f.write(svg_content)

def save_gcode(gcode_content, filename):
    with open(filename, 'w') as f:
        f.write(gcode_content)
    print(f"G-code saved to {filename}")
