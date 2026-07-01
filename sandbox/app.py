# sandbox/app.py

import os
import gradio as gr
import pandas as pd
import json
import re
import base64
from pathlib import Path

CSV_PATH = Path(os.getenv("CSV_PATH", "HireSense_AI.csv"))
LOGO_PATH = Path("Golden_Heart_AI.jpg")


def get_logo_base64() -> str:
    try:
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        return ""


LOGO_B64 = get_logo_base64()

HOLOGRAPHIC_CSS = """
:root {
    --holo-primary: #00d4ff;
    --holo-secondary: #7b2ff7;
    --holo-accent: #00ff88;
    --holo-gold: #ffd700;
    --holo-bg: #020818;
    --holo-surface: #0a1628;
}
.gradio-container {
    background: var(--holo-bg) !important;
    background-image:
        radial-gradient(ellipse at 20% 50%, rgba(123,47,247,0.08) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(0,212,255,0.06) 0%, transparent 60%),
        radial-gradient(ellipse at 50% 80%, rgba(0,255,136,0.04) 0%, transparent 60%) !important;
    min-height: 100vh;
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
}
.hiresense-header {
    text-align: center;
    padding: 40px 20px 20px;
    position: relative;
    overflow: hidden;
}
.hiresense-title {
    font-size: clamp(2rem, 6vw, 3.5rem);
    font-weight: 900;
    background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 35%, #00ff88 65%, #ffd700 100%);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: holoShift 4s ease infinite;
    letter-spacing: -2px;
    margin: 0;
    line-height: 1.1;
}
@keyframes holoShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.hiresense-subtitle {
    color: rgba(0,212,255,0.9) !important;
    font-size: 1.1rem;
    margin-top: 8px;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-weight: 300;
}
.hiresense-tagline {
    color: rgba(180,130,255,0.9) !important;
    font-size: 0.85rem;
    margin-top: 4px;
    letter-spacing: 1px;
}
.scan-line {
    height: 2px;
    background: linear-gradient(90deg, transparent 0%, #00d4ff 50%, transparent 100%);
    animation: scan 3s ease-in-out infinite;
    margin: 16px auto;
    width: 60%;
    border-radius: 2px;
    box-shadow: 0 0 10px rgba(0,212,255,0.8);
}
@keyframes scan {
    0% { transform: scaleX(0.3); opacity: 0.4; }
    50% { transform: scaleX(1.0); opacity: 1.0; }
    100% { transform: scaleX(0.3); opacity: 0.4; }
}
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    padding: 20px 0;
}
.stat-card {
    background: linear-gradient(135deg, rgba(0,212,255,0.12) 0%, rgba(123,47,247,0.12) 100%) !important;
    border: 1px solid rgba(0,212,255,0.35) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    text-align: center !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.2) !important;
    backdrop-filter: blur(10px) !important;
}
.stat-card:hover {
    border-color: rgba(0,212,255,0.8) !important;
    box-shadow: 0 0 40px rgba(0,212,255,0.4) !important;
    transform: translateY(-4px) !important;
}
.stat-number {
    font-size: 2.8rem !important;
    font-weight: 900 !important;
    color: #00d4ff !important;
    text-shadow: 0 0 20px rgba(0,212,255,0.8) !important;
    line-height: 1 !important;
    display: block !important;
}
.stat-label {
    color: #ffffff !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    margin-top: 8px !important;
    font-weight: 600 !important;
    display: block !important;
    opacity: 1 !important;
    text-shadow: 0 0 8px rgba(0,212,255,0.5) !important;
}
.ranking-scroll .table-wrap,
.ranking-scroll .gr-samples-table,
.ranking-scroll [data-testid="dataframe"] > div {
    max-height: 520px !important;
    overflow-y: auto !important;
    overflow-x: auto !important;
}
.ranking-scroll [data-testid="dataframe"] > div::-webkit-scrollbar {
    width: 6px !important;
    height: 6px !important;
}
.ranking-scroll [data-testid="dataframe"] > div::-webkit-scrollbar-track {
    background: rgba(0,212,255,0.05) !important;
}
.ranking-scroll [data-testid="dataframe"] > div::-webkit-scrollbar-thumb {
    background: rgba(0,212,255,0.4) !important;
    border-radius: 3px !important;
}
.dataframe {
    background: var(--holo-surface) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    width: 100% !important;
}
.dataframe thead th {
    background: linear-gradient(135deg, rgba(0,212,255,0.2), rgba(123,47,247,0.2)) !important;
    color: #00d4ff !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    border-bottom: 1px solid rgba(0,212,255,0.3) !important;
    padding: 14px !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 10 !important;
}
.dataframe tbody tr {
    border-bottom: 1px solid rgba(0,212,255,0.06) !important;
    transition: background 0.2s ease !important;
}
.dataframe tbody tr:hover {
    background: rgba(0,212,255,0.07) !important;
}
.dataframe tbody td {
    color: #ffffff !important;
    padding: 12px 14px !important;
    font-size: 0.9rem !important;
}
.gr-button-primary, button.primary {
    background: linear-gradient(135deg, #00d4ff, #7b2ff7) !important;
    border: none !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    border-radius: 10px !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.4) !important;
    transition: all 0.3s ease !important;
}
.gr-button-primary:hover, button.primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 30px rgba(0,212,255,0.7) !important;
}
input, textarea, select {
    background: rgba(10,22,40,0.9) !important;
    border: 1px solid rgba(0,212,255,0.3) !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
}
input:focus, textarea:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.4) !important;
    outline: none !important;
}
label, .gr-form label {
    color: rgba(0,212,255,0.9) !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
}
.tab-nav button {
    background: transparent !important;
    border: 1px solid rgba(0,212,255,0.2) !important;
    color: rgba(0,212,255,0.8) !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
    font-weight: 600 !important;
}
.tab-nav button.selected {
    background: linear-gradient(135deg, rgba(0,212,255,0.2), rgba(123,47,247,0.2)) !important;
    border-color: #00d4ff !important;
    color: #00d4ff !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.4) !important;
}
.pulse-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #00ff88;
    border-radius: 50%;
    margin-right: 8px;
    animation: pulseDot 2s ease infinite;
    box-shadow: 0 0 8px #00ff88;
    vertical-align: middle;
}
@keyframes pulseDot {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.4); opacity: 0.6; }
    100% { transform: scale(1); opacity: 1; }
}
.hiresense-footer {
    text-align: center;
    padding: 30px;
    color: rgba(0,212,255,0.5) !important;
    font-size: 0.8rem;
    letter-spacing: 2px;
    border-top: 1px solid rgba(0,212,255,0.08);
    margin-top: 40px;
    position: relative;
}
.holo-grid {
    background-image:
        linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
}
.gr-markdown p, .gr-markdown li,
.gr-markdown h1, .gr-markdown h2, .gr-markdown h3,
.gr-markdown td, .gr-markdown th {
    color: #ffffff !important;
}

/* ── Footer logo button fixed positioning ── */
#hs-footer-logo-btn {
    position: fixed !important;
    bottom: 20px !important;
    right: 20px !important;
    width: 52px !important;
    height: 52px !important;
    border-radius: 50% !important;
    overflow: hidden !important;
    cursor: pointer !important;
    border: 2px solid rgba(0,212,255,0.6) !important;
    box-shadow: 0 0 18px rgba(0,212,255,0.4) !important;
    transition: all 0.3s ease !important;
    background: #0a1628 !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    z-index: 9000 !important;
}
#hs-footer-logo-btn:hover {
    border-color: #00d4ff !important;
    box-shadow: 0 0 32px rgba(0,212,255,0.8) !important;
    transform: scale(1.12) !important;
}

/* ── Mobile text justification fix ── */
@media (max-width: 768px) {
    .gr-markdown p,
    .gr-markdown li,
    .gr-markdown td,
    .gr-markdown th {
        text-align: left !important;
        word-break: break-word !important;
    }
    .hiresense-subtitle {
        letter-spacing: 1px !important;
        font-size: 0.95rem !important;
    }
    .hiresense-tagline {
        font-size: 0.78rem !important;
        letter-spacing: 0.5px !important;
        word-break: break-word !important;
    }
    .stats-grid {
        grid-template-columns: repeat(2, 1fr) !important;
    }
    .stat-number {
        font-size: 2rem !important;
    }
    .stat-label {
        font-size: 0.65rem !important;
        letter-spacing: 1px !important;
    }
    .hiresense-footer {
        letter-spacing: 0.5px !important;
        font-size: 0.72rem !important;
        padding: 20px 10px 50px !important;
        text-align: left !important;
        word-break: break-word !important;
    }
    .dataframe tbody td,
    .dataframe thead th {
        font-size: 0.78rem !important;
        padding: 8px 8px !important;
    }
}
"""


