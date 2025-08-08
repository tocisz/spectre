import sys
from xml.dom import minidom
from svgpathtools import parse_path

def extract_absolute_vertices(svg_filename):
    # Parse SVG
    doc = minidom.parse(svg_filename)
    paths = doc.getElementsByTagName('path')

    for i, p in enumerate(paths):
        d = p.getAttribute('d')
        if not d.strip():
            continue

        path = parse_path(d)

        # Collect absolute vertices (start and end points of each segment)
        vertices = []
        for seg in path:
            # Add start point
            if not vertices or vertices[-1] != (seg.start.real, seg.start.imag):
                vertices.append((seg.start.real, seg.start.imag))
            # Add end point
            vertices.append((seg.end.real, seg.end.imag))

        print(f"Path {i+1} (id={p.getAttribute('id')}):")
        for x, y in vertices:
            print(f"  ({x:.6f}, {y:.6f})")
        print()

    doc.unlink()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_svg_vertices.py input.svg")
    else:
        extract_absolute_vertices(sys.argv[1])
