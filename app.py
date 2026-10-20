import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Neon Runner: Funk & Skill Shop",
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
        color: #ffe600;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-shadow: 0 0 10px #ffe600, 0 0 20px #ff0055;
    }
    .stApp {
        background: radial-gradient(circle, #2a0033 0%, #050010 100%);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔥 NEON RUNNER: FUNK EDITION 🔥")
st.caption("Né vật cản, nhặt **Xu Vàng 🪙**, mua **Kĩ Năng** và cháy cùng nhạc Funk!")

# Mã HTML + JavaScript của Game (Sử dụng r\"\"\" để tránh lỗi syntax)
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
        box-shadow: 0 0 35px #ffe600;
        border-radius: 12px;
        overflow: hidden;
        border: 2px solid #ffe600;
    }
    canvas {
        background: #080010;
        display: block;
    }
    #overlay {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(8, 0, 16, 0.9);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: #fff;
    }
    .btn {
        background: #ffe600;
        color: #000;
        border: none;
        padding: 12px 28px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 25px;
        cursor: pointer;
        box-shadow: 0 0 15px #ffe600;
        transition: 0.2s;
        text-transform: uppercase;
        margin-top: 10px;
    }
    .btn:hover {
        transform: scale(1.08);
        box-shadow: 0 0 25px #ff0055;
        background: #ff0055;
        color: #fff;
    }
    .shop-btn {
        background: #00f3ff;
        color: #000;
        border: none;
        padding: 8px 16px;
        font-size: 14px;
        font-weight: bold;
        border-radius: 15px;
        cursor: pointer;
        margin: 5px;
        box-shadow: 0 0 10px #00f3ff;
    }
    .shop-btn:disabled {
        background: #555;
        color: #888;
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
        bottom: 15px;
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

    <div id="skillBar">
        <button id="skill1Btn" class="shop-btn" onclick="activateSkill(1)" disabled>🌪️ Gió Quét [Q] (0/15)</button>
        <button id="skill2Btn" class="shop-btn" onclick="activateSkill(2)" disabled>🛡️ Miễn Khống [E] (0/20)</button>
    </div>

    <div id="overlay">
        <h2 id="title" style="color: #ffe600; text-shadow: 0 0 15px #ffe600; font-size: 28px;">FUNK RUNNER</h2>
        <p id="finalScore" style="font-size: 18px; display: none; margin-bottom: 10px;"></p>
        
        <div style="border: 1px solid #ffe600; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px; background: rgba(255,230,0,0.1);">
            <h3 style="margin:0 0 10px 0; color: #00f3ff;">🛒 CỬA HÀNG KĨ NĂNG</h3>
            <p style="font-size: 13px; margin: 4px;">🌪️ <b>Gió Quét Xuyên Không</b>: Mua 15 Xu (Phím Q)</p>
            <p style="font-size: 13px; margin: 4px;">🛡️ <b>Miễn Khống / Bất Tử</b>: Mua 20 Xu (Phím E)</p>
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
let totalCoins = 0;
let gameSpeed = 4.5;
let isPlaying = false;
let animationId;
let keys = {};

let skill1Owned = 0;
let skill2Owned = 0;
let isWindActive = false;
let isShieldActive = false;
let windTimer = 0;
let shieldTimer = 0;

let audioCtx = null;
let funkTimer = null;
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
    osc2.frequency.setValueAtTime(freq * 1.5, time);

    gain.gain.setValueAtTime(0.12, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.15);

    osc1.connect(gain);
    osc2.connect(gain);
    gain.connect(audioCtx.destination);

    osc1.start(time);
    osc2.start(time);
    osc1.stop(time + 0.15);
    osc2.stop(time + 0.15);
}

function playFunkBass(freq, time) {
    if (!audioCtx) return;
    let osc = audioCtx.createOscillator();
    let gain = audioCtx.createGain();

    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(freq, time);
    osc.frequency.exponentialRampToValueAtTime(freq * 0.5, time + 0.2);

    gain.gain.setValueAtTime(0.3, time);
    gain.gain.linearRampToValueAtTime(0.01, time + 0.2);

    osc.connect(gain);
    gain.connect(audioCtx.destination);

    osc.start(time);
    osc.stop(time + 0.2);
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