def build_speech_head(logo_b64: str) -> str:
    favicon_tag = ""

    # ── Fallback when no logo ──
    modal_logo_html = (
        "<div style='display:flex;align-items:center;justify-content:center;"
        "width:100%;height:100%;background:#0a1628;color:#00d4ff;"
        "font-size:2rem;font-weight:900;'>HS</div>"
    )
    footer_logo_inner = (
        "<span style='display:flex;align-items:center;justify-content:center;"
        "width:100%;height:100%;color:#00d4ff;font-size:1.2rem;"
        "font-weight:900;'>HS</span>"
    )

    if logo_b64:
        favicon_tag = (
            '<link rel="icon" type="image/jpeg" '
            'href="data:image/jpeg;base64,' + logo_b64 + '">'
        )
        modal_logo_html = (
            '<img src="data:image/jpeg;base64,' + logo_b64 + '" '
            'alt="HireSense Logo" '
            'style="width:100%;height:100%;object-fit:contain;'
            'background:#0a1628;" />'
        )
        footer_logo_inner = (
            '<img src="data:image/jpeg;base64,' + logo_b64 + '" '
            'alt="Logo" '
            'style="width:100%;height:100%;object-fit:cover;'
            'display:block;border-radius:50%;" />'
        )

    # ── Style strings passed into JS template ──
    modal_overlay_style = (
        "display:none;position:fixed;inset:0;z-index:99998;"
        "background:rgba(2,8,24,0.92);backdrop-filter:blur(10px);"
        "align-items:center;justify-content:center;cursor:pointer;"
    )
    modal_box_style = (
        "width:380px;height:380px;border-radius:12px;overflow:hidden;"
        "border:2px solid rgba(0,212,255,0.6);"
        "box-shadow:0 0 60px rgba(0,212,255,0.5);"
        "cursor:default;background:#0a1628;"
        "animation:modalPop 0.3s ease;"
    )

    # ── Welcome overlay: WHITE background ──
    welcome_overlay_style = (
        "display:flex;position:fixed;inset:0;z-index:999999;"
        "background:rgba(255,255,255,0.97);backdrop-filter:blur(12px);"
        "align-items:center;justify-content:center;flex-direction:column;"
        "cursor:pointer;"
    )

    return (
        favicon_tag
        + """
<style>
@keyframes modalPop {
    0%   { transform: scale(0.7); opacity: 0; }
    100% { transform: scale(1.0); opacity: 1; }
}
#hs-logo-modal-overlay.active { display: flex !important; }

/* Welcome overlay animations */
@keyframes welcomeFadeIn {
    0%   { opacity: 0; transform: scale(0.92); }
    100% { opacity: 1; transform: scale(1); }
}
@keyframes welcomeFadeOut {
    0%   { opacity: 1; transform: scale(1); }
    100% { opacity: 0; transform: scale(1.04); pointer-events: none; }
}
#hs-welcome-overlay {
    animation: welcomeFadeIn 0.6s ease forwards;
}
#hs-welcome-overlay.dismissing {
    animation: welcomeFadeOut 0.5s ease forwards;
}
#hs-welcome-btn {
    margin-top: 36px;
    padding: 14px 44px;
    background: linear-gradient(135deg, #00d4ff, #7b2ff7);
    border: none;
    border-radius: 50px;
    color: #ffffff;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 2px;
    cursor: pointer;
    box-shadow: 0 0 30px rgba(0,212,255,0.4);
    transition: all 0.3s ease;
    text-transform: uppercase;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}
#hs-welcome-btn:hover {
    box-shadow: 0 0 50px rgba(0,212,255,0.7);
    transform: translateY(-2px) scale(1.04);
}
#hs-welcome-title {
    font-size: clamp(1.8rem, 5vw, 2.8rem);
    font-weight: 900;
    background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 40%, #00b894 70%, #e67e22 100%);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: holoShift 4s ease infinite;
    letter-spacing: -1px;
    text-align: center;
    margin: 0 0 8px 0;
}
#hs-welcome-sub {
    color: #5b6a8a;
    font-size: 0.9rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    text-align: center;
    margin: 0;
    font-family: 'Inter', 'Segoe UI', sans-serif;
    font-weight: 500;
}
#hs-welcome-hint {
    color: #8a7bb5;
    font-size: 0.78rem;
    letter-spacing: 1px;
    text-align: center;
    margin-top: 14px;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}
#hs-welcome-scan {
    height: 2px;
    width: 60%;
    max-width: 320px;
    background: linear-gradient(90deg, transparent 0%, #00d4ff 50%, transparent 100%);
    border-radius: 2px;
    box-shadow: 0 0 10px rgba(0,212,255,0.6);
    margin: 18px auto 0;
    animation: scan 3s ease-in-out infinite;
}
@media (max-width: 600px) {
    #hs-welcome-btn {
        padding: 12px 30px;
        font-size: 0.92rem;
        letter-spacing: 1px;
    }
    #hs-welcome-sub {
        letter-spacing: 1px;
        font-size: 0.78rem;
    }
}
</style>

<script>
(function () {
    var SESSION_KEY = 'hiresense_welcomed';

    /* ── Voice Engine ────────────────────────────────────────────────────── */
    var Voice = {
        synth: null,
        ready: false,
        voiceList: [],
        init: function () {
            if (!window.speechSynthesis) return;
            this.synth = window.speechSynthesis;
            var self = this;
            function loadVoices() {
                self.voiceList = self.synth.getVoices();
                if (self.voiceList.length > 0) { self.ready = true; }
            }
            loadVoices();
            if (this.synth.onvoiceschanged !== undefined) {
                this.synth.onvoiceschanged = function () { loadVoices(); };
            }
        },
        pickVoice: function () {
            var preferred = [
                'Google US English',
                'Microsoft David - English (United States)',
                'Microsoft Mark - English (United States)',
                'Microsoft Zira - English (United States)',
                'Alex', 'Samantha', 'Karen', 'Daniel', 'Moira', 'Tessa'
            ];
            for (var i = 0; i < preferred.length; i++) {
                for (var j = 0; j < this.voiceList.length; j++) {
                    if (this.voiceList[j].name === preferred[i]) {
                        return this.voiceList[j];
                    }
                }
            }
            for (var k = 0; k < this.voiceList.length; k++) {
                if (this.voiceList[k].lang && this.voiceList[k].lang.startsWith('en')) {
                    return this.voiceList[k];
                }
            }
            return this.voiceList[0] || null;
        },
        speak: function (text, rate, pitch, onEnd) {
            if (!this.synth) return;
            this.synth.cancel();
            var self = this;
            function doSpeak() {
                var utt = new SpeechSynthesisUtterance(text);
                utt.rate   = rate  || 0.88;
                utt.pitch  = pitch || 1.05;
                utt.volume = 1.0;
                var v = self.pickVoice();
                if (v) utt.voice = v;
                utt.onend = function () {
                    if (typeof onEnd === 'function') onEnd();
                };
                utt.onerror = function (e) {
                    if (e.error !== 'interrupted' && e.error !== 'canceled') {
                        console.warn('HireSenseVoice error:', e.error);
                    }
                };
                self.synth.speak(utt);
                var resumeTimer = setInterval(function () {
                    if (self.synth.speaking) { self.synth.resume(); }
                    else { clearInterval(resumeTimer); }
                }, 10000);
            }
            if (this.voiceList.length === 0) { setTimeout(doSpeak, 600); }
            else { doSpeak(); }
        },
        welcome: function () {
            if (sessionStorage.getItem(SESSION_KEY)) return;
            sessionStorage.setItem(SESSION_KEY, '1');
            this.speak(
                'HireSense AI. Intelligent Candidate Discovery and Ranking Platform.',
                0.88, 1.05
            );
        },
        announceTopN: function (n) {
            this.speak('Displaying top ' + n + ' ranked candidates.', 0.9, 1.05);
        }
    };

    Voice.init();
    window.HireSenseVoice = Voice;

    /* ── Welcome Overlay (WHITE background) ──────────────────────────────── */
    function createWelcomeOverlay() {
        if (sessionStorage.getItem(SESSION_KEY)) return;

        var overlay = document.createElement('div');
        overlay.id = 'hs-welcome-overlay';
        overlay.setAttribute('style', '""" + welcome_overlay_style + """');

        overlay.innerHTML = [
            '<div style="display:flex;flex-direction:column;align-items:center;',
            'padding:40px 28px;max-width:500px;width:92%;',
            'border-radius:20px;',
            'box-shadow:0 8px 40px rgba(0,212,255,0.15);',
            'background:rgba(255,255,255,0.6);',
            'backdrop-filter:blur(6px);">',
            '  <h1 id="hs-welcome-title">HireSense_AI</h1>',
            '  <p id="hs-welcome-sub">Intelligent Candidate Discovery &amp; Ranking</p>',
            '  <div id="hs-welcome-scan"></div>',
            '  <button id="hs-welcome-btn">&#9654;&nbsp; Enter Platform</button>',
            '  <p id="hs-welcome-hint">Tap to activate voice &amp; enter the platform</p>',
            '</div>'
        ].join('');

        document.body.appendChild(overlay);

        function dismiss() {
            overlay.classList.add('dismissing');
            setTimeout(function () {
                if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
                if (window.HireSenseVoice) {
                    window.HireSenseVoice.welcome();
                }
            }, 500);
        }

        var btn = overlay.querySelector('#hs-welcome-btn');
        if (btn) {
            btn.addEventListener('click', function (e) {
                e.stopPropagation();
                dismiss();
            });
        }
        overlay.addEventListener('click', function (e) {
            if (e.target === overlay) { dismiss(); }
        });
    }

    /* ── Logo Modal (SQUARE image popup) ─────────────────────────────────── */
    function setupLogoModal() {
        var modalOverlay = document.createElement('div');
        modalOverlay.id = 'hs-logo-modal-overlay';
        modalOverlay.setAttribute('style', '""" + modal_overlay_style + """');
        modalOverlay.innerHTML = (
            '<div id="hs-logo-modal-box" style=\"""" + modal_box_style + """\">' +
            '""" + modal_logo_html + """' +
            '</div>'
        );
        document.body.appendChild(modalOverlay);

        modalOverlay.addEventListener('click', function (e) {
            if (e.target === modalOverlay) {
                modalOverlay.classList.remove('active');
            }
        });

        /* ── Footer logo button injected directly into body (fixed position) */
        var logoBtn = document.createElement('button');
        logoBtn.id = 'hs-footer-logo-btn';
        logoBtn.title = 'HireSense AI — Click to view logo';
        logoBtn.innerHTML = '""" + footer_logo_inner + """';
        document.body.appendChild(logoBtn);

        logoBtn.addEventListener('click', function () {
            modalOverlay.classList.add('active');
        });
    }

    /* ── Boot ────────────────────────────────────────────────────────────── */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            createWelcomeOverlay();
            setupLogoModal();
        });
    } else {
        createWelcomeOverlay();
        setupLogoModal();
    }
})();
</script>
"""
    )


