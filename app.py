import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Neon Cyber-Runner",
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
        text-shadow: 0 0 10px #00f3ff, 0 0 20px #00f3ff;
    }
    .stApp {
        background: radial-gradient(circle, #1a0033 0%, #050010 100%);
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ NEON CYBER-RUNNER ⚡")
st.caption("Dùng phím mũi tên **Trái (←)** và **Phải (→)** hoặc phím **A / D** để điều khiển xe né vật cản! (Có âm thanh sống động)")

# Mã HTML + JavaScript của Game kèm Web Audio API tạo nhạc & hiệu ứng
game_code = """
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
        box-shadow: 0 0 30px #ff007f;
        border-radius: 12px;
        overflow: hidden;
        border: 2px solid #ff007f;
    }
    canvas {
        background: #080014;
        display: block;
    }
    #overlay {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(8, 0, 20, 0.85);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: #fff;
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
        box-shadow: 0 0 15px #00f3ff;
        transition: 0.2s;
    }
    .btn:hover {
        transform: scale(1.08);
        box-shadow: 0 0 25px #00f3ff;
    }
</style>
</head>
<body>

<div id="gameContainer">
    <canvas id="gameCanvas" width="400" height="550"></canvas>
    <div id="overlay">
        <h2 id="title" style="color: #ff007f; text-shadow: 0 0 10px #ff007f;">NEON RUNNER</h2>
        <p id="scoreText" style="font-size: 18px; display: none;"></p>
        <button class="btn" onclick="startGame()">BẮT ĐẦU CHƠI</button>
    </div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const overlay = document.getElementById("overlay");
const scoreText = document.getElementById("scoreText");

let player = { x: 180, y: 450, width: 40, height: 60, speed: 6 };
let obstacles = [];
let score = 0;
let gameSpeed = 4;
let isPlaying = false;
let animationId;
let keys = {};

// --- HỆ THỐNG ÂM THANH (WEB AUDIO API) ---
let audioCtx = null;
let musicInterval = null;

function initAudio() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
}

// Hiệu ứng tiếng bấm nút / va chạm
function playSound(type) {
    if (!audioCtx) return;
    let osc = audioCtx.createOscillator();
    let gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);

    let now = audioCtx.currentTime;
    if (type === 'start') {
        osc.frequency.setValueAtChoice = 300;
        osc.frequency.exponentialRampToValueAtTime(800, now + 0.2);
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.2);
        osc.start(now);
        osc.stop(now + 0.2);
    } else if (type === 'hit') {
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(150, now);
        osc.frequency.linearRampToValueAtTime(40, now + 0.4);
        gain.gain.setValueAtTime(0.5, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.4);
        osc.start(now);
        osc.stop(now + 0.4);
    }
}

// Nhạc nền Cyberpunk tự động phát lặp lại
function startCyberMusic() {
    if (musicInterval) clearInterval(musicInterval);
    let notes = [110, 130.81, 146.83, 164.81, 196.00]; // Âm giai huyền bí
    musicInterval = setInterval(() => {
        if (!isPlaying || !audioCtx) return;
        let osc = audioCtx.createOscillator();
        let gain = audioCtx.createGain();
        osc.type = 'triangle';
        let note = notes[Math.floor(Math.random() * notes.length)];
        osc.frequency.setValueAtTime(note, audioCtx.currentTime);
        
        gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
        
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.15);
    }, 180);
}

function stopCyberMusic() {
    if (musicInterval) clearInterval(musicInterval);
}
// ----------------------------------------

document.addEventListener("keydown", e => keys[e.key] = true);
document.addEventListener("keyup", e => keys[e.key] = false);

function startGame() {
    initAudio();
    if (audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume();
    }
    
    playSound('start');
    isPlaying = true;
    score = 0;
    gameSpeed = 4;
    obstacles = [];
    player.x = 180;
    overlay.style.display = "none";
    
    startCyberMusic();
    animate();
}

function gameOver() {
    isPlaying = false;
    stopCyberMusic();
    playSound('hit');
    cancelAnimationFrame(animationId);
    
    overlay.style.display = "flex";
    document.getElementById("title").innerText = "GAME OVER";
    scoreText.innerText = "Điểm của bạn: " + Math.floor(score);
    scoreText.style.display = "block";
}

function spawnObstacle() {
    if (Math.random() < 0.03) {
        let lanes = [50, 140, 230, 320];
        let lane = lanes[Math.floor(Math.random() * lanes.length)];
        obstacles.push({
            x: lane,
            y: -60,
            width: 40,
            height: 60,
            color: Math.random() > 0.5 ? '#ff007f' : '#ffe600'
        });
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

function update() {
    if ((keys["ArrowLeft"] || keys["a"] || keys["A"]) && player.x > 20) {
        player.x -= player.speed;
    }
    if ((keys["ArrowRight"] || keys["d"] || keys["D"]) && player.x < canvas.width - player.width - 20) {
        player.x += player.speed;
    }

    score += 0.1;
    gameSpeed += 0.001;
    spawnObstacle();

    for (let i = obstacles.length - 1; i >= 0; i--) {
        let obs = obstacles[i];
        obs.y += gameSpeed;

        if (
            player.x < obs.x + obs.width &&
            player.x + player.width > obs.x &&
            player.y < obs.y + obs.height &&
            player.y + player.height > obs.y
        ) {
            gameOver();
            return;
        }

        if (obs.y > canvas.height) {
            obstacles.splice(i, 1);
        }
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBackground();

    ctx.shadowBlur = 15;
    ctx.shadowColor = "#00f3ff";
    ctx.fillStyle = "#00f3ff";
    ctx.fillRect(player.x, player.y, player.width, player.height);

    ctx.fillStyle = "#ff007f";
    ctx.fillRect(player.x + 12, player.y + player.height, 16, 10 + Math.random() * 8);

    obstacles.forEach(obs => {
        ctx.shadowBlur = 15;
        ctx.shadowColor = obs.color;
        ctx.fillStyle = obs.color;
        ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
    });

    ctx.shadowBlur = 0;

    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 18px 'Courier New'";
    ctx.fillText("SCORE: " + Math.floor(score), 20, 35);
}

function animate() {
    if (!isPlaying) return;
    update();
    draw();
    animationId = requestAnimationFrame(animate);
}
</script>
</body>
</html>
"""

components.html(game_code, height=600)
