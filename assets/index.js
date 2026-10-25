
document.addEventListener("load", () => {
	gameCanvas.height = canvas.width / 3
})

function sendPrompt() {
	promptInputPane.hidden = true;
	gameOutputPane.hidden = false;
}

function editPrompt() {
	promptInputPane.hidden = false;
	gameOutputPane.hidden = true;
}
