import http.client
import json
import csv


class Graph:

    # Do not modify
    def __init__(self, with_nodes_file=None, with_edges_file=None):
        """
        option 1:  init as an empty graph and add nodes
        option 2: init by specifying a path to nodes & edges files
        """
        self.nodes = []
        self.edges = []
        if with_nodes_file and with_edges_file:
            nodes_CSV = csv.reader(open(with_nodes_file))
            nodes_CSV = list(nodes_CSV)[1:]
            self.nodes = [(n[0], n[1]) for n in nodes_CSV]

            edges_CSV = csv.reader(open(with_edges_file))
            edges_CSV = list(edges_CSV)[1:]
            self.edges = [(e[0], e[1]) for e in edges_CSV]

    def add_node(self, id: str, name: str) -> None:
        """
        add a tuple (id, name) representing a node to self.nodes if it does not already exist
        The graph should not contain any duplicate nodes
        """
        #convert to string if not already
        id = str(id)

        # check for commas in name and replace
        name = name.replace(",", "")

        # Check for duplicate nodes
        existing_nodes = [node for node in self.nodes if node[0] == id]
        if len(existing_nodes) > 0:
            #print("ID {} already contains a node. Node has been ignored.".format(id))
            return
        else:
            self.nodes.append((id, name))
        return

    def add_edge(self, source: str, target: str) -> None:
        """
        Add an edge between two nodes if it does not already exist.
        An edge is represented by a tuple containing two strings: e.g.: ('source', 'target').
        Where 'source' is the id of the source node and 'target' is the id of the target node
        e.g., for two nodes with ids 'a' and 'b' respectively, add the tuple ('a', 'b') to self.edges
        """
        # convert to strings if not already
        source = str(source)
        target = str(target)

        if source == target:
            return

        # check if edge already exists (could be either a, b or b, a)
        for item in self.edges:
            if item[0] == source:
                if item[1] == target:
                    # edge exists, ignore addition
                    #print("Edge already exists. Ignoring edge.")
                    return
            elif item[1] == source:
                if item[0] == target:
                    #edge exists, ignore addition
                    #print("Edge already exists. Ignoring edge.")
                    return

        # if not a duplicate, add edge
        self.edges.append((source, target))
        return

    def total_nodes(self) -> int:
        """
        Returns an integer value for the total number of nodes in the graph
        """
        return len(self.nodes)

    def total_edges(self) -> int:
        """
        Returns an integer value for the total number of edges in the graph
        """
        return len(self.edges)

    def max_degree_nodes(self) -> dict:
        """
        Return the node(s) with the highest degree
        Return multiple nodes in the event of a tie
        Format is a dict where the key is the node_id and the value is an integer for the node degree
        e.g. {'a': 8}
        or {'a': 22, 'b': 22}
        """
        a = []
        for id in [node[0] for node in self.nodes]:
            occ = 0 # initialize counter
            for edge in self.edges:
                if edge[0] == id or edge[1] == id:
                    occ += 1
            a.append((id, occ))

        #out = dict(sorted(out.items(), key=lambda item: item[1]))
        a.sort(key=lambda x: x[1])
        highest_cnt = max(a, key=lambda item:item[1])[1]
        out = dict([tup for tup in a if tup[1] == highest_cnt])

        return out

    def count_nodes_w_deg_greater_than_1(self) -> dict:
        """
        Return the count of node(s) with degree > 1

        """
        a = []
        for id in [node[0] for node in self.nodes]:
            deg = 0 # initialize counter
            for edge in self.edges:
                if edge[0] == id or edge[1] == id:
                    deg += 1
            a.append((id, deg))

        #out = dict(sorted(out.items(), key=lambda item: item[1]))
        a.sort(key=lambda x: x[1])

        return [node for node in a if node[1]>1]

    def print_nodes(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.nodes)

    def print_edges(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.edges)

    # Do not modify
    def write_edges_file(self, path="edges.csv")->None:
        """
        write all edges out as .csv
        :param path: string
        :return: None
        """
        edges_path = path
        edges_file = open(edges_path, 'w', encoding='utf-8')

        edges_file.write("source" + "," + "target" + "\n")

        for e in self.edges:
            edges_file.write(e[0] + "," + e[1] + "\n")

        edges_file.close()
        print("finished writing edges to csv")

    # Do not modify
    def write_nodes_file(self, path="nodes.csv")->None:
        """
        write all nodes out as .csv
        :param path: string
        :return: None
        """
        nodes_path = path
        nodes_file = open(nodes_path, 'w', encoding='utf-8')

        nodes_file.write("id,name" + "\n")
        for n in self.nodes:
            nodes_file.write(n[0] + "," + n[1] + "\n")
        nodes_file.close()
        print("finished writing nodes to csv")
