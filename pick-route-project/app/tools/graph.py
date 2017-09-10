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
    
    def shortest_path(self, start, finish):
        distances = {}
        previous = {} 
        nodes = []
 
        for vertex in self.vertices:
            if vertex == start:
                distances[vertex] = 0
                heapq.heappush(nodes, [0, vertex])
            else:
                distances[vertex] = float("inf")
                heapq.heappush(nodes, [float("inf"), vertex])
            previous[vertex] = None
        
        while nodes:
            smallest = heapq.heappop(nodes)[1]
            if smallest == finish:
                path = []
                while previous[smallest]:
                    path.append(smallest)
                    smallest = previous[smallest]
                path.append(start)
                path.reverse()
                return path, distances[finish]
            
            if distances[smallest] == float("inf"):
                break
            
            for neighbor in self.vertices[smallest]:
                distance_beetween_smallest_neighbor = distances[smallest] + self.vertices[smallest][neighbor]
                if distance_beetween_smallest_neighbor < distances[neighbor]:
                    distances[neighbor] = distance_beetween_smallest_neighbor
                    previous[neighbor] = smallest
                    for node in nodes:
                        if node[1] == neighbor:
                            node[0] = distance_beetween_smallest_neighbor
                            break
                    heapq.heapify(nodes)
        return distances
        
    def __str__(self):
        return str(self.vertices)
        