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
            path_vertices.append([])
            continue

        path = parse_path(d)

        vertices = []
        for seg in path:
            if not vertices or vertices[-1] != (seg.start.real, seg.start.imag):
                vertices.append((seg.start.real, seg.start.imag))
            vertices.append((seg.end.real, seg.end.imag))

        path_vertices.append(vertices)
        print(f"Processed {idx}/{total} paths")

    return doc, paths, path_vertices

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

def path_distance(v1, v2):
    if len(v1) != len(v2):
        return float("inf")
    return sum(abs(x1-x2) + abs(y1-y2) for (x1,y1),(x2,y2) in zip(v1,v2))

def find_representative(cluster, vertices):
    min_total_dist = float("inf")
    rep_idx = None
    for i in cluster:
        total = sum(path_distance(vertices[i], vertices[j]) for j in cluster if j != i)
        if total < min_total_dist:
            min_total_dist = total
            rep_idx = i
    return rep_idx

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cluster_representatives.py input.svg")
        sys.exit(1)

    svg_file = sys.argv[1]

    doc, paths, vertices = extract_absolute_vertices(svg_file)
    clusters = cluster_paths(vertices)

    big_clusters = [c for c in clusters if len(c) >= 2]

    print("\n=== Representatives of big clusters (size >= 2) ===\n")
    print('<svg xmlns="http://www.w3.org/2000/svg">')
    for cluster in big_clusters:
        rep = find_representative(cluster, vertices)
        path_el = paths[rep]
        print(f'  {path_el.toxml()}  <!-- cluster size {len(cluster)} -->')
    print("</svg>")
