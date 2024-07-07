import { emoji_labels, metaRelevantColor, metaRelevantId, edgeList, nodeList } from "./graph_data.js";
import { resetStorage } from "./util.js";

// create an array with nodes
var nodes = new vis.DataSet(nodeList);

// create an array with edges
var edges = new vis.DataSet(edgeList);

// create a network
var container = document.getElementById('visNetwork');

// provide the data in the vis format
var data = {
    nodes: nodes,
    edges: edges
};
var options = {
	nodes: {labelHighlightBold: false}
};

// initialize your network!
var network = new vis.Network(container, data, options);

// add loading screen while initializing
network.on("stabilizationProgress", function (params) {
	document.getElementById("loadingScreen").style.display = "block";
	document.getElementById("loadingScreenText").innerHTML = "🤫";
});
network.once("stabilizationIterationsDone", function () {
	document.getElementById("loadingScreen").style.display = "none";
	document.getElementById("loadingScreenText").innerHTML = "";
});

// load/initialize storage
if (localStorage.getItem("puzzleState")) {
	var puzzleState = JSON.parse(localStorage.getItem("puzzleState"));

	// load solved nodes
	for (var i = 0; i < puzzleState.solved.length; i++) {
		var nodeLabel = puzzleState.solved[i];
		var nodeId = emoji_labels.indexOf(nodeLabel);
		if (nodeId == metaRelevantId) { // re-shade the meta-relevant cell after update
			nodes.update({ id: nodeId, hidden: false, label: nodeLabel, color: { background: metaRelevantColor } });
		} else {
			nodes.update({ id: nodeId, hidden: false, label: nodeLabel });
		}
	}

	// load unlocked nodes
	for (var i = 0; i < puzzleState.unlocked.length; i++) {
		var nodeLabel = puzzleState.unlocked[i];
		var nodeId = emoji_labels.indexOf(nodeLabel);
		if (nodeId == metaRelevantId) { // re-shade the meta-relevant cell after update
			nodes.update({ id: nodeId, hidden: false, color: { background: metaRelevantColor } });
		} else {
			nodes.update({ id: nodeId, hidden: false });
		}
	}

	// load found special nodes
	for (var specialNodeId = emoji_labels.length; specialNodeId <= nodes.length; specialNodeId++) {
		var neighbors = network.getConnectedNodes(specialNodeId);
		for (var i = 0; i < neighbors.length; i++) {
			var neighborInfo = nodes.get(neighbors[i]);
			if (neighborInfo.label != '❓' && neighborInfo.group == 1) {
				nodes.update({ id: specialNodeId, hidden: false });
				break;
			}
		}
	}
} else {
	resetStorage();
}

export { nodes, network };