def build_footer_html(logo_b64: str) -> str:
    """
    Footer bar — the circular logo button is now injected directly
    into <body> via JS (fixed positioning), so we only render the
    text strip here.
    """
    return (
        '<div class="hiresense-footer" style="padding-right:80px;">'
        '<span class="pulse-dot"></span>'
        'HIRESENSE_AI &nbsp;|&nbsp; REDROB AI HACKATHON 2026 &nbsp;|&nbsp; PRODUCTION RANKING SYSTEM &nbsp;|&nbsp; BUILT BY SHAIK ARSHAD WASIB &nbsp;|&nbsp; SOLO PROJECT - TEAM LEADER '
        '</div>'
    )


HEADER_HTML = """
<div class="hiresense-header holo-grid">
    <h1 class="hiresense-title">HireSense_AI</h1>
    <p class="hiresense-subtitle">Intelligent Candidate Discovery &amp; Ranking</p>
    <p class="hiresense-tagline">
        Redrob AI Hackathon &nbsp;|&nbsp; BAAI/bge-small-en-v1.5 &nbsp;|&nbsp; 100K Candidate Dataset
    </p>
    <div class="scan-line"></div>
</div>
"""

JS_ON_LOAD = """
() => {
    setTimeout(function () {
        if (window.HireSenseVoice) {
            window.HireSenseVoice.welcome();
        }
    }, 1200);
}
"""


