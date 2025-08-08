from xml.dom import minidom

# This function recursively walks the SVG document tree
# and counts all <path> elements with a red stroke.
def count_red_paths(node):
    count = 0
    # Check if the node is an element and has the correct tag and style
    if node.nodeType == node.ELEMENT_NODE:
        if node.tagName == "path" and "stroke:#ff0000" in node.getAttribute("style"):
            count += 1
    
    # Recursively call the function for all child nodes
    for child in node.childNodes:
        count += count_red_paths(child)
    return count

# This function recursively builds a dictionary of element IDs.
# This workaround is necessary because minidom.getElementById() does not
# work by default without specific parser configurations.
def build_id_map(node, id_map):
    if node.nodeType == node.ELEMENT_NODE and node.hasAttribute("id"):
        id_map[node.getAttribute("id")] = node
    for child in node.childNodes:
        build_id_map(child, id_map)

# This function expands a single <use> element by replacing it
# with a clone of its referenced element.
def expand_use(doc, use, id_map):
    # Get the reference ID from either xlink:href or href
    href = use.getAttributeNS("http://www.w3.org/1999/xlink", "href") or use.getAttribute("href")
    if not href:
        return False
    ref_id = href[1:] if href.startswith("#") else href
    
    # Look up the referenced element using our custom id_map
    ref_el = id_map.get(ref_id)
    if not ref_el:
        print(f"Error: Element with id '{ref_id}' not found.")
        return False

    # Create a wrapper group to hold the cloned content
    wrapper = doc.createElement("g")

    # Clone the referenced element's content and append it to the wrapper
    clone = ref_el.cloneNode(deep=True)
    wrapper.appendChild(clone)

    # If the <use> element has a transform, apply it to the wrapper group
    if use.hasAttribute("transform"):
        wrapper.setAttribute("transform", use.getAttribute("transform"))

    # Replace the <use> element with the new wrapper group
    use.parentNode.replaceChild(wrapper, use)
    return True

# This function iterates and expands all <use> elements in the document
# until there are no more to expand.
def expand_all_uses(doc, id_map):
    while True:
        uses = doc.getElementsByTagName("use")
        if not uses:
            break
        changed = False
        # Create a list copy to iterate over, as the live collection changes
        for use in list(uses):
            if expand_use(doc, use, id_map):
                changed = True
        if not changed:
            break

# -------------------- Main Script Execution --------------------

# Parse the SVG file using the standard minidom.parse() function.
# This function does not automatically validate IDs, so getElementById() won't work.
svg = minidom.parse("jigsaw2.2.svg")

# Manually build the ID map to enable ID lookups
id_map = {}
build_id_map(svg.documentElement, id_map)

print("Initial red path count:", count_red_paths(svg.documentElement))
expand_all_uses(svg, id_map)
print("After expansion red path count:", count_red_paths(svg.documentElement))
