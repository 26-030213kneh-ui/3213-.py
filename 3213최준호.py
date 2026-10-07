import math
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="알까기",
    page_icon="⚫",
    layout="centered",
)

st.title("⚫ 알까기")
st.caption("알을 마우스로 잡고 뒤로 당긴 다음 놓아보세요!")

GAME = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: transparent;
    font-family: Arial, sans-serif;
    user-select: none;
}

#game {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

#status {
    margin-bottom: 12px;
    font-size: 18px;
    font-weight: bold;
    color: #333;
}

#board {
    position: relative;
    width: min(90vw, 600px);
    aspect-ratio: 1 / 1;
    background:
        radial-gradient(circle at center, #d7a64d 0%, #c89439 100%);
    border: 14px solid #70451d;
    border-radius: 16px;
    box-shadow:
        inset 0 0 30px rgba(0,0,0,.25),
        0 5px 15px rgba(0,0,0,.3);
    overflow: hidden;
    touch-action: none;
}

.hole {
    position: absolute;
    width: 42px;
    height: 42px;
    background: #171717;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    box-shadow: inset 0 5px 8px rgba(0,0,0,.8);
}

.marble {
    position: absolute;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    z-index: 5;
    box-shadow:
        2px 4px 5px rgba(0,0,0,.45),
        inset 5px 5px 5px rgba(255,255,255,.35);
}

.black {
    background: radial-gradient(circle at 30% 25%, #555, #111 65%);
    border: 2px solid #050505;
}

.white {
    background: radial-gradient(circle at 30% 25%, white, #bbb 70%);
    border: 2px solid #777;
}

#aim {
    position: absolute;
    height: 5px;
    background: #e53935;
    transform-origin: left center;
    display: none;
    z-index: 10;
    border-radius: 5px;
}

#power {
    margin-top: 10px;
    color: #666;
    font-size: 13px;
}
</style>
</head>

<body>
<div id="game">
    <div id="status">⚫ 검은 알 차례</div>

    <div id="board">

        <div class="hole" style="left:0%;top:0%"></div>
        <div class="hole" style="left:50%;top:0%"></div>
        <div class="hole" style="left:100%;top:0%"></div>

        <div class="hole" style="left:0%;top:100%"></div>
        <div class="hole" style="left:50%;top:100%"></div>
        <div class="hole" style="left:100%;top:100%"></div>

        <div id="aim"></div>

        <div id="black" class="marble black"
             style="left:50%;top:75%"></div>

        <div id="white" class="marble white"
             style="left:50%;top:25%"></div>
    </div>

    <div id="power">
        알을 뒤로 당길수록 더 강하게 발사됩니다.
    </div>
</div>

<script>
const board = document.getElementById("board");
const status = document.getElementById("status");
const aim = document.getElementById("aim");

const balls = [
    {
        el: document.getElementById("black"),
        x: 0.5,
        y: 0.75,
        vx: 0,
        vy: 0,
        name: "검은"
    },
    {
        el: document.getElementById("white"),
        x: 0.5,
        y: 0.25,
        vx: 0,
        vy: 0,
        name: "흰"
    }
];

let turn = 0;
let dragging = false;
let moving = false;
let activeBall = null;

const holes = [
    [0, 0],
    [0.5, 0],
    [1, 0],
    [0, 1],
    [0.5, 1],
    [1, 1]
];

function pointerPosition(event) {
    const rect = board.getBoundingClientRect();

    return {
        x: (event.clientX - rect.left) / rect.width,
        y: (event.clientY - rect.top) / rect.height
    };
}

function distance(a, b) {
    return Math.sqrt(
        Math.pow(a.x - b.x, 2) +
        Math.pow(a.y - b.y, 2)
    );
}

function render() {
    for (const ball of balls) {
        if (!ball.el) continue;

        ball.el.style.left = (ball.x * 100) + "%";
        ball.el.style.top = (ball.y * 100) + "%";
    }
}

function updateStatus() {
    if (!moving) {
        const emoji = turn === 0 ? "⚫" : "⚪";
        status.textContent =
            emoji + " " + balls[turn].name + " 알 차례";
    }
}

board.addEventListener("pointerdown", function(event) {

    if (moving) return;

    const p = pointerPosition(event);
    const ball = balls[turn];

    if (!ball.el) return;

    const d = Math.sqrt(
        Math.pow(p.x - ball.x, 2) +
        Math.pow(p.y - ball.y, 2)
    );

    if (d > 0.09) return;

    dragging = true;
    activeBall = ball;

    board.setPointerCapture(event.pointerId);
});

