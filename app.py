
import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Neon Cyber-Runner - Shield Edition",
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
        color: #00f3ff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-shadow: 0 0 10px #00f3ff, 0 0 20px #ff0055;
    }
    .stApp {
        background: radial-gradient(circle, #1a0022 0%, #050010 100%);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔥 NEON RUNNER: SHIELD EDITION 🔥")
st.caption("Thu thập **Xu Vàng 🪙**, mua **Bất Tử 3s (Có Khiên Chắn)**, Hồi chiêu **5s** & Quẩy nhạc Phonk!")

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
        box-shadow: 0 0 35px #00f3ff;
        border-radius: 12px;
        overflow: hidden;
        border: 2px solid #00f3ff;
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
        background: #00f3ff;
        color: #000;
        border: none;
        padding: 12px 28px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 25px;
        cursor: pointer;
        box-shadow: 0 0 20px #00f3ff;
        transition: 0.2s;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 10px;
    }
    .btn:hover {
        transform: scale(1.08);
        box-shadow: 0 0 30px #00f3ff;
        background: #ff0055;
        color: #fff;
    }
    .shop-card {
        border: 1px solid #00f3ff;
        background: rgba(0, 243, 255, 0.1);
        border-radius: 10px;
        padding: 12px;
        width: 85%;
        text-align: center;
        margin-bottom: 10px;
    }
    .shop-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 6px 0;
        font-size: 14px;
    }
    .action-btn {
        background: #ffe600;
        color: #000;
        border: none;
        padding: 5px 12px;
        font-size: 12px;
        font-weight: bold;
        border-radius: 12px;
        cursor: pointer;
        margin-left: 4px;
    }
    .action-btn:disabled {
        background: #444;
        color: #888;
        cursor: not-allowed;
    }
    .hud-skill-btn {
        background: #00f3ff;
        color: #000;
        border: none;
        padding: 8px 16px;
        font-size: 13px;
        font-weight: bold;
        border-radius: 15px;
        cursor: pointer;
        box-shadow: 0 0 12px #00f3ff;
        min-width: 150px;
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
        justify-content: center;
        width: 100%;
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

    <!-- Thanh kĩ năng Bất tử -->
    <div id="skillBar">
        <button id="shieldBtn" class="hud-skill-btn" onclick="useShieldSkill()" disabled>[Q/E] Bất Tử: Trống</button>
    </div>

    <div id="overlay">
        <h2 id="title" style="color: #00f3ff; text-shadow: 0 0 15px #00f3ff; font-size: 26px; margin: 5px 0;">CỬA HÀNG KĨ NĂNG</h2>
        <div style="color: #ffe600; font-weight: bold; margin-bottom: 12px;" id="shopCoinText">Số xu hiện có: 🪙 0</div>

        <div class="shop-card">
            <div class="shop-item">
                <span>🛡️ <b>Bất Tử 3s</b> (7 Xu) - Sở hữu: <b id="ownedShieldCount">0</b></span>
                <div>
                    <button class="action-btn" onclick="buyShield()">Mua</button>
                    <button class="action-btn" onclick="equipShield()">Trang bị</button>
                </div>
            </div>
        </div>

        <div style="font-size: 13px; color: #00f3ff; margin-bottom: 12px;">
            Trạng thái: <span id="equipStatusText" style="color: #ff0055; font-weight: bold;">Chưa trang bị</span>
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

// Quản lý kĩ năng Bất tử
let shieldOwned = 0;
let isShieldEquipped = false;
let shieldCooldown = 0; // Đếm ngược hồi chiêu (5s = 300 frames)
let isShieldActive = false;
let shieldTimer = 0; // Tác dụng 3s = 180 frames

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
    } else if (type === 'shield') {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(300, now);
        osc.frequency.exponentialRampToValueAtTime(900, now + 0.35);
        gain.gain.setValueAtTime(0.35, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.35);
        osc.start(now);
        osc.stop(now + 0.35);
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

// Cửa hàng
function updateShopUI() {
    document.getElementById("shopCoinText").innerText = "Số xu hiện có: 🪙 " + walletCoins;
    document.getElementById("ownedShieldCount").innerText = shieldOwned;
    let status = document.getElementById("equipStatusText");
    if (isShieldEquipped) {
        status.innerText = "Đã trang bị 🛡️ Bất Tử";
        status.style.color = "#00f3ff";
    } else {
        status.innerText = "Chưa trang bị";
        status.style.color = "#ff0055";
    }
}

function buyShield() {
    if (walletCoins >= 7) {
        walletCoins -= 7;
        shieldOwned++;
        playSoundEffect('coin');
        updateShopUI();
    }
}

function equipShield() {
    if (shieldOwned > 0) {
        isShieldEquipped = true;
        updateShopUI();
    }
}

function updateHUDButton() {
    let btn = document.getElementById("shieldBtn");
    if (!isShieldEquipped) {
        btn.innerText = "[Q/E] Bất Tử: Trống";
        btn.disabled = true;
    } else if (shieldCooldown > 0) {
        let secLeft = Math.ceil(shieldCooldown / 60);
        btn.innerText = `🛡️ Hồi chiêu: ${secLeft}s`;
        btn.disabled = true;
    } else {
        btn.innerText = `🛡️ Bất Tử [Q/E] (${shieldOwned})`;
        btn.disabled = shieldOwned <= 0;
    }
}

function useShieldSkill() {
    if (!isPlaying) return;

    if (isShieldEquipped && shieldCooldown <= 0 && shieldOwned > 0) {
        shieldOwned--;
        shieldCooldown = 300; // 5 giây hồi chiêu
        isShieldActive = true;
        shieldTimer = 180; // 3 giây tác dụng

        playSoundEffect('shield');
        updateHUDButton();
    }
}

document.addEventListener("keydown", e => {
    keys[e.key] = true;
    if (e.key === 'q' || e.key === 'Q' || e.key === 'e' || e.key === 'E' || e.key === ' ') {
        useShieldSkill();
    }
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

    shieldCooldown = 0;
    isShieldActive = false;

    overlay.style.display = "none";
    updateHUDButton();

    startPhonkMusic();
    animate();
}

function gameOver() {
    isPlaying = false;
    stopPhonkMusic();
    playSoundEffect('crash');
    cancelAnimationFrame(animationId);

    walletCoins += sessionCoins; // Cộng xu trận vào tài khoản
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
            color: Math.random() > 0.5 ? '#ff0055' : '#ffe600'
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
    if (isShieldActive) {
        shieldTimer--;
        if (shieldTimer <= 0) isShieldActive = false;
    }

    // Giảm thời gian hồi chiêu
    if (shieldCooldown > 0) {
        shieldCooldown--;
    }
    updateHUDButton();

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
            if (isShieldActive) {
                // Bất tử: Dọn dẹp vật cản
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
    ctx.strokeStyle = "rgba(0, 243, 255, 0.15)";
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

    // Vẽ Xe người chơi
    ctx.shadowBlur = 18;
    ctx.shadowColor = isShieldActive ? "#00f3ff" : "#ff0055";
    ctx.fillStyle = isShieldActive ? "#00f3ff" : "#ff0055";
    ctx.fillRect(player.x, player.y, player.width, player.height);

    // HIỆU ỨNG KIÊN CHẮN NEON KHI BẬT BẤT TỬ 🛡️
    if (isShieldActive) {
        let centerX = player.x + player.width / 2;
        let centerY = player.y + player.height / 2;

        // Vòng khiên bảo vệ phát sáng bên ngoài
        ctx.save();
        ctx.shadowBlur = 25;
        ctx.shadowColor = "#00f3ff";
        ctx.strokeStyle = "rgba(0, 243, 255, 0.85)";
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.arc(centerX, centerY, 45, 0, Math.PI * 2);
        ctx.stroke();

        // Màng năng lượng bên trong khiên
        ctx.fillStyle = "rgba(0, 243, 255, 0.2)";
        ctx.fill();
        ctx.restore();
    }

    // Đuôi lửa xe
    ctx.fillStyle = "#00f3ff";
    ctx.fillRect(player.x + 12, player.y + player.height, 16, 12 + Math.random() * 8);

    // Vẽ Vật cản
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

// Cập nhật giao diện cửa hàng ban đầu
updateShopUI();
</script>
</body>
</html>
"""

components.html(game_code, height=600)
