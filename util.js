import { synonyms, emoji_labels } from "./graph_data.js";
import { nodes } from "./initialize_graph.js";

// "one-character" ZWJ emojis that we want to accept as input
var validZWJ = ["👁️‍🗨️", "🏳️‍🌈", "🐈‍⬛", "🏳️‍⚧️", "🐻‍❄️", "😮‍💨", "😵‍💫", "❤️‍🩹", "❤️‍🔥", "😶‍🌫️"];

function parseInput(inputValue) {
    var parsedInput = inputValue;

    // TODO: convert ZWJ family emojis to the "family" emoji
    // TODO: handle all occupation ZWJ emojis

    // handle ZWJ emojis (skintones, gender, etc)
    // convert ZWJ emojis to first emoji character (before first ZWJ) if ZWJ found and not in ZWJ whitelist
    const emojiAsArray = [...`${parsedInput}`];
    const zwjIndex = emojiAsArray.indexOf('\u200d');
    console.log(emojiAsArray);
    if (zwjIndex >= 0 && validZWJ.indexOf(parsedInput) < 0) {
        console.log(`zwj detected at ${zwjIndex}`);
        parsedInput = emojiAsArray.slice(0, zwjIndex).join('');
    }

    // handle synonyms and variation selector variants
    var variationSelectorVariant = parsedInput;
    if (parsedInput.slice(-1) == '\ufe0f') {
        variationSelectorVariant = parsedInput.slice(0, -1);
    } else {
        variationSelectorVariant = parsedInput + '\ufe0f';
    }
    var variants = [parsedInput, variationSelectorVariant];
    for (var i = 0; i < variants.length; i++) {
        var variant = variants[i];
        // check if variant is already in labels
        if (emoji_labels.indexOf(variant) > -1) {
            parsedInput = variant;
            break;
        }
        // check variant in synonyms
        if (synonyms.hasOwnProperty(variant)) {
            console.log(`parsing ${inputValue} as ${synonyms[variant]}`)
            parsedInput = synonyms[variant];
            break;
        }
    }
    return parsedInput;
}

function resetStorage() {
    var puzzleState = {
        solved : [],
        unlocked : ["🤫"],
        solvePhraseStatus : 0,
        puzzleSolved : false,
    }
    console.log(puzzleState);
    console.log(JSON.stringify(puzzleState));
    localStorage.setItem("puzzleState", JSON.stringify(puzzleState));
}

function resetSolveVisuals() {
    const solvedNotif = document.getElementById('solved_notif');
    solvedNotif.innerHTML = '';
    const solveBoxIds = ['solve1', 'solve2', 'solve3'];
    for (var i = 0; i < 3; i++) {
        document.getElementById(solveBoxIds[i]).style.backgroundColor = "lightgray"; 
    }
}

function resetNetwork() {
    resetStorage();
    resetSolveVisuals();
    var nodeIds = nodes.getIds();
    var startingId = emoji_labels.indexOf("🤫");
    for (var i = 0; i < nodeIds.length; i++) {
        var nodeId = nodeIds[i];
        var nodeInfo = nodes.get(nodeId);
        if (nodeInfo.group == 2) {
            nodes.update({ id: nodeId, hidden: true });
        } else if (nodeId == startingId) {
            nodes.update({ id: nodeId, hidden: false, label: '❓' });
        } else {
            nodes.update({ id: nodeId, hidden: true, label: '❓' });
        }
    }
}

export { parseInput, resetStorage, resetNetwork };