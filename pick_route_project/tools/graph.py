import heapq

 
class Graph:
    
    def __init__(self):
        self.vertices = {}
        
    def add_vertex(self, name, edge):
        if not self.vertices.get(list(edge)[0]):
                self.vertices[list(edge)[0]] = { name : list(edge.values())[0]}
        if self.vertices.get(name):
            self.vertices.get(name).update(edge)
        else:
            self.vertices[name] = edge
    
    def shortest_path(self, source, target):
        distances_from_source = {}
        previous_vertex = {} 
        nodes = []
 
        for vertex in self.vertices:
            if vertex == source:
                distances_from_source[vertex] = 0
                heapq.heappush(nodes, [0, vertex])
            else:
                distances_from_source[vertex] = float("inf")
                heapq.heappush(nodes, [float("inf"), vertex])
            previous_vertex[vertex] = None
        
        while nodes:
            smallest = heapq.heappop(nodes)[1]
            if smallest == target:
                path = []
                while previous_vertex[smallest]:
                    path.append(smallest)
                    smallest = previous_vertex[smallest]
                path.append(source)
                path.reverse()
                return path, distances_from_source[target]
            
            if distances_from_source[smallest] == float("inf"):
                break
            
            # relax
            for neighbor in self.vertices[smallest]:
                distance_beetween_smallest_neighbor = distances_from_source[smallest] + self.vertices[smallest][neighbor]
                if distance_beetween_smallest_neighbor < distances_from_source[neighbor]:
                    distances_from_source[neighbor] = distance_beetween_smallest_neighbor
                    previous_vertex[neighbor] = smallest
                    for node in nodes:
                        if node[1] == neighbor:
                            node[0] = distance_beetween_smallest_neighbor
                            break
                    heapq.heapify(nodes)
        return distances_from_source
        
    def __str__(self):
        return str(self.vertices)
        