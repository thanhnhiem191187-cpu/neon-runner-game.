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

        <button class="btn" onclick="startGame
