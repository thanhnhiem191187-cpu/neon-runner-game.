import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Neon Cyber-Runner - Phonk Edition",
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
st.caption("Dùng phím mũi tên **Trái (←)** và **Phải (→)** hoặc **A / D** để quái xế né vật cản!")

# Mã HTML + JavaScript của Game với bộ tạo nhạc PHONK (Cowbell + Bass 808)
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
        background: rgba(8, 0, 16, 0.88);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: #fff;
    }
    .btn {
        background: #ff0055;
        color: #fff;
        border: none;
        padding: 14px 32px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 25px;
        cursor: pointer;
        box-shadow: 0 0 20px #ff0055;
        transition: 0.2s;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .btn:hover {
        transform: scale(1.08);
        box-shadow: 0 0 30px #ff0055;
        background: #00f3ff;
        color: #000;
    }
</style>
</head>
<body>

<div id="gameContainer">
    <canvas id="gameCanvas" width="400" height="550"></canvas>
    <div id="overlay">
        <h2 id="title" style="color: #ff0055; text-shadow: 0 0 15px #ff0055; font-size: 28px;">PHONK RUNNER</h2>
        <p id="scoreText" style="font-size: 18px; display: none; margin-bottom: 20px;"></p>
        <button class="btn" onclick="startGame()">BẮT ĐẦU CHƠI</button>
    </div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const overlay = document.getElementById("overlay");
const scoreText = document.getElementById("scoreText");

let player = { x: 180, y: 450, width: 40, height: 60, speed: 6.5 };
let obstacles = [];
let score = 0;
let gameSpeed = 4.5;
let isPlaying = false;
let animationId;
let keys = {};

// --- TRÌNH TẠO NHẠC PHONK (WEB AUDIO API) ---
let audioCtx = null;
let phonkTimer = null;
let step = 0;

function initAudio() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
}

// Âm thanh Cowbell đặc trưng của Phonk
function playCowbell(freq, time) {
    if (!audioCtx) return;
    let osc1 = audioCtx.createOscillator();
    let osc2 = audioCtx.createOscillator();
    let gain = audioCtx.createGain();

    osc1.type = 'square';
    osc2.type = 'square';

    osc1.frequency.setValueAtTime(freq, time);
    osc2.frequency.setValueAtTime(freq * 1.48, time); // Âm sắc Cowbell

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

// Tiếng Bass 808 xốc nhịp
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

// Vòng lặp giai điệu Phonk
function startPhonkMusic() {
    if (phonkTimer) clearInterval(phonkTimer);
    
    // Giai điệu Cowbell Phonk sôi động
    const notes = [587.33, 587.33, 783.99, 659.25, 587.33, 523.25, 587.33, 440.00];
    const bassNotes = [110, 110, 146.83, 130.81];

    step = 0;
    phonkTimer = setInterval(() => {
        if (!isPlaying || !audioCtx) return;
        let now = audioCtx.currentTime;

        // Phát Cowbell
        let note = notes[step % notes.length];
        playCowbell(note, now);

        // Phát Bass 808 dồn dập
        if (step % 2 === 0) {
            let bNote = bassNotes[Math.floor(step / 2) % bassNotes.length];
            playBass808(bNote, now);
        }

        step++;
    }, 140); // Nhịp độ nhanh (BPM cao)
}

function stopPhonkMusic() {
    if (phonkTimer) clearInterval(phonkTimer);
}

function playCrashSound() {
    if (!audioCtx) return;
    let osc = audioCtx.createOscillator();
    let gain = audioCtx.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(200, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(20, audioCtx.currentTime + 0.5);
    gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
    gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.5);
}
// ----------------------------------------

document.addEventListener("keydown", e => keys[e.key] = true);
document.addEventListener("keyup", e => keys[e.key] = false);

function startGame() {
    initAudio();
    if (audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume();
    }

    isPlaying = true;
    score = 0;
    gameSpeed = 4.5;
    obstacles = [];
    player.x = 180;
    overlay.style.display = "none";

    startPhonkMusic();
    animate();
}

function gameOver() {
    isPlaying = false;
    stopPhonkMusic();
    playCrashSound();
    cancelAnimationFrame(animationId);

    overlay.style.display = "flex";
    document.getElementById("title").innerText = "GAME OVER";
    scoreText.innerText = "Điểm của bạn: " + Math.floor(score);
    scoreText.style.display = "block";
}

function spawnObstacle() {
    if (Math.random() < 0.035) {
        let lanes = [50, 140, 230, 320];
        let lane = lanes[Math.floor(Math.random() * lanes.length)];
        obstacles.push({
            x: lane,
            y: -60,
            width: 40,
            height: 60,
            color: Math.random() > 0.5 ? '#ff0055' : '#00f3ff'
        });
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

function update() {
    if ((keys["ArrowLeft"] || keys["a"] || keys["A"]) && player.x > 20) {
        player.x -= player.speed;
    }
    if ((keys["ArrowRight"] || keys["d"] || keys["D"]) && player.x < canvas.width - player.width - 20) {
        player.x += player.speed;
    }

    score += 0.1;
    gameSpeed += 0.0012;
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

    // Xe người chơi
    ctx.shadowBlur = 18;
    ctx.shadowColor = "#ff0055";
    ctx.fillStyle = "#ff0055";
    ctx.fillRect(player.x, player.y, player.width, player.height);

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

    // Điểm số
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
