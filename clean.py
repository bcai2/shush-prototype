import networkx as nx
import emoji

cluephrases = ["PUZZLEPART", "OPENEDLOCK", "MAGICSTICK"]
starting_node = "🤫"
meta_node = "👀"
frozen_category_node = "Livestock"
frozen_category_enum = "⑤●●●6️⃣●●●❿" # subject to change

def get_synonym_dict(node_list):
    D = {}
    with open("synonyms.txt", "r", encoding="utf8") as f:
        for line in f:
            synonym_line = [x for x in line.split("\t") if x != ""]
            if len(synonym_line) <= 1:
                continue
            main_node = None
            for c in line:
                if not c.isspace() and emoji.is_emoji(c):
                    if not main_node:
                        main_node = c
                        # check for variation selector
                        variant = c + '\ufe0f'
                        if variant in node_list:
                            main_node = variant
                    else:
                        D[c] = main_node
    # print(D)
    return D

def get_entries(filename):
    G = nx.Graph()

    last_cluephrase_entries = [{}, {}, {}]

    with open(filename, "r", encoding="utf8") as f:
        for line in f:
            # print(line)
            node = None

            edge_line = [x.lstrip().rstrip() for x in line.split("\t")]
            edge_line = [x for x in edge_line if x != ""]
            if len(edge_line) == 0:
                continue
            elif not emoji.is_emoji(edge_line[0]):
                enum_label = convert_names_to_enums(edge_line[0], edge_line[-3:], last_cluephrase_entries)
                if edge_line[0] == frozen_category_node:
                    frozen_category_enum = enum_label # TODO: fix bug here where this doesn't transfer to other functions
                edge_line = [enum_label] + edge_line[1:-3]
            
            for next_node in edge_line:
                if next_node == "":
                    continue
                if not node:
                    node = next_node
                    G.add_node(node)
                else:
                    G.add_node(next_node)
                    G.add_edge(node, next_node)
    return G

def get_degree_info(G):
    sorted_nodes = sorted(G.nodes, key=lambda node: G.degree[node])
    for node in sorted_nodes:
        print(node, G.degree[node])
    return G

def get_info(G):
    node_id = {}
    special_nodes = []
    edges = []
    counter = 1

    node_list_sorted = [x for x in G.nodes if emoji.is_emoji(x)] + [x for x in G.nodes if not emoji.is_emoji(x)]

    for node in node_list_sorted:
        node_id[node] = counter
        counter += 1
        if not emoji.is_emoji(node):
            special_nodes.append(node)
    
    # get printed emoji list and synonym object map
    synonym_map = get_synonym_dict(node_list_sorted)
    emoji_list = "[0,\"" + "\",\"".join(node_list_sorted[:-len(special_nodes)]) + "\"]"
    synonym_map_str = "{" + ",".join(f"\"{x}\": \"{synonym_map[x]}\"" for x in synonym_map) + "}"
    
    for edge in G.edges:
        u,v = edge
        edges.append(sorted((int(node_id[u]), int(node_id[v])), reverse=True))

    with open("graph_visjs_data.txt", "w", encoding="utf8") as f:
        # write all nodes
        f.write('const nodeList = [\n')
        for node in node_id:
            if node not in special_nodes:
                if node == meta_node: # meta node is slightly darker
                    f.write("\t{{ id: {0}, label: '{1}', group: 1, hidden: true, color: {{ background: '#4D96FA' }} }},\n".format(node_id[node], "❓"))
                    # f.write("\t{{ id: {0}, label: '{1}', group: 1 }},\n".format(node_id[node], node))
                elif node == starting_node: # starting node isn't hidden
                    f.write("\t{{ id: {0}, label: '{1}', group: 1 }},\n".format(node_id[node], "❓"))
                else:
                    f.write("\t{{ id: {0}, label: '{1}', group: 1, hidden: true }},\n".format(node_id[node], "❓"))
            else:
                if node == frozen_category_enum: # extraction node is fixed
                    f.write("\t{{ id: {0}, label: '{1}', group: 2, hidden: true, physics: false, fixed: true, x: 0, y: 0 }},\n".format(node_id[node], node))
                else:
                    f.write("\t{{ id: {0}, label: '{1}', group: 2, hidden: true }},\n".format(node_id[node], node))
        f.write('];\n\n') 

        # write all edges
        f.write('const edgeList = [\n')
        for edge in edges:
            f.write("\t{{ from: {0}, to: {1} }},\n".format(edge[0], edge[1]))
        f.write('];\n\n')

        # write map of all synonyms
        f.write('const synonyms = {0};\n\n'.format(synonym_map_str))
        
        # write list of all emojis by ID
        f.write('const emoji_labels = {0};\n\n'.format(emoji_list))

def run():
    edges_sheet = "edges_sheet.txt"
    G = get_entries(edges_sheet)
    get_info(G)

def convert_names_to_enums(label, index_chars, last_cluephrase_entries):
    index_sets = ["①②③④⑤⑥⑦⑧⑨⑩", "❶❷❸❹❺❻❼❽❾❿", [":one:",":two:",":three:",":four:",":five:",":six:",":seven:",":eight:",":nine:",":ten:"]]

    # get index of desired letters inside the spelled-out (special) labels
    index_set_indices = [label.upper().find(x) for x in index_chars]
    if label.upper() == "MYTHICAL CREATURES":
        index_set_indices = [label.upper().find(x, len("MYTHICAL")) for x in index_chars] # forces the code to draw from CREATURES letters
    
    enum_label_chars = []
    for i, ltr in enumerate(label.upper()):
        # print(i, ltr, index_set_indices)
        if i in index_set_indices:
            index_set = index_set_indices.index(i)
            last_used_cluephrase_letter = 0
            if ltr in last_cluephrase_entries[index_set]:
                last_used_cluephrase_letter = last_cluephrase_entries[index_set][ltr]
            # print(x, ltr, last_used_cluephrase_letter)
            cluephrase_index = cluephrases[index_set].index(ltr, last_used_cluephrase_letter)
            last_cluephrase_entries[index_set][ltr] = cluephrase_index + 1

            if index_set == 2:
                enum_label_chars.append(emoji.emojize(index_sets[index_set][cluephrase_index], language="alias"))
            else:
                enum_label_chars.append(index_sets[index_set][cluephrase_index])
        else:
            if ltr == " ":
                enum_label_chars.append("⎵")
            else:
                enum_label_chars.append("●")
    print(index_set_indices, index_chars, label, "".join(enum_label_chars))
    return "".join(enum_label_chars)
    


if __name__ == "__main__":
    run()
