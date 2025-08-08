from xml.dom import minidom
from svgpathtools import parse_path
import numpy as np
import math
import re

def parse_transform(transform_str):
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

def apply_matrix(pt, matrix):
    v = np.array([pt[0], pt[1], 1.0])
    res = matrix @ v
    return (res[0], res[1])

def expand_uses_recursive(node, doc):
    if node.nodeType != node.ELEMENT_NODE:
        return

    if node.tagName == "use":
        href = node.getAttribute("xlink:href") or node.getAttribute("href")
        ref_id = href[1:] if href.startswith("#") else href
        ref_el = doc.getElementById(ref_id)
        if not ref_el:
            return

        clone = ref_el.cloneNode(deep=True)
        transform_attr = node.getAttribute("transform")
        if transform_attr:
            old_t = clone.getAttribute("transform")
            new_t = (old_t + " " + transform_attr).strip() if old_t else transform_attr
            clone.setAttribute("transform", new_t)

        parent = node.parentNode
        parent.replaceChild(clone, node)
        expand_uses_recursive(clone, doc)
    else:
        for child in list(node.childNodes):
            expand_uses_recursive(child, doc)

def expand_uses(doc):
    expand_uses_recursive(doc.documentElement, doc)

def parse_style(style_str):
    style_dict = {}
    for item in style_str.split(";"):
        if ":" in item:
            k, v = item.split(":", 1)
            style_dict[k.strip().lower()] = v.strip().lower()
    return style_dict

def gather_paths(node, parent_transform=""):
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

def transform_points_to_segments(points, transform):
    matrix = parse_transform(transform)
    abs_points = [apply_matrix(pt, matrix) for pt in points]
    return [(abs_points[i], abs_points[i+1]) for i in range(len(abs_points)-1)]

doc = minidom.parse("jigsaw2.2.svg")
expand_uses(doc)
paths = gather_paths(doc.documentElement)

result = []
for points, transform in paths:
    result.append(transform_points_to_segments(points, transform))

for i, segs in enumerate(result):
    print(f"Polygon {i}:")
    for s in segs:
        print("  ", s)