def load_csv_data() -> pd.DataFrame:
    try:
        return pd.read_csv(CSV_PATH)
    except Exception:
        return pd.DataFrame({
            "candidate_id": ["CAND_0039754"],
            "rank":         [1],
            "score":        [1.0],
            "reasoning":    ["Good Match, Senior Applied Scientist"],
        })


def parse_tier(reasoning: str) -> str:
    for tier in ["Elite Match", "Strong Match", "Good Match",
                 "Moderate Match", "Partial Match", "Weak Match"]:
        if str(reasoning).startswith(tier):
            return tier
    return "Unknown"


def parse_title(reasoning: str) -> str:
    try:
        parts = str(reasoning).split(", ")
        if len(parts) >= 2:
            return parts[1]
    except Exception:
        pass
    return "Unknown"


def parse_years(reasoning: str) -> str:
    m = re.search(r"(\d+\.?\d*)\s+yrs?\s+experience", str(reasoning))
    return f"{m.group(1)} yrs" if m else "N/A"


def get_stats_html(df: pd.DataFrame) -> str:
    total      = len(df)
    top_score  = float(df["score"].max())  if not df.empty else 0
    avg_score  = float(df["score"].mean()) if not df.empty else 0
    tier_counts: dict = {}
    for _, row in df.iterrows():
        t = parse_tier(str(row["reasoning"]))
        tier_counts[t] = tier_counts.get(t, 0) + 1
    good_match     = tier_counts.get("Good Match",     0)
    moderate_match = tier_counts.get("Moderate Match", 0)
    return f"""
<div class="stats-grid">
    <div class="stat-card">
        <span class="stat-number" style="color:#00d4ff !important;">{total}</span>
        <span class="stat-label"  style="color:#ffffff !important;">TOTAL RANKED</span>
    </div>
    <div class="stat-card">
        <span class="stat-number" style="color:#ffd700 !important;">{top_score:.3f}</span>
        <span class="stat-label"  style="color:#ffffff !important;">TOP SCORE</span>
    </div>
    <div class="stat-card">
        <span class="stat-number" style="color:#00ff88 !important;">{good_match}</span>
        <span class="stat-label"  style="color:#ffffff !important;">GOOD MATCH</span>
    </div>
    <div class="stat-card">
        <span class="stat-number" style="color:#7b2ff7 !important;">{moderate_match}</span>
        <span class="stat-label"  style="color:#ffffff !important;">MODERATE MATCH</span>
    </div>
</div>
<div style="text-align:center;color:rgba(0,212,255,0.7) !important;
     font-size:0.8rem;padding:8px;letter-spacing:2px;font-weight:600;">
    <span class="pulse-dot"></span>
    AVG SCORE: {avg_score:.4f} &nbsp;|&nbsp; MODEL: BAAI/bge-small-en-v1.5 &nbsp;|&nbsp; DATASET: 100K CANDIDATES
</div>
"""


