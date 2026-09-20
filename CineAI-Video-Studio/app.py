python
# ============================================================
# 🎬 PREMIUM AI VIDEO STUDIO
# Streamlit + Groq
#
# Secret required in Streamlit Cloud:
# GROQ_API-KEY = "your_api_key"
# ============================================================

import time
import streamlit as st
from groq import Groq


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CineAI Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PREMIUM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(124, 58, 237, 0.18),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(59, 130, 246, 0.14),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #070711 0%,
                #0b0b18 45%,
                #080812 100%
            );

        color: #f8fafc;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ---------- HIDE DEFAULT ---------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* ---------- HERO ---------- */

    .hero {
        padding: 35px 20px 25px 20px;
        text-align: center;
    }

    .hero-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 999px;

        background: rgba(139, 92, 246, 0.12);
        border: 1px solid rgba(139, 92, 246, 0.35);

        color: #c4b5fd;
        font-size: 13px;
        font-weight: 700;

        letter-spacing: 1px;
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: 55px;
        font-weight: 900;
        line-height: 1.05;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #c4b5fd,
                #60a5fa
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        margin: 0;
    }

    .hero-subtitle {
        max-width: 720px;
        margin: 18px auto 0 auto;

        color: #a1a1b5;
        font-size: 17px;
        line-height: 1.7;
    }

    /* ---------- GLASS CARD ---------- */

    .glass-card {
        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.065),
                rgba(255,255,255,0.025)
            );

        border: 1px solid rgba(255,255,255,0.09);

        border-radius: 24px;

        padding: 25px;

        box-shadow:
            0 25px 70px rgba(0,0,0,0.35),
            inset 0 1px 0 rgba(255,255,255,0.05);

        backdrop-filter: blur(18px);
    }

    .section-title {
        font-size: 21px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .section-description {
        color: #85859a;
        font-size: 13px;
        margin-bottom: 18px;
    }

    /* ---------- SIDEBAR ---------- */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #090912 0%,
                #0d0d19 100%
            );

        border-right: 1px solid rgba(255,255,255,0.07);
    }

    .sidebar-brand {
        text-align: center;
        padding: 12px 0 28px 0;
    }

    .sidebar-logo {
        width: 65px;
        height: 65px;

        margin: auto;

        border-radius: 20px;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 31px;

        background:
            linear-gradient(
                135deg,
                #7c3aed,
                #2563eb
            );

        box-shadow:
            0 12px 35px rgba(124,58,237,0.35);
    }

    .sidebar-title {
        font-size: 19px;
        font-weight: 800;
        margin-top: 12px;
    }

    .sidebar-subtitle {
        color: #77778b;
        font-size: 12px;
        margin-top: 4px;
    }

    /* ---------- INPUTS ---------- */

    textarea,
    input {
        border-radius: 15px !important;
    }

    [data-baseweb="select"] > div {
        border-radius: 13px !important;
    }

    /* ---------- BUTTON ---------- */

    .stButton > button {
        width: 100%;

        min-height: 55px;

        border: 0;

        border-radius: 15px;

        color: white;

        font-size: 16px;
        font-weight: 800;

        background:
            linear-gradient(
                100deg,
                #7c3aed,
                #2563eb
            );

        box-shadow:
            0 12px 30px rgba(79,70,229,0.28);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 18px 40px rgba(79,70,229,0.40);
    }

    /* ---------- RESULT BOX ---------- */

    .result-header {
        display: flex;
        align-items: center;
        justify-content: space-between;

        margin-bottom: 15px;
    }

    .status-pill {
        padding: 7px 13px;
        border-radius: 999px;

        background: rgba(34,197,94,0.10);
        border: 1px solid rgba(34,197,94,0.25);

        color: #86efac;

        font-size: 12px;
        font-weight: 700;
    }

    /* ---------- METRICS ---------- */

    .metric-card {
        background: rgba(255,255,255,0.035);

        border: 1px solid rgba(255,255,255,0.07);

        border-radius: 15px;

        padding: 15px;

        text-align: center;
    }

    .metric-value {
        font-size: 20px;
        font-weight: 800;
    }

    .metric-label {
        color: #77778b;
        font-size: 11px;
        margin-top: 4px;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;

        color: #555568;

        font-size: 12px;

        margin-top: 45px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# GROQ API
# ============================================================

def get_api_key():

    try:

        if "GROQ_API-KEY" in st.secrets:

            key = st.secrets["GROQ_API-KEY"]

            if key and str(key).strip():
                return str(key).strip()

        return None

    except Exception:
        return None


API_KEY = get_api_key()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">

            <div class="sidebar-logo">
                🎬
            </div>

            <div class="sidebar-title">
                CineAI Studio
            </div>

            <div class="sidebar-subtitle">
                AI Video Prompt Creator
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### ⚙️ Generation Settings")

    aspect_ratio = st.selectbox(
        "Aspect Ratio",
        [
            "16:9 — YouTube / Landscape",
            "9:16 — TikTok / Reels / Shorts",
            "1:1 — Square",
        ],
    )

    duration = st.slider(
        "Video Duration",
        min_value=3,
        max_value=30,
        value=8,
        step=1,
        format="%d seconds",
    )

    style = st.selectbox(
        "Visual Style",
        [
            "Cinematic",
            "Photorealistic",
            "Anime",
            "3D Animation",
            "Documentary",
            "Fantasy",
            "Sci-Fi",
            "Commercial",
            "Music Video",
        ],
    )

    camera = st.selectbox(
        "Camera Style",
        [
            "Cinematic Camera",
            "Handheld",
            "Drone",
            "Slow Dolly",
            "Tracking Shot",
            "Close-up",
            "Wide Establishing Shot",
            "First Person",
        ],
    )

    quality = st.selectbox(
        "Quality",
        [
            "Ultra Cinematic",
            "Professional",
            "Natural",
            "Creative",
        ],
    )

    st.divider()

    st.markdown("### 🤖 Groq Model")

    model = st.selectbox(
        "Model",
        [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
        ],
        index=0,
    )

    st.divider()

    if API_KEY:

        st.success("🔐 API key connected")

    else:

        st.error(
            "🔑 GROQ_API-KEY is not configured"
        )

        st.caption(
            "Add GROQ_API-KEY in Streamlit Cloud → "
            "Settings → Secrets."
        )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            ⚡ POWERED BY GROQ
        </div>

        <h1 class="hero-title">
            Create Your Next
            <br>
            Cinematic Vision
        </h1>

        <p class="hero-subtitle">
            Describe your idea and let AI transform it into a
            professional, production-ready video prompt.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# MAIN COLUMNS
# ============================================================

left, right = st.columns(
    [0.95, 1.05],
    gap="large",
)


# ============================================================
# LEFT — PROMPT CREATOR
# ============================================================

with left:

    st.markdown(
        """
        <div class="glass-card">

        <div class="section-title">
            ✨ Describe Your Video
        </div>

        <div class="section-description">
            Be creative. Describe the scene, characters,
            action or story you want to visualize.
        </div>

        """,
        unsafe_allow_html=True,
    )

    prompt = st.text_area(
        "Video prompt",
        placeholder=(
            "Example:\n\n"
            "A young cricket player walks onto a huge stadium "
            "at sunset. The crowd is cheering while golden "
            "sunlight shines across the field. The camera "
            "slowly moves toward him..."
        ),
        height=260,
        label_visibility="collapsed",
    )

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    generate = st.button(
        "✨ Generate Cinematic Prompt",
        use_container_width=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# RIGHT — OUTPUT
# ============================================================

with right:

    st.markdown(
        """
        <div class="glass-card">

        <div class="result-header">

            <div>
                <div class="section-title">
                    🎞️ Your AI Result
                </div>

                <div class="section-description">
                    Your optimized production prompt appears here.
                </div>
            </div>

            <div class="status-pill">
                READY
            </div>

        </div>

        """,
        unsafe_allow_html=True,
    )

    if "result" not in st.session_state:
        st.session_state.result = ""

    if "generation_time" not in st.session_state:
        st.session_state.generation_time = 0


    if generate:

        if not API_KEY:

            st.error(
                """
                🔑 **API key missing**

                Add this to Streamlit Cloud Secrets:

                `GROQ_API-KEY = "your_api_key"`

                Then redeploy/restart the app.
                """
            )

        elif not prompt.strip():

            st.warning(
                "✍️ Please describe the video you want to create."
            )

        else:

            try:

                start_time = time.time()

                with st.status(
                    "🚀 Creating your cinematic prompt...",
                    expanded=True,
                ) as status:

                    st.write(
                        "🧠 Understanding your concept..."
                    )

                    client = Groq(
                        api_key=API_KEY
                    )

                    system_prompt = """
You are an elite cinematic director,
AI video prompt engineer and visual storyteller.

Transform the user's simple idea into an extremely
high-quality prompt for a modern text-to-video model.

The final prompt must contain:

1. Subject and characters
2. Environment
3. Story/action
4. Camera movement
5. Shot composition
6. Lens/camera feel
7. Lighting
8. Atmosphere
9. Color and visual mood
10. Realistic motion
11. Important environmental details
12. Professional cinematic quality

Do not explain what you did.

Return ONLY the final video-generation prompt.

Make it detailed but coherent.
Do not add unnecessary sections.
"""

                    user_prompt = f"""
Create a professional video-generation prompt from:

USER IDEA:
{prompt}

VIDEO SETTINGS:

Aspect Ratio:
{aspect_ratio}

Duration:
{duration} seconds

Visual Style:
{style}

Camera:
{camera}

Quality:
{quality}
"""

                    st.write(
                        "🎥 Building cinematic camera direction..."
                    )

                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {
                                "role": "system",
                                "content": system_prompt,
                            },
                            {
                                "role": "user",
                                "content": user_prompt,
                            },
                        ],
                        temperature=0.75,
                        max_completion_tokens=1600,
                    )

                    result = (
                        response
                        .choices[0]
                        .message
                        .content
                        .strip()
                    )

                    elapsed = (
                        time.time() - start_time
                    )

                    st.session_state.result = result
                    st.session_state.generation_time = elapsed

                    status.update(
                        label="✅ Generation complete",
                        state="complete",
                        expanded=False,
                    )

            except Exception as e:

                st.error(
                    f"""
                    ❌ **Generation failed**

                    `{type(e).__name__}`

                    {str(e)}
                    """
                )


    if st.session_state.result:

        st.text_area(
            "Optimized Video Prompt",
            value=st.session_state.result,
            height=360,
            key="final_prompt",
        )

        st.download_button(
            label="⬇️ Download Prompt",
            data=st.session_state.result,
            file_name="cinematic_video_prompt.txt",
            mime="text/plain",
            use_container_width=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)

        with m1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">
                        {aspect_ratio.split(" ")[0]}
                    </div>
                    <div class="metric-label">
                        ASPECT
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with m2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">
                        {duration}s
                    </div>
                    <div class="metric-label">
                        DURATION
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with m3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">
                        {st.session_state.generation_time:.1f}s
                    </div>
                    <div class="metric-label">
                        AI TIME
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:

        st.markdown(
            """
            <div style="
                height: 430px;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                color: #65657a;
            ">

                <div>

                    <div style="
                        font-size: 65px;
                        margin-bottom: 15px;
                    ">
                        🎞️
                    </div>

                    <div style="
                        font-size: 20px;
                        font-weight: 700;
                        color: #9b9bad;
                    ">
                        Your cinematic prompt
                        <br>
                        will appear here
                    </div>

                    <div style="
                        margin-top: 10px;
                        font-size: 13px;
                    ">
                        Describe your idea on the left
                        and click Generate.
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# INFORMATION SECTION
# ============================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="glass-card">

        <div class="section-title">
            🎬 How It Works
        </div>

        <div class="section-description">
            Three simple steps from idea to cinematic prompt.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown(
        """
        <div class="metric-card">

        <div style="font-size:32px;">
            💡
        </div>

        <div style="
            font-size:16px;
            font-weight:800;
            margin-top:8px;
        ">
            01 — Describe
        </div>

        <div style="
            color:#77778b;
            font-size:12px;
            margin-top:7px;
        ">
            Tell the AI what you want
            your video to look like.
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:

    st.markdown(
        """
        <div class="metric-card">

        <div style="font-size:32px;">
            🧠
        </div>

        <div style="
            font-size:16px;
            font-weight:800;
            margin-top:8px;
        ">
            02 — Enhance
        </div>

        <div style="
            color:#77778b;
            font-size:12px;
            margin-top:7px;
        ">
            Groq transforms your idea
            into cinematic instructions.
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:

    st.markdown(
        """
        <div class="metric-card">

        <div style="font-size:32px;">
            🎥
        </div>

        <div style="
            font-size:16px;
            font-weight:800;
            margin-top:8px;
        ">
            03 — Create
        </div>

        <div style="
            color:#77778b;
            font-size:12px;
            margin-top:7px;
        ">
            Copy the optimized prompt
            into your video generator.
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        🎬 CineAI Studio · Powered by Groq

        <br><br>

        Your API key is read from Streamlit Secrets
        and is never displayed in the interface.

    </div>
    """,
    unsafe_allow_html=True,
)
```
