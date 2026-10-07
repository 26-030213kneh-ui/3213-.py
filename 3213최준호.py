import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="알까기",
    page_icon="⚫",
    layout="centered",
)

st.title("⚫ 알까기")

GAME = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">

<style>
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    overflow-x: hidden;
    font-family: Arial, sans-serif;
    user-select: none;
}

#app {
    width: 100%;
    max-width: 720px;
    margin: 0 auto;
    padding: 4px 8px 20px;
}

#menu {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px;
    margin-bottom: 12px;
}

.control {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.control label {
    font-size: 13px;
    font-weight: bold;
    color: #555;
}

select,
button {
    width: 100%;
    min-height: 42px;
    border: 1px solid #bbb;
    border-radius: 9px;
    background: white;
    padding: 7px 10px;
    font-size: 14px;
}

button {
    cursor: pointer;
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
    font-weight: bold;
    font-size: 18px;
    min-height: 25px;
    margin-bottom: 4px;
}

#score {
    text-align: center;
    color: #666;
    font-size: 13px;
    margin-bottom: 9px;
}

/*
 * 핵심 수정:
 * 게임판의 비율을 고정하고,
 * 부모 영역 안에서만 크기가 결정되도록 함.
 */
#boardWrap {
    width: 100%;
    display: flex;
    justify-content: center;
    overflow: visible;
}

#board {
    position: relative;

    width: min(
        calc(100vw - 36px),
        640px
    );

    height: min(
        calc(100vw - 36px),
        640px
    );

    /*
     * iframe 내부 높이가 부족해지는 문제를 막기 위해
     * 절대로 height를 viewport 단위로 잡지 않음.
     */
    flex: 0 0 auto;

    background:
        radial-gradient(
            circle at 50% 45%,
            #e3b55f 0%,
            #c9953d 100%
        );

    border: 14px solid #68411d;
    border-radius: 17px;

    box-shadow:
        inset 0 0 30px rgba(0,0,0,.25),
        0 7px 16px rgba(0,0,0,.25);

    overflow: hidden;
    touch-action: none;
}

.hole {
    position: absolute;
    width: 42px;
    height: 42px;

    background:
        radial-gradient(
            circle,
            #000 0%,
            #151515 65%,
            #333 100%
        );

    border-radius: 50%;
    transform: translate(-50%, -50%);

    z-index: 2;

    box-shadow:
        inset 0 4px 9px rgba(0,0,0,.9);
}

.marble {
    position: absolute;

    width: 32px;
    height: 32px;

    transform:
        translate(-50%, -50%);

    border-radius: 50%;

    z-index: 5;

    pointer-events: none;

    box-shadow:
        2px 4px 6px rgba(0,0,0,.45),
        inset 5px 5px 5px rgba(255,255,255,.3);
}

.black {
    background:
        radial-gradient(
            circle at 30% 25%,
            #777,
            #252525 55%,
            #050505
        );

    border: 2px solid #000;
}

.white {
    background:
        radial-gradient(
            circle at 30% 25%,
            #fff,
            #ddd 60%,
            #999
        );

    border: 2px solid #777;
}

#aim {
    position: absolute;
    height: 4px;
    display: none;
    z-index: 10;

    background:
        linear-gradient(
            90deg,
            #e53935,
            #ff8a80
        );

    border-radius: 4px;
    transform-origin: left center;
    pointer-events: none;
}

#pauseOverlay {
    position: absolute;
    inset: 0;

    z-index: 100;

    display: none;

    align-items: center;
    justify-content: center;

    background: rgba(0,0,0,.68);
}

#pauseBox {
    width: min(85%, 330px);
    padding: 22px;

    background: white;
    border-radius: 16px;

    text-align: center;

    box-shadow:
        0 10px 30px rgba(0,0,0,.4);
}

#pauseBox h2 {
    margin-top: 0;
}

.pauseButtons {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

#hint {
    text-align: center;
    margin-top: 10px;
    color: #777;
    font-size: 12px;
}