def format_ranking_table(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    d = df.copy()
    d["Tier"]  = d["reasoning"].apply(parse_tier)
    d["Role"]  = d["reasoning"].apply(parse_title)
    d["Exp"]   = d["reasoning"].apply(parse_years)
    d["Score"] = d["score"].apply(lambda x: f"{float(x):.4f}")
    return d[["rank", "candidate_id", "Score", "Tier", "Role", "Exp"]].rename(
        columns={"rank": "Rank", "candidate_id": "Candidate ID"}
    )


def show_top_n(n: int) -> tuple:
    df      = load_csv_data()
    display = format_ranking_table(df.head(n))
    stats   = get_stats_html(df)
    return display, stats


def search_candidates(query: str) -> pd.DataFrame:
    df = load_csv_data()
    if not query or not query.strip():
        return format_ranking_table(df.head(20))
    q    = query.lower().strip()
    mask = (
        df["candidate_id"].str.lower().str.contains(q, na=False)
        | df["reasoning"].str.lower().str.contains(q, na=False)
    )
    results = df[mask]
    if len(results) == 0:
        return pd.DataFrame({"Message": [f"No candidates found for: '{query}'"]})
    return format_ranking_table(results)


def upload_and_rank(file) -> tuple:
    if file is None:
        return pd.DataFrame({"Message": ["Please upload a JSON file"]}), "No file uploaded."
    try:
        with open(file.name, "r", encoding="utf-8") as f:
            content = f.read().strip()
        candidates = []
        if content.startswith("["):
            candidates = json.loads(content)
        else:
            for line in content.split("\n"):
                line = line.strip()
                if line:
                    candidates.append(json.loads(line))
        if not candidates:
            return pd.DataFrame({"Message": ["Empty file"]}), "No candidates found in file."

        tech_keywords = {
            "machine learning", "deep learning", "nlp", "neural", "ai", "ml",
            "data science", "python", "tensorflow", "pytorch", "llm", "transformer",
            "bert", "gpt", "embedding", "recommendation", "computer vision", "mlops",
        }
        results = []
        for cand in candidates[:50]:
            cand_id      = cand.get("candidate_id", "Unknown")
            profile      = cand.get("profile", {})
            title        = profile.get("current_title", "Unknown")
            years        = profile.get("years_of_experience", 0)
            skills       = cand.get("skills", [])
            profile_text = (
                title.lower() + " "
                + profile.get("headline", "").lower() + " "
                + " ".join(s.get("name", "").lower() for s in skills)
            )
            tech_signals = sum(1 for kw in tech_keywords if kw in profile_text)
            status       = "✓ Would Pass Filter" if tech_signals >= 2 else "✗ Would Fail Filter"
            results.append({
                "Candidate ID": cand_id,
                "Title":        title,
                "Experience":   f"{years} yrs",
                "Skills":       len(skills),
                "Tech Signals": tech_signals,
                "Filter":       status,
            })

        result_df = pd.DataFrame(results)
        passed    = len(result_df[result_df["Filter"].str.startswith("✓")])
        failed    = len(result_df) - passed
        summary   = (
            f"Analyzed {len(results)} candidates. "
            f"✓ {passed} would pass domain filter. "
            f"✗ {failed} would be filtered out."
        )
        return result_df, summary

    except json.JSONDecodeError as e:
        return pd.DataFrame({"Error": [f"Invalid JSON: {e}"]}), "File parsing failed."
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]}), "Analysis failed."


