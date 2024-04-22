nodes = [1, 2, 3, 4, 5, 6]
edges = [(1,3),(2,3),(3,4),(4, 5), (4, 6)]

def dfs(nodes, edges, start_node, visited=None):
    if visited is None:
        visited = set()
    visited.add(start_node)

    for edge in edges:
        if start_node in edge:
            neighbor = edge[1] if edge[0] == start_node else edge[0]
            if neighbor not in visited:
                dfs(nodes, edges, neighbor, visited)

def count_components(nodes, edges):
    visited = set()
    components = 0
    for node in nodes:
        if node not in visited:
            dfs(nodes, edges, node, visited)
            components += 1
    return components

def find_articulation_points(nodes, edges):
    articulation_points = []
    initial_components = count_components(nodes, edges)

    for node in nodes:
        modified_nodes = [n for n in nodes if n != node]
        modified_edges = [edge for edge in edges if node not in edge]
        modified_components = count_components(modified_nodes, modified_edges)

        if modified_components > initial_components:
            articulation_points.append(node)

    return articulation_points

def main():
    print(f"{find_articulation_points(nodes, edges)}")

if __name__ == "__main__":
    main()