@media (max-width: 500px) {

    #menu {
        grid-template-columns: 1fr;
    }

    #board {
        width: calc(100vw - 28px);
        height: calc(100vw - 28px);
        border-width: 10px;
    }

    .hole {
        width: 34px;
        height: 34px;
    }

    .marble {
        width: 28px;
        height: 28px;
    }
}
</style>
</head>

<body>

<div id="app">

    <div id="menu">

        <div class="control">
            <label>게임 방식</label>

            <select id="mode">
                <option value="ai">🤖 AI와 대전</option>
                <option value="pvp">👥 2인 대전</option>
            </select>
        </div>

        <div class="control">
            <label>알 개수</label>

            <select id="count">
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

        <div class="control" id="difficultyBox">
            <label>AI 난이도</label>

            <select id="difficulty">
                <option value="easy">쉬움</option>
                <option value="normal" selected>보통</option>
                <option value="hard">어려움</option>
            </select>
        </div>

        <div class="control">
            <label>&nbsp;</label>

            <button id="newGame">
                🔄 새 게임
            </button>
        </div>

    </div>

    <div id="status">
        ⚫ 플레이어 1 차례
    </div>

    <div id="score">
        ⚫ 3개 · ⚪ 3개
    </div>

    <div id="boardWrap">

        <div id="board">

            <div class="hole"
                 style="left:0%;top:0%"></div>

            <div class="hole"
                 style="left:50%;top:0%"></div>

            <div class="hole"
                 style="left:100%;top:0%"></div>

            <div class="hole"
                 style="left:0%;top:100%"></div>

            <div class="hole"
                 style="left:50%;top:100%"></div>

            <div class="hole"
                 style="left:100%;top:100%"></div>

            <div id="aim"></div>

            <div id="pauseOverlay">

                <div id="pauseBox">

                    <h2>⏸ 일시정지</h2>

                    <p>게임이 잠시 멈췄습니다.</p>

                    <div class="pauseButtons">

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

    </div>

    <div id="hint">
        알을 뒤로 당긴 뒤 놓으세요 · ESC = 일시정지
    </div>

</div>


<script>
const board = document.getElementById("board");
const status = document.getElementById("status");
const score = document.getElementById("score");

const mode = document.getElementById("mode");
const count = document.getElementById("count");
const difficulty = document.getElementById("difficulty");

const difficultyBox =
    document.getElementById("difficultyBox");

const newGame =
    document.getElementById("newGame");

const aim =
    document.getElementById("aim");

const pauseOverlay =
    document.getElementById("pauseOverlay");

const resume =
    document.getElementById("resume");

const restart =
    document.getElementById("restart");


let balls = [];
let turn = 0;

let dragging = false;
let selectedBall = null;

let moving = false;
let paused = false;
let gameOver = false;

let animationFrame = null;
let lastTime = 0;


/* 구멍 */
const holes = [
    [0, 0],
    [.5, 0],
    [1, 0],
    [0, 1],
    [.5, 1],
    [1, 1]
];