def build_interface():
    SPEECH_HEAD = build_speech_head(LOGO_B64)
    FOOTER_HTML = build_footer_html(LOGO_B64)

    with gr.Blocks(
        title="HireSense_AI — Redrob Hackathon",
        head=SPEECH_HEAD,
        js=JS_ON_LOAD,
    ) as demo:

        gr.HTML(HEADER_HTML)
        stats_html = gr.HTML()

        with gr.Tabs(elem_classes=["tab-nav"]):

            # ── Tab 1: Top Rankings ────────────────────────────────────────
            with gr.TabItem("🏆 Top Rankings"):
                with gr.Row():
                    btn_top10  = gr.Button("⚡ Top 10",  variant="primary")
                    btn_top50  = gr.Button("🔥 Top 50",  variant="primary")
                    btn_top100 = gr.Button("📊 All 100", variant="secondary")
                ranking_table = gr.Dataframe(
                    label="HireSense_AI Rankings",
                    interactive=False,
                    wrap=False,
                    elem_classes=["ranking-scroll"],
                )
                btn_top10.click(
                    fn=lambda: show_top_n(10),
                    outputs=[ranking_table, stats_html],
                    js="() => { if(window.HireSenseVoice) window.HireSenseVoice.announceTopN(10); }",
                )
                btn_top50.click(
                    fn=lambda: show_top_n(50),
                    outputs=[ranking_table, stats_html],
                    js="() => { if(window.HireSenseVoice) window.HireSenseVoice.announceTopN(50); }",
                )
                btn_top100.click(
                    fn=lambda: show_top_n(100),
                    outputs=[ranking_table, stats_html],
                    js="() => { if(window.HireSenseVoice) window.HireSenseVoice.announceTopN(100); }",
                )

            # ── Tab 2: Search ──────────────────────────────────────────────
            with gr.TabItem("🔍 Search Candidates"):
                with gr.Row():
                    search_input = gr.Textbox(
                        label="Search by Role, ID, or Keyword",
                        placeholder="e.g. AI Engineer, NLP, CAND_0039754...",
                        lines=1,
                    )
                    search_btn = gr.Button("🔍 Search", variant="primary")
                search_results = gr.Dataframe(
                    label="Search Results",
                    interactive=False,
                    wrap=False,
                    elem_classes=["ranking-scroll"],
                )
                search_btn.click(
                    fn=search_candidates,
                    inputs=[search_input],
                    outputs=[search_results],
                )
                search_input.submit(
                    fn=search_candidates,
                    inputs=[search_input],
                    outputs=[search_results],
                )

            # ── Tab 3: Upload & Analyze ────────────────────────────────────
            with gr.TabItem("📁 Upload & Analyze"):
                gr.Markdown("""
### Upload Candidate Sample
Upload a JSON file (up to 50 candidates) to see how HireSense_AI domain filter evaluates them.

**Accepted formats:**
- `sample_candidates.json` (JSON array)
- `candidates.jsonl` (JSONL format)
""")
                file_input = gr.File(
                    label="Upload candidates.json or .jsonl",
                    file_types=[".json", ".jsonl"],
                )
                analyze_btn = gr.Button("🚀 Analyze Candidates", variant="primary")
                analysis_summary = gr.Textbox(
                    label="Analysis Summary",
                    interactive=False,
                    lines=2,
                )
                analysis_table = gr.Dataframe(
                    label="Filter Analysis Results",
                    interactive=False,
                    wrap=False,
                    elem_classes=["ranking-scroll"],
                )
                analyze_btn.click(
                    fn=upload_and_rank,
                    inputs=[file_input],
                    outputs=[analysis_table, analysis_summary],
                )

            with gr.TabItem("🧠  Architecture"):
                gr.Markdown("""
                ## HireSense_AI — System Architecture

                ```
                candidates.jsonl (100K)
                        ↓
                candidate_embedding.py
                  BAAI/bge-small-en-v1.5
                  Document embedding (no prefix)
                        ↓
                ChromaDB Vector Store
                  384-dim embeddings
                  100K indexed candidates
                        ↓
                semantic_ranking_pipeline.py
                        ↓
                ┌───────────────────────────┐
                │  BGE Query Embedding      │
                │  "Represent this sentence │
                │  for searching relevant   │
                │  passages: " + JD text    │
                └───────────────────────────┘
                        ↓
                ChromaDB.query(top_k=30,000)
                        ↓
                candidate_domain_filter.py
                  JD vocabulary overlap
                  Weighted domain score
                  Bigram tokenization
                  → Blocks Civil/HR/Sales
                  → Passes AI/ML/NLP/DS
                        ↓
                feature_vector_builder.py
                  23 Redrob signals used
                  Skill proficiency
                  Career recency decay
                  GitHub activity
                  Assessment scores
                        ↓
                ranker.py + weighted_score.py
                  Similarity:   70%
                  Skills:       12%
                  Experience:    8%
                  Profile:       4%
                  Behavior:      3%
                  Trust:         3%
                        ↓
                csv_reasoning_builder.py
                  Tier classification
                  Signal-rich reasoning
                  All 23 redrob signals
                        ↓
                HireSense_AI.csv
                  Top 100 AI/ML candidates
                  Validated ✓
                ```

                ## Key Design Decisions

                | Decision | Reason |
                |---|---|
                | BGE query prefix | Required for bge-small retrieval quality |
                | Similarity weight 70% | Semantic relevance dominates |
                | Bigram tokenization | Catches compound terms like machine_learning |
                | Career recency decay | Recent roles weighted higher |
                | Skill proficiency multiplier | Expert skills weighted 2x |
                | GitHub activity signal | Real technical evidence |
                | 23 Redrob signals | Full behavioral profile used |

                ## Evaluation Metrics Targeted

                | Metric | Weight | Our Strategy |
                |---|---|---|
                | NDCG@10 | 50% | Top 10 are strongest AI/ML profiles |
                | NDCG@50 | 30% | Domain filter ensures AI/ML only |
                | MAP | 15% | Semantic similarity drives precision |
                | P@10 | 5% | 100% relevant in top 10 |
                """)


        # ── Footer (outside tabs) ──────────────────────────────────────────
        gr.HTML(FOOTER_HTML)

        demo.load(
            fn=lambda: show_top_n(10),
            outputs=[ranking_table, stats_html],
        )

    return demo


if __name__ == "__main__":
    demo = build_interface()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
        css=HOLOGRAPHIC_CSS,
        theme=gr.themes.Base(
            primary_hue=gr.themes.colors.cyan,
            secondary_hue=gr.themes.colors.purple,
            neutral_hue=gr.themes.colors.slate,
            font=gr.themes.GoogleFont("Inter"),
        ),
    )