board.addEventListener("pointermove", function(event) {

    if (!dragging || !activeBall) return;

    const p = pointerPosition(event);

    let dx = activeBall.x - p.x;
    let dy = activeBall.y - p.y;

    const length = Math.sqrt(dx * dx + dy * dy);

    if (length < 0.01) {
        aim.style.display = "none";
        return;
    }

    const maxPower = 0.45;
    const power = Math.min(length, maxPower);

    const angle = Math.atan2(dy, dx);

    aim.style.display = "block";
    aim.style.left = (activeBall.x * 100) + "%";
    aim.style.top = (activeBall.y * 100) + "%";
    aim.style.width =
        Math.min(power * board.clientWidth * 1.7, 180) + "px";

    aim.style.transform =
        "rotate(" + angle + "rad)";
});

board.addEventListener("pointerup", function(event) {

    if (!dragging || !activeBall) return;

    dragging = false;
    aim.style.display = "none";

    const p = pointerPosition(event);

    const dx = activeBall.x - p.x;
    const dy = activeBall.y - p.y;

    const length = Math.sqrt(dx * dx + dy * dy);

    if (length < 0.025) {
        activeBall = null;
        return;
    }

    const power = Math.min(length, 0.45);

    const speed = 5.5;

    activeBall.vx =
        (dx / length) * power * speed;

    activeBall.vy =
        (dy / length) * power * speed;

    moving = true;
    status.textContent = "💥 발사!";

    activeBall = null;

    startPhysics();
});

function checkHole(ball) {

    for (const hole of holes) {

        const d = Math.sqrt(
            Math.pow(ball.x - hole[0], 2) +
            Math.pow(ball.y - hole[1], 2)
        );

        if (d < 0.075) {

            if (ball.el) {
                ball.el.remove();
                ball.el = null;
            }

            ball.vx = 0;
            ball.vy = 0;

            return true;
        }
    }

    return false;
}

function wallCollision(ball) {

    const radius = 0.045;

    if (ball.x < radius) {
        ball.x = radius;
        ball.vx = Math.abs(ball.vx) * 0.75;
    }

    if (ball.x > 1 - radius) {
        ball.x = 1 - radius;
        ball.vx = -Math.abs(ball.vx) * 0.75;
    }

    if (ball.y < radius) {
        ball.y = radius;
        ball.vy = Math.abs(ball.vy) * 0.75;
    }

    if (ball.y > 1 - radius) {
        ball.y = 1 - radius;
        ball.vy = -Math.abs(ball.vy) * 0.75;
    }
}

function ballCollision() {

    const a = balls[0];
    const b = balls[1];

    if (!a.el || !b.el) return;

    const dx = b.x - a.x;
    const dy = b.y - a.y;

    const d = Math.sqrt(dx * dx + dy * dy);
    const minDistance = 0.08;

    if (d >= minDistance || d === 0) return;

    const nx = dx / d;
    const ny = dy / d;

    const relativeVelocity =
        (b.vx - a.vx) * nx +
        (b.vy - a.vy) * ny;

    if (relativeVelocity < 0) {

        const impulse = -relativeVelocity;

        a.vx -= impulse * nx;
        a.vy -= impulse * ny;

        b.vx += impulse * nx;
        b.vy += impulse * ny;
    }

    const overlap = minDistance - d;

    a.x -= nx * overlap / 2;
    a.y -= ny * overlap / 2;

    b.x += nx * overlap / 2;
    b.y += ny * overlap / 2;
}

function startPhysics() {

    let previous = performance.now();

    function frame(now) {

        const dt =
            Math.min((now - previous) / 1000, 0.03);

        previous = now;

        let anyMoving = false;

        for (const ball of balls) {

            if (!ball.el) continue;

            ball.x += ball.vx * dt;
            ball.y += ball.vy * dt;

            ball.vx *= Math.pow(0.025, dt);
            ball.vy *= Math.pow(0.025, dt);

            wallCollision(ball);

            checkHole(ball);

            const speed =
                Math.sqrt(
                    ball.vx * ball.vx +
                    ball.vy * ball.vy
                );

            if (speed > 0.03) {
                anyMoving = true;
            } else {
                ball.vx = 0;
                ball.vy = 0;
            }
        }

        ballCollision();

        render();

        if (anyMoving) {

            requestAnimationFrame(frame);

        } else {

            moving = false;

            // 현재 차례의 알이 홀에 들어가면 상대방 승리
            if (!balls[turn].el) {

                const winner =
                    turn === 0 ? "⚪ 흰 알" : "⚫ 검은 알";

                status.textContent =
                    "🎉 " + winner + " 승리!";

                return;
            }

            turn = 1 - turn;

            updateStatus();
        }
    }

    requestAnimationFrame(frame);
}

render();
updateStatus();
</script>

</body>
</html>
"""

components.html(GAME, height=700)

st.divider()

st.markdown(
    """
### 게임 방법

1. 자신의 알을 마우스로 누릅니다.
2. **알의 반대 방향으로 드래그**합니다.
3. 손을 놓으면 알이 발사됩니다.
4. 상대방 알을 구멍에 넣으면 승리합니다.

> 현재 버전은 2인용 기본 알까기입니다.
"""
)
