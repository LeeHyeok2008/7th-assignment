WIDTH = 800
HEIGHT = 600

WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
BLUE = (70, 130, 255)
LIGHT_GRAY = (211, 211, 211)
RED = (220, 80, 80)
SKY_BLUE = (178, 255, 255)
GOLD = (255, 210, 0)
GREEN = (80, 200, 120)
GRAY = (180, 180, 180)
PURPLE = (170, 90, 220)
YELLOW = (255, 255, 0)

FPS = 10
NUMBER_TO_ACTION = {
    0: (0, 0), 1: (0, -1), 2: (0, 1),
    3: (-1, 0), 4: (-1, -1), 5: (-1, 1),
    6: (1, 0), 7: (1, -1), 8: (1, 1),
}

GAME_JS = f"""
window.drawGame = function(canvasID, data) {{
    const canvas = document.getElementById(canvasID);
    if (!canvas || !data) return;

    const ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    if (data.target) {{

        const targetW = 80;
        const targetH = 50;

        ctx.save();

        ctx.translate(data.target.x, data.target.y);
        ctx.rotate(data.target.angle);

        ctx.translate(-targetW / 2, -targetH / 2);

        ctx.strokeStyle = "rgb{GREEN}";
        ctx.lineWidth = 2;

        ctx.strokeRect(0, 0, targetW, targetH);

        ctx.save();

        ctx.translate(targetW / 2, targetH / 2);
        ctx.rotate(Math.PI / 2);

        ctx.fillStyle = "rgb{GREEN}";
        ctx.font = "bold 24px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";

        ctx.fillText("P", 0, 0);

        ctx.restore();
        
        ctx.restore();
    }}
    
    if (data.player) {{
        const carW = 80;
        const carH = 40;

        ctx.save();

        ctx.translate(data.player.x, data.player.y);
        ctx.rotate(data.player.angle);

        ctx.translate(-carW / 2, -carH / 2);
    
        ctx.fillStyle = "rgb{BLACK}";
        ctx.fillRect(10, 0, 15, 8);
        ctx.fillRect(10, 32, 15, 8);
        ctx.fillRect(55, 0, 15, 8);
        ctx.fillRect(55, 32, 15, 8);


        ctx.fillStyle = "rgb{BLUE}";
        ctx.fillRect(5, 5, 70, 30);
        ctx.fill();

        ctx.fillStyle = "rgb{SKY_BLUE}";
        ctx.fillRect(45, 8, 15, 24);

        ctx.fillStyle = "rgb{YELLOW}";
        ctx.fillRect(72, 7, 5, 8);
        ctx.fillRect(72, 25, 5, 8);
    
        ctx.restore();
    }}

}};
"""

MANUAL_HTML = f"""
<canvas
    id="manualCanvas"
    width="{WIDTH}"
    height="{HEIGHT}"
    style="
        background:white;
        border:1px solid black;
        display:block;
        margin:auto;
    "
></canvas>
"""

AI_HTML = f"""
<canvas
    id="aiCanvas"
    width="{WIDTH}"
    height="{HEIGHT}"
    style="
        background:white;
        border:1px solid black;
        display:block;
        margin:auto;
    "
></canvas>
"""

REINFORCEMENT_HTML = f"""
<canvas
    id="reinforcementCanvas"
    width="{WIDTH}"
    height="{HEIGHT}"
    style="
        background:white;
        border:1px solid black;
        display:block;
        margin:auto;
    "
></canvas>
"""