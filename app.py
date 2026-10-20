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
let is
components.html(game_code, height=600)
