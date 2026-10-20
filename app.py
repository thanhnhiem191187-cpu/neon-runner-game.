
 import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Neon Cyber-Runner - Phonk & Skill Shop",
    page_icon="🏎️",
    layout="centered"
)

# Tùy chỉnh giao diện Streamlit bằng CSS
st.markdown("""
    <style>
    .main {
        background-color: #0d1117;
        color: #ffffff;
    }
    h1 {
        text-align: center;
        color: #ff0055;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-shadow: 0 0 10px #ff0055, 0 0 20px #ff0055;
    }
    .stApp {
        background: radial-gradient(circle, #1a0022 0%, #050010 100%);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔥 NEON RUNNER: PHONK EDITION 🔥")
st.caption("Nhặt **Xu Vàng 🪙**, Trang bị **2 Kĩ Năng** trong Cửa Hàng, Hồi Chiêu **5s** & Quẩy cùng Phonk!")

# Mã HTML + JavaScript của Game
game_code = r"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        background: transparent;
        display: flex;
        justify-content: center;
        align-items: center;
        font-family: 'Courier New', Courier, monospace;
        overflow: hidden;
    }
    #gameContainer {
        position: relative;
        box-shadow: 0 0 35px #ff0055;
        border-radius: 12px;
        overflow: hidden;
        border: 2px solid #ff0055;
    }
    canvas {
        background: #080010;
        display: block;
    }
    #overlay {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(8, 0, 16, 0.92);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: #fff;
        padding: 10px;
        box-sizing: border-box;
    }
    .btn {
        background: #ff0055;
        color: #fff;
        border: none;
        padding: 12px 28px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 25px;
        cursor: pointer;
        box-shadow: 0 0 20px #ff0055;
        transition: 0.2s;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 10px;
    }
    .btn:hover {
        transform: scale(1.08);
        box-shadow: 0 0 30px #ff0055;
        background: #00f3ff;
        color: #000;
    }
    .shop-card {
        border: 1px solid #ff0055;
        background: rgba(255, 0, 85, 0.1);
        border-radius: 10px;
        padding: 10px;
        width: 85%;
        text-align: center;
        margin-bottom: 10px;
    }
    .shop-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 6px 0;
        font-size: 13px;
    }
    .action-btn {
        background: #ffe600;
        color: #000;
        border: none;
        padding: 4px 10px;
        font-size: 12px;
        font-weight: bold;
        border-radius: 12px;
        cursor: pointer;
    }
    .action-btn:disabled {
        background: #444;
        color: #888;
        cursor: not-allowed;
    }
    .hud-skill-btn {
        background: #ff0055;
        color: #fff;
        border: none;
        padding: 8px 12px;
        font-size: 12px;
        font-weight: bold;
        border-radius: 15px;
        cursor: pointer;
        box-shadow: 0 0 10px #ff0055;
        min-width: 130px;
    }
    .hud-skill-btn:disabled {
        background: #333;
        color: #777;
        box-shadow: none;
        cursor: not-allowed;
    }
    #hud {
        position: absolute;
        top: 10px;
        left: 10px;
        right: 10px;
        display: flex;
        justify-content: space-between;
        color: #fff;
        font-weight: bold;
        font-size: 16px;
        pointer-events: none;
    }
    #skillBar {
        position: absolute;
        bottom: 12px;
        display: flex;
        gap: 10px;
    }
</style>
</head>
<body>

<div id="gameContainer">
    <canvas id="gameCanvas" width="400" height="550"></canvas>

    <div id="hud">
        <div id="scoreText">SCORE: 0</div>
        <div id="coinText" style="color: #ffe600;">🪙 0</div>
    </div>

    <!-- Thanh hiển thị 2 kĩ năng trang bị với Hồi Chiêu -->
    <div id="skillBar">
        <button id="slot1Btn" class="hud-skill-btn" onclick="useSkill(1)" disabled>[Q] Trống</button>
        <button id="slot2Btn" class="hud-skill-btn" onclick="useSkill(2)" disabled>[E] Trống</button>
    </div>

    <div id="overlay">
        <h2 id="title" style="color: #ff0055; text-shadow: 0 0 15px #ff0055; font-size: 26px; margin: 5px 0;">CỬA HÀNG & TRANG BỊ</h2>
        <div style="color: #ffe600; font-weight: bold; margin-bottom: 8px;" id="shopCoinText">Số xu hiện có: 🪙 0</div>

        <div class="shop-card">
            <div class="shop-item">
                <span>🌪️ Gió Quét (5 Xu) - Sở hữu: <b id="owned1">0</b></span>
                <div>
                    <button class="action-btn" onclick="buySkill(1)">Mua</button>
                    <button class="action-btn" onclick="equipSkill(1)">Trang bị</button>
                </div>
            </div>
            <div class="shop-item">
                <span>🛡️ Bất Tử (7 Xu) - Sở hữu: <b id="owned2">0</b></span>
                <div>
                    <button class="action-btn" onclick="buySkill(2)">Mua</button>
                    <button class="action-btn" onclick="equipSkill(2)">Trang bị</button>
                </div>
            </div>
        </div>

        <div style="font-size: 12px; color: #00f3ff; margin-bottom: 10px;">
            Trang bị hiện tại: Ô 1 (Q): <span id="eq1Text">Trống</span> | Ô 2 (E): <span id="eq2Text">Trống</span>
        </div>

        <button class="btn" onclick="startGame()">BẮT ĐẦU CHƠI</button>
    </div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const overlay = document.getElementById("overlay");

let player = { x: 180, y: 450, width: 40, height: 60, speed: 6.5 };
let obstacles = [];
let coins = [];
let score = 0;
let walletCoins = 0; // Xu tổng lưu trữ
let sessionCoins = 0; // Xu nhặt trong trận
let gameSpeed = 4.5;
let isPlaying = false;
let animationId;
let keys = {};

// Quản lý kĩ năng
let ownedSkills = { 1: 0, 2: 0 }; // 1: Gió quét, 2: Bất tử
let equippedSlots = { 1: null, 2: null }; // Tối đa 2 kĩ năng trang bị
let cooldowns = { 1: 0, 2: 0 }; // Đếm ngược hồi chiêu (tính bằng frame ~ 60fps, 5s = 300)

let isWindActive = false;
let isShieldActive = false;
let windTimer = 0;
let shieldTimer = 0;

// Trình tạo Nhạc Phonk
let audioCtx = null;
let phonkTimer = null;
let step = 0;

function initAudio() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
}

function playCowbell(freq, time) {
    if (!audioCtx) return;
    let osc1 = audioCtx.createOscillator();
    let osc2 = audioCtx.createOscillator();
    let gain = audioCtx.createGain();

    osc1.type = 'square';
    osc2.type = 'square';
    osc1.frequency.setValueAtTime(freq, time);
    osc2.frequency.setValueAtTime(freq * 1.48, time);

    gain.gain.setValueAtTime(0.12, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.18);

    osc1.connect(gain);
    osc2.connect(gain);
    gain.connect(audioCtx.destination);

    osc1.start(time);
    osc2.start(time);
    osc1.stop(time + 0.18);
    osc2.stop(time + 0.18);
}

function playBass808(freq, time) {
    if (!audioCtx) return;
    let osc = audioCtx.createOscillator();
    let gain = audioCtx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, time);
    osc.frequency.exponentialRampToValueAtTime(30, time + 0.25);

    gain.gain.setValueAtTime(0.4, time);
    gain.gain.exponentialRampToValueAtTime(0.01, time + 0.25);

    osc.connect(gain);
    gain.connect(audioCtx.destination);

    osc.start(time);
    osc.stop(time + 0.25);
}

function playSoundEffect(type) {
    if (!audioCtx) return;
    let osc = audioCtx.createOscillator();
    let gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    let now = audioCtx.currentTime;

    if (type === 'coin') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(987.77, now);
        osc.frequency.setValueAtTime(1318.51, now + 0.08);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.2);
        osc.start(now);
        osc.stop(now + 0.2);
    } else if (type === 'skill') {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(400, now);
        osc.frequency.exponentialRampToValueAtTime(1200, now + 0.3);
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.3);
        osc.start(now);
        osc.stop(now + 0.3);
    } else if (type === 'crash') {
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(200, now);
        osc.frequency.exponentialRampToValueAtTime(20, now + 0.5);
        gain.gain.setValueAtTime(0.5, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.5);
        osc.start(now);
        osc.stop(now + 0.5);
    }
}

function startPhonkMusic() {
    if (phonkTimer) clearInterval(phonkTimer);
    const notes = [587.33, 587.33, 783.99, 659.25, 587.33, 523.25, 587.33, 440.00];
    const bassNotes = [110, 110, 146.83, 130.81];

    step = 0;
    phonkTimer = setInterval(() => {
        if (!isPlaying || !audioCtx) return;
        let now = audioCtx.currentTime;
        let note = notes[step % notes.length];
        playCowbell(note, now);
        if (step % 2 === 0) {
            let bNote = bassNotes[Math.floor(step / 2) % bassNotes.length];
            playBass808(bNote, now);
        }
        step++;
    }, 140);
}

function stopPhonkMusic() {
    if (phonkTimer) clearInterval(phonkTimer);
}

// --- CỬA HÀNG & TRANG BỊ ---
function updateShopUI() {
    document.getElementById("shopCoinText").innerText = "Số xu hiện có: 🪙 " + walletCoins;
    document.getElementById("owned1").innerText = ownedSkills[1];
    document.getElementById("owned2").innerText = ownedSkills[2];

    let nameMap = { 1: "🌪️ Gió Quét", 2: "🛡️ Bất Tử" };
    document.getElementById("eq1Text").innerText = equippedSlots[1] ? nameMap[equippedSlots[1]] : "Trống";
    document.getElementById("eq2Text").innerText = equippedSlots[2] ? nameMap[equippedSlots[2]] : "Trống";
}

function buySkill(type) {
    let cost = type === 1 ? 5 : 7;
    if (walletCoins >= cost) {
        walletCoins -= cost;
        ownedSkills[type]++;
        playSoundEffect('coin');
        updateShopUI();
    }
}

function equipSkill(type) {
    if (ownedSkills[type] <= 0) return;

    // Kiểm tra nếu đã trang bị rồi
    if (equippedSlots[1] === type || equippedSlots[2] === type) return;

    if (!equippedSlots[1]) {
        equippedSlots[1] = type;
    } else if (!equippedSlots[2]) {
        equippedSlots[2] = type;
    } else {
        // Đầy ô thì đổi Ô 1
        equippedSlots[1] = type;
    }
    updateShopUI();
}

function updateHUDButtons() {
    let nameMap = { 1: "🌪️ Gió Quét", 2: "🛡️ Bất Tử" };
    
    [1, 2].forEach(slot => {
        let btn = document.getElementById(`slot${slot}Btn`);
        let keyChar = slot === 1 ? "Q" : "E";
        let skillType = equippedSlots[slot];

        if (!skillType) {
            btn.innerText = `[${keyChar}] Trống`;
            btn.disabled = true;
        } else if (cooldowns[slot] > 0) {
            let secLeft = Math.ceil(cooldowns[slot] / 60);
            btn.innerText = `[${keyChar}] Hồi: ${secLeft}s`;
            btn.disabled = true;
        } else {
            let count = ownedSkills[skillType];
            btn.innerText = `[${keyChar}] ${nameMap[skillType]} (${count})`;
            btn.disabled = count <= 0;
        }
    });
}

function useSkill(slot) {
    if (!isPlaying) return;
    let skillType = equippedSlots[slot];

    if (skillType && cooldowns[slot] <= 0 && ownedSkills[skillType] > 0) {
        ownedSkills[skillType]--;
        cooldowns[slot] = 300; // 5 giây hồi chiêu (60 fps * 5s)

        if (skillType === 1) {
            isWindActive = true;
            windTimer = 180; // Tác dụng 3s
        } else if (skillType === 2) {
            isShieldActive = true;
            shieldTimer = 300; // Tác dụng 5s
        }

        playSoundEffect('skill');
        updateHUDButtons();
    }
}

document.addEventListener("keydown", e => {
    keys[e.key] = true;
    if (e.key === 'q' || e.key === 'Q') useSkill(1);
    if (e.key === 'e' || e.key === 'E') useSkill(2);
});
document.addEventListener("keyup", e => keys[e.key] = false);

function startGame() {
    initAudio();
    if (audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume();
    }

    isPlaying = true;
    score = 0;
    sessionCoins = 0;
    gameSpeed = 4.5;
    obstacles = [];
    coins = [];
    player.x = 180;

    cooldowns = { 1: 0, 2: 0 };
    isWindActive = false;
    isShieldActive = false;

    overlay.style.display = "none";
    updateHUDButtons();

    startPhonkMusic();
    animate();
}

function gameOver() {
    isPlaying = false;
    stopPhonkMusic();
    playSoundEffect('crash');
    cancelAnimationFrame(animationId);

    walletCoins += sessionCoins; // Cộng xu trận vào ví

    overlay.style.display = "flex";
    document.getElementById("title").innerText = "GAME OVER";
    updateShopUI();
}

function spawnEntities() {
    let lanes = [50, 140, 230, 320];

    // Vật cản
    if (Math.random() < 0.035) {
        let lane = lanes[Math.floor(Math.random() * lanes.length)];
        obstacles.push({
            x: lane, y: -60, width: 40, height: 60,
            color: Math.random() > 0.5 ? '#ff0055' : '#00f3ff'
        });
    }

    // Xu Vàng
    if (Math.random() < 0.025) {
        let lane = lanes[Math.floor(Math.random() * lanes.length)] + 10;
        coins.push({ x: lane, y: -30, radius: 12 });
    }
}

function update() {
    if ((keys["ArrowLeft"] || keys["a"] || keys["A"]) && player.x > 20) {
        player.x -= player.speed;
    }
    if ((keys["ArrowRight"] || keys["d"] || keys["D"]) && player.x < canvas.width - player.width - 20) {
        player.x += player.speed;
    }

    score += 0.1;
    gameSpeed += 0.0012;
    document.getElementById("scoreText").innerText = "SCORE: " + Math.floor(score);
    document.getElementById("coinText").innerText = "🪙 " + sessionCoins;

    // Giảm thời gian tác dụng kĩ năng
    if (isWindActive) {
        windTimer--;
        if (windTimer <= 0) isWindActive = false;
    }
    if (isShieldActive) {
        shieldTimer--;
        if (shieldTimer <= 0) isShieldActive = false;
    }

    // Đếm ngược thời gian hồi chiêu 5s
    [1, 2].forEach(slot => {
        if (cooldowns[slot] > 0) {
            cooldowns[slot]--;
        }
    });
    updateHUDButtons();

    spawnEntities();

    // Nhặt Xu
    for (let i = coins.length - 1; i >= 0; i--) {
        let c = coins[i];
        c.y += gameSpeed;
        if (
            player.x < c.x + c.radius &&
            player.x + player.width > c.x - c.radius &&
            player.y < c.y + c.radius &&
            player.y + player.height > c.y - c.radius
        ) {
            sessionCoins++;
            playSoundEffect('coin');
            coins.splice(i, 1);
            continue;
        }
        if (c.y > canvas.height) coins.splice(i, 1);
    }

    // Cập nhật vật cản
    for (let i = obstacles.length - 1; i >= 0; i--) {
        let obs = obstacles[i];
        obs.y += gameSpeed;

        let hit = (
            player.x < obs.x + obs.width &&
            player.x + player.width > obs.x &&
            player.y < obs.y + obs.height &&
            player.y + player.height > obs.y
        );

        if (hit) {
            if (isWindActive || isShieldActive) {
                obstacles.splice(i, 1);
                continue;
            } else {
                gameOver();
                return;
            }
        }
        if (obs.y > canvas.height) obstacles.splice(i, 1);
    }
}

function drawBackground() {
    ctx.strokeStyle = "rgba(255, 0, 85, 0.15)";
    ctx.lineWidth = 2;
    for (let x = 0; x < canvas.width; x += 40) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBackground();

    // Vẽ Xu Vàng 🪙
    coins.forEach(c => {
        ctx.shadowBlur = 12;
        ctx.shadowColor = "#ffe600";
        ctx.fillStyle = "#ffe600";
        ctx.beginPath();
        ctx.arc(c.x, c.y, c.radius, 0, Math.PI * 2);
        ctx.fill();
    });

    // Vẽ xe
    ctx.shadowBlur = 18;
    if (isShieldActive) {
        ctx.shadowColor = "#00f3ff";
        ctx.fillStyle = "#00f3ff";
    } else if (isWindActive) {
        ctx.shadowColor = "#a600ff";
        ctx.fillStyle = "#a600ff";
    } else {
        ctx.shadowColor = "#ff0055";
        ctx.fillStyle = "#ff0055";
    }
    ctx.fillRect(player.x, player.y, player.width, player.height);

    if (isShieldActive || isWindActive) {
        ctx.strokeStyle = isShieldActive ? "#00f3ff" : "#a600ff";
        ctx.lineWidth = 4;
        ctx.strokeRect(player.x - 6, player.y - 6, player.width + 12, player.height + 12);
    }

    // Đuôi lửa
    ctx.fillStyle = "#00f3ff";
    ctx.fillRect(player.x + 12, player.y + player.height, 16, 12 + Math.random() * 8);

    // Vật cản
    obstacles.forEach(obs => {
        ctx.shadowBlur = 15;
        ctx.shadowColor = obs.color;
        ctx.fillStyle = obs.color;
        ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
    });

    ctx.shadowBlur = 0;
}

function animate() {
    if (!isPlaying) return;
    update();
    draw();
    animationId = requestAnimationFrame(animate);
}

// Khởi tạo giao diện Cửa Hàng ban đầu
updateShopUI();
</script>
</body>
</html>
"""

components.html(game_code, height=600)
