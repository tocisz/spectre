import sys
from xml.dom import minidom
from svgpathtools import parse_path

def dedup_vertices(vertices, tol=1e-6):
    """Remove consecutive duplicates (within tol)."""
    deduped = []
    for x, y in vertices:
        if not deduped or abs(x - deduped[-1][0]) > tol or abs(y - deduped[-1][1]) > tol:
            deduped.append((x, y))
    return deduped

def extract_absolute_vertices(svg_filename):
    doc = minidom.parse(svg_filename)
    paths = doc.getElementsByTagName("path")

    path_vertices = []

    total = len(paths)
    for idx, p in enumerate(paths, 1):
        d = p.getAttribute("d")
        if not d.strip():
            path_vertices.append([])  # keep index alignment
            continue

        path = parse_path(d)

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

        print(f"Processed {idx}/{total} paths")

    return doc, paths, path_vertices

def paths_are_similar(v1, v2, tol=0.1):
    v1 = dedup_vertices(v1)
    v2 = dedup_vertices(v2)

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

def write_filtered_svg(doc, paths, clusters, min_cluster_size, output_file):
    # Determine which paths to keep
    keep_indices = set()
    for cluster in clusters:
        if len(cluster) >= min_cluster_size:
            keep_indices.update(cluster)

    # Remove paths not in keep_indices
    for i, p in enumerate(paths):
        if i not in keep_indices:
            p.parentNode.removeChild(p)

    with open(output_file, "w", encoding="utf-8") as f:
        doc.writexml(f, encoding="utf-8")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python filter_svg_clusters.py input.svg output.svg")
        sys.exit(1)

    svg_file = sys.argv[1]
    out_file = sys.argv[2]

    doc, paths, vertices = extract_absolute_vertices(svg_file)
    clusters = cluster_paths(vertices)

    for idx, cluster in enumerate(clusters, 1):
        print(f"Cluster {idx}: {len(cluster)} members")

    write_filtered_svg(doc, paths, clusters, min_cluster_size=2, output_file=out_file)
    print(f"Filtered SVG saved to {out_file}")
