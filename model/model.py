import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes = []
        self.edges = []
        self.idMap = {}

        self.bilancio = {}

        self.bestPath = []

    def getBestPath(self, v0, soglia, vFine):
        self.bestPath = []

        parziale = [v0]
        archi_visitati = []
        self._ricorsione(parziale, archi_visitati, soglia, vFine)

        return self.bestPath

    def _ricorsione(self, parziale, archi_visitati, soglia, vFine):
        if parziale[-1] == vFine:
            if len(parziale) > len(self.bestPath):
                self.bestPath = copy.deepcopy(parziale)
                return

        for n in self.graph[parziale[-1]]:
            peso = self.graph[parziale[-1]][n]['weight']
            bilancio = self.bilancio[n]
            b1 = self.bilancio[parziale[0]]
            if (self.graph[parziale[-1]][n]['weight'] >= soglia and self.bilancio[n] > self.bilancio[parziale[0]] and (parziale[-1], n) not in archi_visitati) or n == vFine:
                archi_visitati.append((parziale[-1], n))
                parziale.append(n)
                self._ricorsione(parziale, archi_visitati, soglia, vFine)
                parziale.pop()
                archi_visitati.pop()



    def buildGraph(self, n):
        self.graph.clear()
        self.nodes = DAO.getNodes(n)
        self.graph.add_nodes_from(self.nodes)
        for node in self.nodes:
            self.idMap[node.AlbumId] = node

        for n1 in range(len(self.nodes)-1):
            for n2 in range(n1+1, len(self.nodes)):
                delta = self.getDelta(self.nodes[n1], self.nodes[n2])
                if delta != 0:
                    if delta < 0:
                        self.graph.add_edge(self.nodes[n1], self.nodes[n2], weight=-delta)
                        self.edges.append((self.nodes[n1], self.nodes[n2], delta))
                    else:
                        self.graph.add_edge(self.nodes[n2], self.nodes[n1], weight=delta)
                        self.edges.append((self.nodes[n2], self.nodes[n1], -delta))

        self.getBilancio()

    def getDelta(self, n1, n2):
        return n1.nTrack - n2.nTrack

    def getGraphSize(self):
        return len(self.nodes), len(self.edges)

    def getBilancio(self):
        for n in self.nodes:
            peso_entranti = 0
            peso_uscenti = 0
            for i in self.graph.in_edges(n):
                peso_entranti += self.graph[i[0]][n]['weight']

            for j in self.graph.out_edges(n):
                peso_uscenti += self.graph[n][j[1]]['weight']

            self.bilancio[n] = peso_entranti - peso_uscenti

    def getSuccessori(self, v0):
        return self.graph[v0]

    def getAdia(self, v0):
        return self.bilancio[v0]
