import http.client
import json
import csv
import pandas as pd

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

    def add_node(self, id: str, name: str, group: str, avg_min: str) -> None:
        """
        add a tuple (id, name, group) representing a node to self.nodes if it does not already exist
        The graph should not contain any duplicate nodes
        """
        #TODO create a dictionary input parameter for multiple kwargs rather than avg_min
        #convert to string if not already
        id = str(id)
        group = str(group)
        avg_min = str(avg_min)

        # check for commas in name and replace
        #name = name.replace(",", "")

        # Check for duplicate nodes
        existing_nodes = [node for node in self.nodes if node[0] == id]
        if len(existing_nodes) > 0:
            #print("ID {} already contains a node. Node has been ignored.".format(id))
            return
        else:
            self.nodes.append((id, name, group, avg_min))
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
    def write_edges_file(self, path="output_data/edges.csv")->None:
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
    def write_nodes_file(self, path="output_data/nodes.csv")->None:
        """
        write all nodes out as .csv
        :param path: string
        :return: None
        """
        nodes_path = path
        nodes_file = open(nodes_path, 'w', encoding='utf-8')

        nodes_file.write("id,name,group,avg_min" + "\n")
        for n in self.nodes:
            nodes_file.write(str(n[0]) + "," + str(n[1]) + "," + str(n[2]) + "," + str(n[3]) + "\n")
        nodes_file.close()
        print("finished writing nodes to csv")

if __name__ == "__main__":

    csv_path = "../webapp/data/player_clusters_py.csv"
    df = pd.read_csv(csv_path)
    df = df.drop_duplicates()  # drop duplicate columns
    df = df.astype({"ID": int, "group": int, "id1": int, "id2": int, "id3": int})  # recast some columns as needed

    # initialize Graph object
    graph = Graph()

    # iterate through all players, adding each's 3 nodes and edges
    for index, row in df.iterrows():
        player = row['PLAYER_NAME']
        name_1 = df[df['ID'] == row['id1']]['PLAYER_NAME'].values[0]
        group_1 = df[df['ID'] == row['id1']]['group'].values[0]
        min_1 = df[df['ID'] == row['id1']]['MIN'].values[0]
        name_2 = df[df['ID'] == row['id2']]['PLAYER_NAME'].values[0]
        group_2 = df[df['ID'] == row['id3']]['group'].values[0]
        min_2 = df[df['ID'] == row['id2']]['MIN'].values[0]
        name_3 = df[df['ID'] == row['id3']]['PLAYER_NAME'].values[0]
        group_3 = df[df['ID'] == row['id3']]['group'].values[0]
        min_3 = df[df['ID'] == row['id3']]['MIN'].values[0]

        # add nodes
        graph.add_node(row['ID'], row['PLAYER_NAME'], row['group'], row['MIN'])  # add player himself
        graph.add_node(row['id1'], name_1, group_1, min_1)  # add player neighbor 1
        graph.add_node(row['id2'], name_2, group_2, min_2)  # add player neighbor 2
        graph.add_node(row['id3'], name_3, group_3, min_3)  # add player neighbor 3

        # add edges
        graph.add_edge(row['ID'], row['id1'])
        graph.add_edge(row['ID'], row['id2'])
        graph.add_edge(row['ID'], row['id3'])

        #todo: add player position info grab

    graph.write_nodes_file("output_data/nodes.csv")
    graph.write_edges_file("output_data/edges.csv")

    print('done')


