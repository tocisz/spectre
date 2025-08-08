import sys
from xml.dom import minidom
from svgpathtools import parse_path

def extract_absolute_vertices(svg_filename):
    doc = minidom.parse(svg_filename)
    paths = doc.getElementsByTagName("path")

    path_vertices = []

    total = len(paths)
    for idx, p in enumerate(paths, 1):
        d = p.getAttribute("d")
        if not d.strip():
            continue

        path = parse_path(d)

        # collect absolute vertices
        vertices = []
        for seg in path:
            if not vertices or vertices[-1] != (seg.start.real, seg.start.imag):
                vertices.append((seg.start.real, seg.start.imag))
            vertices.append((seg.end.real, seg.end.imag))

        # Commented out transform for now
        # transform_str = p.getAttribute("transform")
        # mat = parse_transform(transform_str)
        # vertices = apply_transform(vertices, mat)

        path_vertices.append(vertices)

        # Progress indicator
        print(f"Processed {idx}/{total} paths")

    doc.unlink()
    return path_vertices

def paths_are_similar(v1, v2, tol=0.1):
    if len(v1) != len(v2):
        return False
    for (x1, y1), (x2, y2) in zip(v1, v2):
        if abs(x1 - x2) > tol or abs(y1 - y2) > tol:
            return False
    return True

def cluster_paths(paths):
    clusters = []
    assigned = [False] * len(paths)

    for i in range(len(paths)):
        if assigned[i]:
            continue
        cluster = [i]
        assigned[i] = True
        for j in range(i+1, len(paths)):
            if not assigned[j] and paths_are_similar(paths[i], paths[j]):
                cluster.append(j)
                assigned[j] = True
        clusters.append(cluster)
    return clusters

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cluster_svg_paths.py input.svg")
        sys.exit(1)

    svg_file = sys.argv[1]
    vertices = extract_absolute_vertices(svg_file)
    clusters = cluster_paths(vertices)

    for idx, cluster in enumerate(clusters, 1):
        print(f"Cluster {idx}: {len(cluster)} members")
