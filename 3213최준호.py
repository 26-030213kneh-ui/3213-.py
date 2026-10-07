import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="알까기",
    page_icon="⚫",
    layout="centered",
)

st.title("⚫ 알까기")

game_html = r"""
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
    font-family: Arial, sans-serif;
    background: transparent;
    color: #222;
    user-select: none;
}

#app {
    width: 100%;
    max-width: 760px;
    margin: auto;
}

#menu {
    background: #f7f7f7;
    border-radius: 14px;
    padding: 15px;
    margin-bottom: 15px;
    border: 1px solid #ddd;
}

.menu-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
    margin-bottom: 10px;
}

.menu-row:last-child {
    margin-bottom: 0;
}

label {
    font-weight: bold;
}

select,
button {
    min-height: 42px;
    border-radius: 9px;
    border: 1px solid #bbb;
    padding: 8px 13px;
    font-size: 15px;
}

button {
    cursor: pointer;
    background: white;
}

button:hover {
    background: #eee;
}

#newGame {
    background: #222;
    color: white;
    border-color: #222;
}

#status {
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
}

#score {
    text-align: center;
    color: #666;
    font-size: 14px;
    margin-bottom: 10px;
}

#board {
    position: relative;
    width: min(92vw, 650px);
    aspect-ratio: 1 / 1;
    margin: auto;

    background:
        radial-gradient(
            circle at 50% 45%,
            #e1b35b 0%,
            #c9943b 100%
        );

    border: 15px solid #67401d;
    border-radius: 18px;

    box-shadow:
        inset 0 0 35px rgba(0,0,0,.25),
        0 8px 18px rgba(0,0,0,.25);

    overflow: hidden;
    touch-action: none;
}

.hole {
    position: absolute;
    width: 48px;
    height: 48px;

    background:
        radial-gradient(
            circle,
            #050505 0%,
            #171717 65%,
            #333 100%
        );

    border-radius: 50%;
    transform: translate(-50%, -50%);

    box-shadow:
        inset 0 5px 10px rgba(0,0,0,.9),
        0 2px 3px rgba(255,255,255,.15);
}

.marble {
    position: absolute;

    width: 34px;
    height: 34px;

    border-radius: 50%;

    transform:
        translate(-50%, -50%);

    z-index: 5;

    box-shadow:
        2px 4px 6px rgba(0,0,0,.5),
        inset 5px 5px 6px rgba(255,255,255,.35);

    pointer-events: none;
}

.black {
    background:
        radial-gradient(
            circle at 30% 25%,
            #666,
            #222 55%,
            #050505 100%
        );

    border: 2px solid #000;
}

.white {
    background:
        radial-gradient(
            circle at 30% 25%,
            #fff,
            #ddd 55%,
            #999 100%
        );

    border: 2px solid #777;
}

#aim {
    position: absolute;

    height: 5px;

    background:
        linear-gradient(
            90deg,
            #e53935,
            #ff8a80
        );

    border-radius: 10px;

    transform-origin: left center;

    display: none;

    z-index: 20;
}

#pauseOverlay {
    position: absolute;

    inset: 0;

    background: rgba(0,0,0,.72);

    display: none;

    align-items: center;
    justify-content: center;

    z-index: 100;
}

#pauseBox {
    width: min(85%, 350px);

    background: white;

    border-radius: 18px;

    padding: 25px;

    text-align: center;

    box-shadow: 0 10px 30px rgba(0,0,0,.4);
}

#pauseBox h2 {
    margin-top: 0;
}

.pause-buttons {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.pause-buttons button {
    width: 100%;
}

#hint {
    text-align: center;
    color: #666;
    font-size: 13px;
    margin-top: 12px;
}

@media (max-width: 500px) {

    #menu {
        padding: 10px;
    }

    .menu-row {
        flex-direction: column;
        align-items: stretch;
    }

    select,
    button {
        width: 100%;
    }

    .hole {
        width: 38px;
        height: 38px;
    }

    .marble {
        width: 29px;
        height: 29px;
    }
}
</style>
</head>

<body>

<div id="app">

    <div id="menu">

        <div class="menu-row">

            <label for="mode">
                게임 방식
            </label>

            <select id="mode">
                <option value="ai">🤖 AI와 대전</option>
                <option value="pvp">👥 2인 대전</option>
            </select>

        </div>

        <div class="menu-row">

            <label for="ballCount">
                알 개수
            </label>

            <select id="ballCount">
                <option value="1">1개</option>
                <option value="2">2개</option>
                <option value="3" selected>3개</option>
                <option value="4">4개</option>
                <option value="5">5개</option>
                <option value="6">6개</option>
                <option value="7">7개</option>
                <option value="8">8개</option>
            </select>

        </div>

        <div
            class="menu-row"
            id="difficultyRow"
        >

            <label for="difficulty">
                AI 난이도
            </label>

            <select id="difficulty">

                <option value="easy">
                    쉬움
                </option>

                <option value="normal" selected>
                    보통
                </option>

                <option value="hard">
                    어려움
                </option>

            </select>

        </div>

        <div class="menu-row">

            <button id="newGame">
                🔄 새 게임
            </button>

            <button id="pauseButton">
                ⏸ 일시정지
            </button>

        </div>

    </div>

    <div id="status">
        ⚫ 플레이어 1 차례
    </div>

    <div id="score">
        검은 알 3개 · 흰 알 3개
    </div>

    <div id="board">

        <div
            class="hole"
            style="left:0%;top:0%"
        ></div>

        <div
            class="hole"
            style="left:50%;top:0%"
        ></div>

        <div
            class="hole"
            style="left:100%;top:0%"
        ></div>

        <div
            class="hole"
            style="left:0%;top:100%"
        ></div>

        <div
            class="hole"
            style="left:50%;top:100%"
        ></div>

        <div
            class="hole"
            style="left:100%;top:100%"
        ></div>

        <div id="aim"></div>

        <div id="pauseOverlay">

            <div id="pauseBox">

                <h2>⏸ 게임 일시정지</h2>

                <p>
                    ESC를 누르거나 버튼을 눌러 계속할 수 있습니다.
                </p>

                <div class="pause-buttons">

                    <button id="resume">
                        ▶ 계속하기
                    </button>

                    <button id="restart">
                        🔄 새 게임
                    </button>

                </div>

            </div>

        </div>

    </div>

    <div id="hint">
        알을 뒤쪽으로 당긴 후 놓으면 발사됩니다.
        ESC를 누르면 일시정지합니다.
    </div>

</div>


<script>

const board =
    document.getElementById("board");

const status =
    document.getElementById("status");

const score =
    document.getElementById("score");

const aim =
    document.getElementById("aim");

const modeSelect =
    document.getElementById("mode");

const countSelect =
    document.getElementById("ballCount");

const difficultySelect =
    document.getElementById("difficulty");

const difficultyRow =
    document.getElementById("difficultyRow");

const newGameButton =
    document.getElementById("newGame");

const pauseButton =
    document.getElementById("pauseButton");

const pauseOverlay =
    document.getElementById("pauseOverlay");

const resumeButton =
    document.getElementById("resume");

const restartButton =
    document.getElementById("restart");


let balls = [];

let turn = 0;

let dragging = false;

let activeBall = null;

let moving = false;

let paused = false;

let gameOver = false;

let animationId = null;

let lastTime = 0;


/*
    구멍 위치
*/

const holes = [

    [0, 0],

    [.5, 0],

    [1, 0],

    [0, 1],

    [.5, 1],

    [1, 1]

];


/*
    마우스 위치를
    게임판 좌표 0~1로 변환
*/

function pointerPosition(event) {

    const rect =
        board.getBoundingClientRect();

    return {

        x:
            (event.clientX - rect.left)
            / rect.width,

        y:
            (event.clientY - rect.top)
            / rect.height

    };
}


/*
    두 점 거리
*/

function distance(x1, y1, x2, y2) {

    return Math.sqrt(

        Math.pow(x1 - x2, 2) +
        Math.pow(y1 - y2, 2)

    );
}


/*
    현재 설정에 맞게
    게임 생성
*/

function createGame() {

    cancelAnimationFrame(animationId);

    balls = [];

    turn = 0;

    moving = false;

    paused = false;

    gameOver = false;

    activeBall = null;

    dragging = false;

    aim.style.display = "none";

    pauseOverlay.style.display = "none";

    const count =
        Number(countSelect.value);

    /*
        위쪽:
        플레이어 2 / AI

        아래쪽:
        플레이어 1
    */

    for (let i = 0; i < count; i++) {

        const spacing =
            count === 1
                ? 0
                : (i - (count - 1) / 2)
                    * Math.min(
                        0.07,
                        0.42 / count
                    );

        balls.push({

            id: i,

            player: 0,

            x: 0.5 + spacing,

            y: 0.78,

            vx: 0,

            vy: 0,

            el: null,

            alive: true

        });

        balls.push({

            id: i,

            player: 1,

            x: 0.5 + spacing,

            y: 0.22,

            vx: 0,

            vy: 0,

            el: null,

            alive: true

        });

    }

    renderBalls();

    updateScore();

    updateStatus();

}


/*
    알 HTML 생성
*/

function createBallElement(ball) {

    const element =
        document.createElement("div");

    element.className =
        "marble " +
        (ball.player === 0
            ? "black"
            : "white");

    board.appendChild(element);

    ball.el = element;

}


/*
    모든 알 표시
*/

function renderBalls() {

    for (const ball of balls) {

        if (!ball.alive) continue;

        if (!ball.el) {

            createBallElement(ball);

        }

        ball.el.style.left =
            (ball.x * 100) + "%";

        ball.el.style.top =
            (ball.y * 100) + "%";

    }

}


/*
    점수 표시
*/

function updateScore() {

    const black =
        balls.filter(
            b => b.player === 0 && b.alive
        ).length;

    const white =
        balls.filter(
            b => b.player === 1 && b.alive
        ).length;

    score.textContent =
        "⚫ 검은 알 " +
        black +
        "개 · ⚪ 흰 알 " +
        white +
        "개";

}


/*
    현재 턴 표시
*/

function updateStatus() {

    if (gameOver) return;

    if (turn === 0) {

        status.textContent =
            "⚫ 플레이어 1 차례";

    } else {

        if (modeSelect.value === "ai") {

            status.textContent =
                "🤖 AI 차례";

        } else {

            status.textContent =
                "⚪ 플레이어 2 차례";

        }

    }

}


/*
    플레이어가 움직일 수 있는지
*/

function canHumanPlay() {

    if (gameOver) return false;

    if (paused) return false;

    if (moving) return false;

    if (turn === 1 &&
        modeSelect.value === "ai") {

        return false;

    }

    return true;

}


/*
    게임판 클릭
*/

board.addEventListener(
    "pointerdown",
    function(event) {

        if (!canHumanPlay()) return;

        const p =
            pointerPosition(event);

        const candidates =
            balls.filter(
                b =>
                    b.alive &&
                    b.player === turn
            );

        let closest = null;

        let closestDistance = Infinity;

        for (const ball of candidates) {

            const d =
                distance(
                    p.x,
                    p.y,
                    ball.x,
                    ball.y
                );

            if (
                d < 0.085 &&
                d < closestDistance
            ) {

                closest = ball;

                closestDistance = d;

            }

        }

        if (!closest) return;

        activeBall = closest;

        dragging = true;

        board.setPointerCapture(
            event.pointerId
        );

    }
);


/*
    조준선
*/

board.addEventListener(
    "pointermove",
    function(event) {

        if (
            !dragging ||
            !activeBall ||
            paused
        ) return;

        const p =
            pointerPosition(event);

        const dx =
            activeBall.x - p.x;

        const dy =
            activeBall.y - p.y;

        const length =
            Math.sqrt(
                dx * dx +
                dy * dy
            );

        if (length < 0.01) {

            aim.style.display = "none";

            return;

        }

        const angle =
            Math.atan2(dy, dx);

        const visualLength =
            Math.min(
                length *
                board.clientWidth *
                1.6,
                220
            );

        aim.style.display = "block";

        aim.style.left =
            (activeBall.x * 100) + "%";

        aim.style.top =
            (activeBall.y * 100) + "%";

        aim.style.width =
            visualLength + "px";

        aim.style.transform =
            "rotate(" +
            angle +
            "rad)";

    }
);


/*
    발사
*/

board.addEventListener(
    "pointerup",
    function(event) {

        if (
            !dragging ||
            !activeBall
        ) return;

        dragging = false;

        aim.style.display = "none";

        const p =
            pointerPosition(event);

        const dx =
            activeBall.x - p.x;

        const dy =
            activeBall.y - p.y;

        const length =
            Math.sqrt(
                dx * dx +
                dy * dy
            );

        if (length < 0.025) {

            activeBall = null;

            return;

        }

        const power =
            Math.min(length, 0.55);

        const speed = 6;

        activeBall.vx =
            (dx / length)
            * power
            * speed;

        activeBall.vy =
            (dy / length)
            * power
            * speed;

        activeBall = null;

        moving = true;

        status.textContent =
            "💥 발사!";

        startPhysics();

    }
);


/*
    벽 충돌
*/

function wallCollision(ball) {

    const radius = 0.035;

    if (ball.x < radius) {

        ball.x = radius;

        ball.vx =
            Math.abs(ball.vx)
            * 0.78;

    }

    if (ball.x > 1 - radius) {

        ball.x = 1 - radius;

        ball.vx =
            -Math.abs(ball.vx)
            * 0.78;

    }

    if (ball.y < radius) {

        ball.y = radius;

        ball.vy =
            Math.abs(ball.vy)
            * 0.78;

    }

    if (ball.y > 1 - radius) {

        ball.y = 1 - radius;

        ball.vy =
            -Math.abs(ball.vy)
            * 0.78;

    }

}


/*
    구멍 검사
*/

function checkHole(ball) {

    for (const hole of holes) {

        const d =
            distance(
                ball.x,
                ball.y,
                hole[0],
                hole[1]
            );

        if (d < 0.065) {

            ball.alive = false;

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


/*
    알 충돌
*/

function collideBalls() {

    const alive =
        balls.filter(
            b => b.alive
        );

    for (let i = 0; i < alive.length; i++) {

        for (
            let j = i + 1;
            j < alive.length;
            j++
        ) {

            const a = alive[i];

            const b = alive[j];

            const dx =
                b.x - a.x;

            const dy =
                b.y - a.y;

            const d =
                Math.sqrt(
                    dx * dx +
                    dy * dy
                );

            const minDistance =
                0.068;

            if (
                d >= minDistance ||
                d === 0
            ) continue;

            const nx =
                dx / d;

            const ny =
                dy / d;

            const relativeVelocity =
                (b.vx - a.vx) * nx +
                (b.vy - a.vy) * ny;

            if (relativeVelocity < 0) {

                const impulse =
                    -relativeVelocity * 0.92;

                a.vx -=
                    impulse * nx;

                a.vy -=
                    impulse * ny;

                b.vx +=
                    impulse * nx;

                b.vy +=
                    impulse * ny;

            }

            const overlap =
                minDistance - d;

            a.x -=
                nx * overlap / 2;

            a.y -=
                ny * overlap / 2;

            b.x +=
                nx * overlap / 2;

            b.y +=
                ny * overlap / 2;

        }

    }

}


/*
    물리 엔진
*/

function startPhysics() {

    lastTime =
        performance.now();

    function frame(now) {

        if (paused) return;

        const dt =
            Math.min(
                (now - lastTime) / 1000,
                0.025
            );

        lastTime = now;

        let anyMoving = false;

        for (const ball of balls) {

            if (!ball.alive) continue;

            ball.x +=
                ball.vx * dt;

            ball.y +=
                ball.vy * dt;

            /*
                마찰
            */

            ball.vx *=
                Math.pow(0.035, dt);

            ball.vy *=
                Math.pow(0.035, dt);

            wallCollision(ball);

            checkHole(ball);

            const speed =
                Math.sqrt(
                    ball.vx * ball.vx +
                    ball.vy * ball.vy
                );

            if (speed > 0.025) {

                anyMoving = true;

            } else {

                ball.vx = 0;

                ball.vy = 0;

            }

        }

        collideBalls();

        renderBalls();

        updateScore();

        if (anyMoving) {

            animationId =
                requestAnimationFrame(frame);

        } else {

            moving = false;

            checkWinner();

        }

    }

    animationId =
        requestAnimationFrame(frame);

}


/*
    승리 검사
*/

function checkWinner() {

    const black =
        balls.some(
            b =>
                b.player === 0 &&
                b.alive
        );

    const white =
        balls.some(
            b =>
                b.player === 1 &&
                b.alive
        );

    if (!black) {

        gameOver = true;

        status.textContent =
            "🎉 ⚪ 흰 알 승리!";

        return;

    }

    if (!white) {

        gameOver = true;

        status.textContent =
            "🎉 ⚫ 검은 알 승리!";

        return;

    }

    turn =
        turn === 0 ? 1 : 0;

    updateStatus();

    /*
        AI 차례라면
        잠시 기다렸다가 공격
    */

    if (
        turn === 1 &&
        modeSelect.value === "ai"
    ) {

        setTimeout(
            aiTurn,
            getAiDelay()
        );

    }

}


/*
    AI 난이도별 반응 시간
*/

function getAiDelay() {

    const difficulty =
        difficultySelect.value;

    if (difficulty === "easy") {

        return 900;

    }

    if (difficulty === "hard") {

        return 350;

    }

    return 600;

}


/*
    AI가 선택할 알
*/

function chooseAiBall() {

    const aiBalls =
        balls.filter(
            b =>
                b.alive &&
                b.player === 1
        );

    if (aiBalls.length === 0)
        return null;

    const playerBalls =
        balls.filter(
            b =>
                b.alive &&
                b.player === 0
        );

    /*
        쉬움:
        랜덤
    */

    if (
        difficultySelect.value === "easy"
    ) {

        return aiBalls[
            Math.floor(
                Math.random() *
                aiBalls.length
            )
        ];

    }

    /*
        보통:
        상대 알에 가까운 알
    */

    if (
        difficultySelect.value === "normal"
    ) {

        let best = aiBalls[0];

        let bestDistance = Infinity;

        for (const ai of aiBalls) {

            for (const enemy of playerBalls) {

                const d =
                    distance(
                        ai.x,
                        ai.y,
                        enemy.x,
                        enemy.y
                    );

                if (
                    d <
                    bestDistance
                ) {

                    bestDistance = d;

                    best = ai;

                }

            }

        }

        return best;

    }

    /*
        어려움:
        가장 가까운 적 + 구멍 방향을
        어느 정도 고려
    */

    let best = aiBalls[0];

    let bestScore = Infinity;

    for (const ai of aiBalls) {

        for (const enemy of playerBalls) {

            const d =
                distance(
                    ai.x,
                    ai.y,
                    enemy.x,
                    enemy.y
                );

            /*
                적을 구멍 쪽으로 밀 수 있는
                방향을 선호
            */

            let holeBonus = 0;

            for (const hole of holes) {

                const enemyHole =
                    distance(
                        enemy.x,
                        enemy.y,
                        hole[0],
                        hole[1]
                    );

                holeBonus =
                    Math.min(
                        holeBonus,
                        enemyHole
                    );

            }

            const scoreValue =
                d + holeBonus * 0.2;

            if (
                scoreValue <
                bestScore
            ) {

                bestScore =
                    scoreValue;

                best = ai;

            }

        }

    }

    return best;

}


/*
    AI 공격
*/

function aiTurn() {

    if (
        gameOver ||
        paused ||
        moving ||
        turn !== 1 ||
        modeSelect.value !== "ai"
    ) {

        return;

    }

    const aiBall =
        chooseAiBall();

    if (!aiBall) return;

    const enemies =
        balls.filter(
            b =>
                b.alive &&
                b.player === 0
        );

    if (enemies.length === 0)
        return;

    let target =
        enemies[0];

    /*
        AI 난이도에 따라
        목표 선정
    */

    if (
        difficultySelect.value === "easy"
    ) {

        target =
            enemies[
                Math.floor(
                    Math.random() *
                    enemies.length
                )
            ];

    } else {

        let closest =
            Infinity;

        for (const enemy of enemies) {

            const d =
                distance(
                    aiBall.x,
                    aiBall.y,
                    enemy.x,
                    enemy.y
                );

            if (d < closest) {

                closest = d;

                target = enemy;

            }

        }

    }

    /*
        적 방향으로 발사

        AI 난이도별 오차
    */

    let error = 0;

    if (
        difficultySelect.value === "easy"
    ) {

        error =
            (Math.random() - .5)
            * 0.45;

    }

    if (
        difficultySelect.value === "normal"
    ) {

        error =
            (Math.random() - .5)
            * 0.16;

    }

    if (
        difficultySelect.value === "hard"
    ) {

        error =
            (Math.random() - .5)
            * 0.05;

    }

    const dx =
        target.x -
        aiBall.x;

    const dy =
        target.y -
        aiBall.y;

    const length =
        Math.sqrt(
            dx * dx +
            dy * dy
        );

    if (length < 0.01)
        return;

    /*
        AI가 조준하는 방향
    */

    let angle =
        Math.atan2(dy, dx);

    angle += error;

    /*
        거리와 난이도에 따른 힘
    */

    let power =
        Math.min(
            .22 +
            length * 0.55,
            .52
        );

    if (
        difficultySelect.value === "easy"
    ) {

        power *=
            0.65 +
            Math.random() * 0.3;

    }

    if (
        difficultySelect.value === "normal"
    ) {

        power *=
            0.88 +
            Math.random() * 0.14;

    }

    if (
        difficultySelect.value === "hard"
    ) {

        power *=
            0.96 +
            Math.random() * 0.05;

    }

    aiBall.vx =
        Math.cos(angle)
        * power
        * 6;

    aiBall.vy =
        Math.sin(angle)
        * power
        * 6;

    moving = true;

    status.textContent =
        "🤖 AI가 공격합니다!";

    startPhysics();

}


/*
    일시정지
*/

function pauseGame() {

    if (
        gameOver ||
        paused
    ) return;

    paused = true;

    pauseOverlay.style.display =
        "flex";

    pauseButton.textContent =
        "▶ 계속하기";

}


/*
    계속하기
*/

function resumeGame() {

    if (!paused) return;

    paused = false;

    pauseOverlay.style.display =
        "none";

    pauseButton.textContent =
        "⏸ 일시정지";

    if (moving) {

        startPhysics();

    } else {

        updateStatus();

        if (
            turn === 1 &&
            modeSelect.value === "ai"
        ) {

            setTimeout(
                aiTurn,
                250
            );

        }

    }

}


/*
    ESC 키
*/

document.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Escape"
        ) {

            if (paused) {

                resumeGame();

            } else {

                pauseGame();

            }

        }

    }
);


/*
    버튼
*/

pauseButton.addEventListener(
    "click",
    function() {

        if (paused) {

            resumeGame();

        } else {

            pauseGame();

        }

    }
);


resumeButton.addEventListener(
    "click",
    resumeGame
);


restartButton.addEventListener(
    "click",
    createGame
);


newGameButton.addEventListener(
    "click",
    createGame
);


/*
    AI 메뉴 표시/숨김
*/

modeSelect.addEventListener(
    "change",
    function() {

        if (
            modeSelect.value === "ai"
        ) {

            difficultyRow.style.display =
                "flex";

        } else {

            difficultyRow.style.display =
                "none";

        }

        createGame();

    }
);


countSelect.addEventListener(
    "change",
    createGame
);


difficultySelect.addEventListener(
    "change",
    function() {

        if (
            turn === 1 &&
            modeSelect.value === "ai" &&
            !moving &&
            !paused
        ) {

            setTimeout(
                aiTurn,
                250
            );

        }

    }
);


/*
    시작
*/

createGame();

</script>

</body>
</html>
"""

components.html(
    game_html,
    height=900,
    scrolling=False
)
