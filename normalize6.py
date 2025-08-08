import sys
from xml.dom import minidom
from svgpathtools import parse_path

def extract_absolute_vertices(svg_filename):
    doc = minidom.parse(svg_filename)
    paths = doc.getElementsByTagName("path")

    path_vertices = []
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
        print(f"Processed {idx}/{len(paths)} paths")

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

def create_svg_with_defs(paths, clusters, representatives, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" ')
        f.write('xmlns:xlink="http://www.w3.org/1999/xlink">\n')

        # <defs> with representative paths
        f.write("  <defs>\n")
        for i, rep_idx in enumerate(representatives):
            path_el = paths[rep_idx].cloneNode(True)
            path_el.setAttribute("id", f"rep{i}")
            if path_el.hasAttribute("transform"):  # remove transform
                path_el.removeAttribute("transform")
            f.write(f"    {path_el.toxml()}\n")
        f.write("  </defs>\n\n")

        # Use each cluster member as <use>
        for cluster_idx, cluster in enumerate(clusters):
            for p_idx in cluster:
                transform = paths[p_idx].getAttribute("transform")
                f.write(f'  <use xlink:href="#rep{cluster_idx}"')
                if transform:
                    f.write(f' transform="{transform}"')
                f.write(" />\n")

        f.write("</svg>\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python svg_cluster_defs.py input.svg output.svg")
        sys.exit(1)

    svg_file = sys.argv[1]
    output_svg = sys.argv[2]

    doc, paths, vertices = extract_absolute_vertices(svg_file)
    clusters = cluster_paths(vertices)

    big_clusters = [c for c in clusters if len(c) >= 2]
    representatives = [find_representative(c, vertices) for c in big_clusters]

    create_svg_with_defs(paths, big_clusters, representatives, output_svg)
    print(f"SVG with defs written to {output_svg}")