/* 좌표 변환 */
function getPointer(event) {

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


/* 거리 */
function dist(x1, y1, x2, y2) {

    return Math.sqrt(
        (x1 - x2) ** 2 +
        (y1 - y2) ** 2
    );
}


/* 게임 생성 */
function resetGame() {

    if (animationFrame) {
        cancelAnimationFrame(animationFrame);
        animationFrame = null;
    }

    balls.forEach(ball => {
        if (ball.el) {
            ball.el.remove();
        }
    });

    balls = [];

    turn = 0;
    dragging = false;
    selectedBall = null;
    moving = false;
    paused = false;
    gameOver = false;

    pauseOverlay.style.display = "none";
    aim.style.display = "none";

    const amount =
        Math.max(
            1,
            Math.min(
                8,
                Number(count.value)
            )
        );

    /*
     * 알 간격을 자동으로 계산해서
     * 8개에서도 바둑판 밖으로 나가지 않게 함.
     */
    const spacing =
        Math.min(
            0.055,
            0.34 / amount
        );

    for (let i = 0; i < amount; i++) {

        const offset =
            (i - (amount - 1) / 2)
            * spacing;

        balls.push({
            player: 0,
            x: .5 + offset,
            y: .77,
            vx: 0,
            vy: 0,
            alive: true,
            el: null
        });

        balls.push({
            player: 1,
            x: .5 + offset,
            y: .23,
            vx: 0,
            vy: 0,
            alive: true,
            el: null
        });
    }

    render();

    updateScore();
    updateStatus();

    if (mode.value === "ai") {
        difficultyBox.style.display = "flex";
    } else {
        difficultyBox.style.display = "none";
    }
}


/* 알 생성 */
function createElement(ball) {

    const el =
        document.createElement("div");

    el.className =
        "marble " +
        (ball.player === 0
            ? "black"
            : "white");

    board.appendChild(el);

    ball.el = el;
}


/* 화면 표시 */
function render() {

    for (const ball of balls) {

        if (!ball.alive) continue;

        if (!ball.el) {
            createElement(ball);
        }

        ball.el.style.left =
            (ball.x * 100) + "%";

        ball.el.style.top =
            (ball.y * 100) + "%";
    }
}


/* 점수 */
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
        "⚫ " + black +
        "개 · ⚪ " + white + "개";
}


/* 상태 */
function updateStatus() {

    if (gameOver) return;

    if (turn === 0) {

        status.textContent =
            "⚫ 플레이어 1 차례";

    } else if (mode.value === "ai") {

        status.textContent =
            "🤖 AI 차례";

    } else {

        status.textContent =
            "⚪ 플레이어 2 차례";
    }
}


/* 사람 차례인지 */
function canControl() {

    if (gameOver) return false;
    if (paused) return false;
    if (moving) return false;

    if (
        turn === 1 &&
        mode.value === "ai"
    ) {
        return false;
    }

    return true;
}


/* 알 선택 */
board.addEventListener(
    "pointerdown",
    event => {

        if (!canControl()) return;

        const p =
            getPointer(event);

        let nearest = null;
        let nearestDistance = Infinity;

        for (const ball of balls) {

            if (
                !ball.alive ||
                ball.player !== turn
            ) continue;

            const d =
                dist(
                    p.x,
                    p.y,
                    ball.x,
                    ball.y
                );

            if (
                d < .09 &&
                d < nearestDistance
            ) {

                nearest = ball;
                nearestDistance = d;
            }
        }

        if (!nearest) return;

        selectedBall = nearest;
        dragging = true;

        board.setPointerCapture(
            event.pointerId
        );
    }
);


/* 조준 */
board.addEventListener(
    "pointermove",
    event => {

        if (
            !dragging ||
            !selectedBall ||
            paused
        ) return;

        const p =
            getPointer(event);

        const dx =
            selectedBall.x - p.x;

        const dy =
            selectedBall.y - p.y;

        const length =
            Math.sqrt(
                dx * dx +
                dy * dy
            );

        if (length < .01) {

            aim.style.display = "none";

            return;
        }

        const angle =
            Math.atan2(dy, dx);

        const width =
            Math.min(
                length *
                board.clientWidth *
                1.5,
                board.clientWidth * .45
            );

        aim.style.display = "block";

        aim.style.left =
            (selectedBall.x * 100) + "%";

        aim.style.top =
            (selectedBall.y * 100) + "%";

        aim.style.width =
            width + "px";

        aim.style.transform =
            "rotate(" +
            angle +
            "rad)";
    }
);


/* 발사 */
board.addEventListener(
    "pointerup",
    event => {

        if (
            !dragging ||
            !selectedBall
        ) return;

        dragging = false;

        aim.style.display = "none";

        const p =
            getPointer(event);

        const dx =
            selectedBall.x - p.x;

        const dy =
            selectedBall.y - p.y;

        const length =
            Math.sqrt(
                dx * dx +
                dy * dy
            );

        if (length < .025) {

            selectedBall = null;

            return;
        }

        const power =
            Math.min(length, .52);

        const speed = 6;

        selectedBall.vx =
            (dx / length)
            * power
            * speed;

        selectedBall.vy =
            (dy / length)
            * power
            * speed;

        selectedBall = null;

        moving = true;

        status.textContent = "💥 발사!";

        startPhysics();
    }
);


