from xml.dom import minidom
from svgpathtools import parse_path
import numpy as np
import math
import re

# This function recursively builds a dictionary of element IDs.
# This workaround is necessary because minidom.getElementById() does not
# work by default.
def build_id_map(node, id_map):
    """Recursively builds a map of element IDs."""
    if node.nodeType == node.ELEMENT_NODE and node.hasAttribute("id"):
        id_map[node.getAttribute("id")] = node
    for child in node.childNodes:
        build_id_map(child, id_map)

# This function parses an SVG transform string into a 3x3 matrix.
def parse_transform(transform_str):
    """Parses an SVG transform string into a 3x3 transformation matrix."""
    matrix = np.eye(3)
    if not transform_str:
        return matrix

    for cmd, params in re.findall(r"(\w+)\(([^\)]*)\)", transform_str):
        nums = list(map(float, re.findall(r"[-+]?[0-9]*\.?[0-9]+", params)))
        if cmd == "translate":
            tx, ty = (nums + [0])[:2]
            m = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
        elif cmd == "scale":
            sx, sy = (nums + [nums[0]])[:2]
            m = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
        elif cmd == "rotate":
            a = math.radians(nums[0])
            cos_a, sin_a = math.cos(a), math.sin(a)
            if len(nums) == 3:
                cx, cy = nums[1], nums[2]
                m = np.array([
                    [cos_a, -sin_a, cx - cos_a*cx + sin_a*cy],
                    [sin_a,  cos_a, cy - sin_a*cx - cos_a*cy],
                    [0, 0, 1]
                ])
            else:
                m = np.array([[cos_a, -sin_a, 0], [sin_a, cos_a, 0], [0, 0, 1]])
        elif cmd == "matrix":
            a, b, c, d, e, f = nums
            m = np.array([[a, c, e], [b, d, f], [0, 0, 1]])
        else:
            continue
        matrix = matrix @ m

    return matrix

# This function applies a transformation matrix to a point.
def apply_matrix(pt, matrix):
    """Applies a 3x3 matrix to a 2D point."""
    v = np.array([pt[0], pt[1], 1.0])
    res = matrix @ v
    return (res[0], res[1])

# This function recursively expands all <use> tags.
def expand_uses_recursive(node, doc, id_map):
    """Recursively expands <use> elements, replacing them with their cloned references."""
    if node.nodeType != node.ELEMENT_NODE:
        return

    if node.tagName == "use":
        href = node.getAttributeNS("http://www.w3.org/1999/xlink", "href") or node.getAttribute("href")
        ref_id = href[1:] if href.startswith("#") else href
        
        # Use our custom id_map to find the referenced element
        ref_el = id_map.get(ref_id)
        if not ref_el:
            print(f"Warning: Element with id '{ref_id}' not found. Skipping expansion.")
            return

        clone = ref_el.cloneNode(deep=True)
        transform_attr = node.getAttribute("transform")
        if transform_attr:
            old_t = clone.getAttribute("transform")
            new_t = (old_t + " " + transform_attr).strip() if old_t else transform_attr
            clone.setAttribute("transform", new_t)

        parent = node.parentNode
        parent.replaceChild(clone, node)
        expand_uses_recursive(clone, doc, id_map) # Recursively expand any new uses within the cloned content
    else:
        for child in list(node.childNodes):
            expand_uses_recursive(child, doc, id_map)

# Wrapper function to start the recursive expansion.
def expand_uses(doc, id_map):
    """Starts the recursive expansion process for all <use> tags."""
    expand_uses_recursive(doc.documentElement, doc, id_map)

# This function parses an SVG style string into a dictionary.
def parse_style(style_str):
    """Parses a CSS style string into a dictionary."""
    style_dict = {}
    for item in style_str.split(";"):
        if ":" in item:
            k, v = item.split(":", 1)
            style_dict[k.strip().lower()] = v.strip().lower()
    return style_dict

# This function gathers all paths and their combined transforms.
def gather_paths(node, parent_transform=""):
    """Recursively gathers all paths, polygons, and polylines with their combined transforms."""
    paths = []
    transform_attr = node.getAttribute("transform") if node.hasAttribute("transform") else ""
    combined_transform = (parent_transform + " " + transform_attr).strip()

    for child in node.childNodes:
        if child.nodeType != child.ELEMENT_NODE:
            continue
        if child.tagName in ("g", "svg"):
            paths.extend(gather_paths(child, combined_transform))
        elif child.tagName in ("path", "polygon", "polyline"):
            style = parse_style(child.getAttribute("style"))
            if style.get("stroke") == "#ff0000":
                if child.tagName == "path":
                    d = child.getAttribute("d")
                    path = parse_path(d)
                    points = [(seg.start.real, seg.start.imag) for seg in path]
                    points.append((path[-1].end.real, path[-1].end.imag))
                else:
                    pts = child.getAttribute("points").strip().split()
                    points = [tuple(map(float, pt.split(","))) for pt in pts]
                paths.append((points, combined_transform))
    return paths

# This function transforms points and converts them to segments.
def transform_points_to_segments(points, transform):
    """Transforms a list of points and returns them as a list of segments."""
    matrix = parse_transform(transform)
    abs_points = [apply_matrix(pt, matrix) for pt in points]
    return [(abs_points[i], abs_points[i+1]) for i in range(len(abs_points)-1)]

# -------------------- Main Script Execution --------------------

# 1. Parse the SVG file
doc = minidom.parse("jigsaw2.2.svg")

# 2. Build the ID map, which is crucial for finding elements by ID
id_map = {}
build_id_map(doc.documentElement, id_map)

# 3. Expand all <use> tags using the ID map
expand_uses(doc, id_map)

# 4. Gather all red-stroked paths from the expanded document
paths = gather_paths(doc.documentElement)

# 5. Transform the points of each path and print the results
result = []
for points, transform in paths:
    result.append(transform_points_to_segments(points, transform))

for i, segs in enumerate(result):
    print(f"Polygon {i}:")
    for s in segs:
        print("   ", s)

