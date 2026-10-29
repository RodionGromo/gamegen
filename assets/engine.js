class Rect {
	constructor(x, y, w, h, color, tag) {
		this.pos = {"x": x, "y": y};
		this.size = {"w": w, "h": h};
		this.color = color;
		this.tag = tag;
	}

	isColliding(other) {
		if(other instanceof this.constructor) {
			if((this.pos.x < other.pos.x + other.size.w) && (other.pos.x < this.pos.x + this.size.w) 
				&& (this.pos.y < other.pos.y + other.size.h) && (other.pos.y < this.pos.y + this.size.h)) {
				return true;
			}
			return false;
		}
		return false;
	}

	// момент позора...
	get x() { return this.pos.x}
	set x(v) { this.pos.x = v}
	get y() { return this.pos.y}
	set y(v) { this.pos.y = v}

	get w() { return this.size.w}
	set w(v) { this.size.w = v}
	get h() { return this.size.h}
	set h(v) { this.size.h = v}
}

class Engine {
	constructor(canvas) {
		this.canvas = canvas;
		this.context = canvas.getContext("2d");
		this.height = canvas.height ?? 800;
		this.width = canvas.width ?? 600;
		this._pointer = {x: 0, y: 0, isDown: false}
		this._lastClick = null;

		const toWorld = (e) => {
			const r = canvas.getBoundingClientRect();
			return {
				x: (e.clientX - r.left) * (this.width  / r.width),
				y: (e.clientY - r.top)  * (this.height / r.height),
			};
	    };

	    canvas.addEventListener("pointerdown", (e) => {
			const p = toWorld(e);
			this._pointer.x = p.x;
			this._pointer.y = p.y;
			this._pointer.isDown = true;
			this._lastClick = { ...p };
			canvas.setPointerCapture(e.pointerId);
	    });

	    canvas.addEventListener("pointermove", (e) => {
	    	const p = toWorld(e);
	    	this._pointer.x = p.x;
	    	this._pointer.y = p.y;
	    });

	    const release = () => { this._pointer.isDown = false; };
	    canvas.addEventListener("pointerup",     release);
	    canvas.addEventListener("pointercancel", release);
	}

	getPointer() {
		return {x: this._pointer.x, y: this._pointer.y, isDown: this._pointer.isDown}
	}

	consumePointerClick() {
		const c = this._lastClick;
		this._lastClick = null;
		return c;
	}

	setColor(color) {
		this.context.fillStyle = color;
	}

	getColor() {
		return this.context.fillStyle;
	}

	fillBackground(color) {
		this.setColor(color)
		this.context.fillRect(0, 0, this.canvas.width, this.canvas.height)
	}

	renderRect(rect) {
		if(!rect) return;
		if(rect.color) {
			this.setColor(rect.color);
			this.context.fillRect(rect.pos.x, rect.pos.y, rect.size.w, rect.size.h);
		} else {
			this.context.strokeRect(rect.pos.x, rect.pos.y, rect.size.w, rect.size.h);
		}
	}

	renderText(text, x, y, color, size = 16, align = "left") {
		this.context.font = `${size}px serif`
		this.setColor(color)
		this.context.textAlign = align
		this.textBaseline = "top";
		this.context.fillText(text, x, y)
	}
}