/* 벽 */
function wallCollision(ball) {

    const r = .035;

    if (ball.x < r) {
        ball.x = r;
        ball.vx =
            Math.abs(ball.vx) * .75;
    }

    if (ball.x > 1 - r) {
        ball.x = 1 - r;
        ball.vx =
            -Math.abs(ball.vx) * .75;
    }

    if (ball.y < r) {
        ball.y = r;
        ball.vy =
            Math.abs(ball.vy) * .75;
    }

    if (ball.y > 1 - r) {
        ball.y = 1 - r;
        ball.vy =
            -Math.abs(ball.vy) * .75;
    }
}


/* 구멍 */
function checkHole(ball) {

    for (const hole of holes) {

        const d =
            dist(
                ball.x,
                ball.y,
                hole[0],
                hole[1]
            );

        if (d < .063) {

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


/* 알 충돌 */
function collideBalls() {

    const alive =
        balls.filter(b => b.alive);

    const radius = .067;

    for (
        let i = 0;
        i < alive.length;
        i++
    ) {

        for (
            let j = i + 1;
            j < alive.length;
            j++
        ) {

            const a = alive[i];
            const b = alive[j];

            const dx = b.x - a.x;
            const dy = b.y - a.y;

            const d =
                Math.sqrt(
                    dx * dx +
                    dy * dy
                );

            if (
                d >= radius ||
                d < .000001
            ) continue;

            const nx = dx / d;
            const ny = dy / d;

            const relative =
                (b.vx - a.vx) * nx +
                (b.vy - a.vy) * ny;

            if (relative < 0) {

                const impulse =
                    -relative * .9;

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
                radius - d;

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


/* 물리 */
function startPhysics() {

    lastTime =
        performance.now();

    function loop(now) {

        if (paused) return;

        const dt =
            Math.min(
                (now - lastTime) / 1000,
                .025
            );

        lastTime = now;

        let active = false;

        for (const ball of balls) {

            if (!ball.alive) continue;

            ball.x += ball.vx * dt;
            ball.y += ball.vy * dt;

            /*
             * 마찰
             */
            const friction =
                Math.pow(.035, dt);

            ball.vx *= friction;
            ball.vy *= friction;

            wallCollision(ball);
            checkHole(ball);

            const speed =
                Math.sqrt(
                    ball.vx * ball.vx +
                    ball.vy * ball.vy
                );

            if (speed > .025) {
                active = true;
            } else {
                ball.vx = 0;
                ball.vy = 0;
            }
        }

        collideBalls();
        render();
        updateScore();

        if (active) {

            animationFrame =
                requestAnimationFrame(loop);

        } else {

            moving = false;

            checkWinner();
        }
    }

    animationFrame =
        requestAnimationFrame(loop);
}


/* 승리 */
function checkWinner() {

    const blackAlive =
        balls.some(
            b =>
                b.player === 0 &&
                b.alive
        );

    const whiteAlive =
        balls.some(
            b =>
                b.player === 1 &&
                b.alive
        );

    if (!blackAlive) {

        gameOver = true;

        status.textContent =
            "🎉 ⚪ 흰색 승리!";

        return;
    }

    if (!whiteAlive) {

        gameOver = true;

        status.textContent =
            "🎉 ⚫ 검은색 승리!";

        return;
    }

    turn =
        turn === 0 ? 1 : 0;

    updateStatus();

    if (
        turn === 1 &&
        mode.value === "ai"
    ) {

        setTimeout(
            aiTurn,
            500
        );
    }
}


/* AI 알 선택 */
function chooseAI() {

    const aiBalls =
        balls.filter(
            b =>
                b.alive &&
                b.player === 1
        );

    if (!aiBalls.length) {
        return null;
    }

    if (
        difficulty.value === "easy"
    ) {

        return aiBalls[
            Math.floor(
                Math.random() *
                aiBalls.length
            )
        ];
    }

    const enemies =
        balls.filter(
            b =>
                b.alive &&
                b.player === 0
        );

    if (!enemies.length) {
        return aiBalls[0];
    }

    let best = aiBalls[0];
    let bestDistance = Infinity;

    for (const ai of aiBalls) {

        for (const enemy of enemies) {

            const d =
                dist(
                    ai.x,
                    ai.y,
                    enemy.x,
                    enemy.y
                );

            if (d < bestDistance) {

                bestDistance = d;
                best = ai;
            }
        }
    }

    return best;
}


/* AI 공격 */
function aiTurn() {

    if (
        gameOver ||
        paused ||
        moving ||
        mode.value !== "ai" ||
        turn !== 1
    ) return;

    const ai =
        chooseAI();

    if (!ai) return;

    const enemies =
        balls.filter(
            b =>
                b.alive &&
                b.player === 0
        );

    if (!enemies.length) return;

    let target = enemies[0];
    let closest = Infinity;

    for (const enemy of enemies) {

        const d =
            dist(
                ai.x,
                ai.y,
                enemy.x,
                enemy.y
            );

        if (d < closest) {

            closest = d;
            target = enemy;
        }
    }

    let angle =
        Math.atan2(
            target.y - ai.y,
            target.x - ai.x
        );

    /*
     * 난이도별 조준 오차
     */
    let error = 0;

    if (difficulty.value === "easy") {

        error =
            (Math.random() - .5) * .65;

    } else if (
        difficulty.value === "normal"
    ) {

        error =
            (Math.random() - .5) * .22;

    } else {

        error =
            (Math.random() - .5) * .055;
    }

    angle += error;

    let power =
        Math.min(
            .22 + closest * .6,
            .50
        );

    if (difficulty.value === "easy") {

        power *=
            .65 +
            Math.random() * .3;

    } else if (
        difficulty.value === "normal"
    ) {

        power *=
            .88 +
            Math.random() * .12;

    } else {

        power *=
            .96 +
            Math.random() * .04;
    }

    ai.vx =
        Math.cos(angle)
        * power
        * 6;

    ai.vy =
        Math.sin(angle)
        * power
        * 6;

    moving = true;

    status.textContent =
        "🤖 AI가 공격합니다!";

    startPhysics();
}


/* 일시정지 */
function pauseGame() {

    if (gameOver) return;

    paused = true;

    pauseOverlay.style.display =
        "flex";
}


/* 재개 */
function resumeGame() {

    if (!paused) return;

    paused = false;

    pauseOverlay.style.display =
        "none";

    if (moving) {

        startPhysics();

    } else {

        updateStatus();

        if (
            turn === 1 &&
            mode.value === "ai"
        ) {

            setTimeout(
                aiTurn,
                250
            );
        }
    }
}


/*
 * ESC
 *
 * iframe 내부에서 키보드 포커스를 얻은 경우뿐 아니라
 * 게임판을 클릭한 뒤에도 정상적으로 동작하도록 함.
 */
document.addEventListener(
    "keydown",
    event => {

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


/* 설정 변경 */
mode.addEventListener(
    "change",
    resetGame
);

count.addEventListener(
    "change",
    resetGame
);

difficulty.addEventListener(
    "change",
    () => {
        if (
            mode.value === "ai" &&
            turn === 1 &&
            !moving &&
            !paused
        ) {
            setTimeout(
                aiTurn,
                300
            );
        }
    }
);


/* 버튼 */
newGame.addEventListener(
    "click",
    resetGame
);

resume.addEventListener(
    "click",
    resumeGame
);

restart.addEventListener(
    "click",
    resetGame
);


/* 시작 */
resetGame();

</script>

</body>
</html>
"""

# 기존 900px보다 충분히 크게 확보해서
# 바둑판 하단이 iframe에서 잘리지 않도록 수정
components.html(
    GAME,
    height=1050,
    scrolling=True
)
