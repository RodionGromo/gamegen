let engine;
let game;
let parts;

document.addEventListener("DOMContentLoaded", () => {
	gameCanvas.width = 800;
	gameCanvas.height = 600;
	engine = new Engine(gameCanvas);
})

async function sendPrompt() {
	setGameStatus('loading');
	promptInputPane.hidden = true;
	gameOutputPane.hidden = false;

	let res = await fetch("./api/generate", {
		method: "POST",
		headers: {
			"Content-Type": "application/json;charset=utf-8"
		},
		body: JSON.stringify({"game_prompt": promptInputField.value})
	});
	setGameStatus('ready');
	// let res = await fetch("./api/testCode")
	// пока оставляю для дебага, чтоб не генерировать игры снова и снова

	let data = await res.text();
	// делим на две части и запускаем раннер
	parts = data.split("```js");
	if(parts.length < 3) {
		// если нет заборчика, молимся что есть маркер второй части
		parts = data.split("// === ЧАСТЬ 2: ЦИКЛ ===");
	} else {
		parts.shift();
		for(let i = 0; i < parts.length; i++) {
			parts[i] = parts[i].replace("```", "");
		}
	}

	try {
		game = run_game(parts);
	} catch(e) {
		console.error(e);
		alert("ИИ ошибся при написании игры, попробуй еще раз!");
	}
}

function run_game(parts) {
	if(game) game.stop();
	const factory = new Function("engine", `
		"use strict";
		${parts[0]}
		// tick runner
		const __tick = () => {
			${parts[1]}
		}
		return setInterval(__tick, TICK_MS)
	`);
	const handle = factory(engine);
	return {
		stop() { clearInterval(handle); },
	}
}

function editPrompt() {
	if(game) game.stop();
	promptInputPane.hidden = false;
	gameOutputPane.hidden = true;
}
