import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import math
import random
import base64
from datetime import datetime
from functools import lru_cache
from pathlib import Path

# Import our custom modules
from app_modules import (
    show_rag_fundamentals, show_rag_architectures, show_implementation_strategies,
    show_real_world_applications, show_performance_optimization, show_best_practices
)
from rag_lab import show_rag_lab
from advanced_rag_tab import show_advanced_rag

# ── Context First AI brand assets ────────────────────────────────────────────
# Logos are vendored in assets/brand/ (see the README there). The Brand Guide
# permits them on dark backgrounds only and forbids recolouring (§7).

BRAND_DIR = Path(__file__).resolve().parent / "assets" / "brand"
# The rendition the live site uses. Its background is baked in as #1A1B1E, the
# same Deep Space the app sets, so it blends instead of showing as a panel.
LOGO_HORIZONTAL = BRAND_DIR / "Logo_ContextFirstAI.png"
LOGO_ICON_PNG = BRAND_DIR / "favicon-32x32.png"


@lru_cache(maxsize=4)
def logo_data_uri(path_str: str) -> str:
    """Return an image file as a base64 data URI, or '' when it is absent.

    Embedding beats st.image() here: it survives Streamlit reruns without a
    media-file handle, and the width can be pinned in CSS.
    """
    path = Path(path_str)
    if not path.is_file():
        return ""
    mime = "image/svg+xml" if path.suffix.lower() == ".svg" else "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def render_logo(path: Path, width_px: int, *, centered: bool = False) -> None:
    """Render a brand logo at a fixed width, preserving its aspect ratio.

    Falls back to the wordmark in brand colours if the asset is missing, so a
    dropped file degrades gracefully instead of showing a broken image.
    """
    uri = logo_data_uri(str(path))
    if not uri:
        st.markdown(
            '<div class="brand-fallback">Context'
            '<span class="brand-fallback-accent">First</span>AI</div>',
            unsafe_allow_html=True,
        )
        return
    justify = "center" if centered else "flex-start"
    st.markdown(
        f'<div class="brand-logo" style="justify-content:{justify};">'
        f'<img src="{uri}" width="{width_px}" alt="Context First AI"/></div>',
        unsafe_allow_html=True,
    )


# Page configuration — the tab carries the brand mark, not a stock emoji.
st.set_page_config(
    page_title="RAG Understanding — Context First AI",
    page_icon=str(LOGO_ICON_PNG) if LOGO_ICON_PNG.is_file() else None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Context First AI brand theme ─────────────────────────────────────────────
# Palette and typography per the Context First AI Brand Guide (§4, §5).
#   Context Blue #41A5EE · Deep Space #1A1B1E · Pure White #FFFFFF
# Base colours (background, widgets, sidebar) come from .streamlit/config.toml;
# this block styles the custom classes and the typefaces.

BRAND = {
    "blue": "#41A5EE",        # Context Blue — primary accent
    "blue_light": "#6BB8F2",  # hover states, gradients
    "blue_dark": "#2B8ED9",   # active states
    "deep_space": "#1A1B1E",  # primary background
    "card": "#20242C",        # panels, lifted surfaces
    "white": "#FFFFFF",
    "muted": "#9CA3AF",       # secondary text
    "border": "#2D2E33",      # borders, dividers
    "success": "#1CCE5E",
    "warning": "#F6A823",
    "danger": "#EF4343",
}

# Plotly charts default to a light template, which fights the Deep Space
# background. Register a brand template once and make it the default.
_brand_template = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=BRAND["white"], family="Inter, sans-serif"),
        colorway=[
            BRAND["blue"], BRAND["blue_light"], BRAND["success"],
            BRAND["warning"], BRAND["blue_dark"], BRAND["danger"],
        ],
        xaxis=dict(gridcolor=BRAND["border"], zerolinecolor=BRAND["border"]),
        yaxis=dict(gridcolor=BRAND["border"], zerolinecolor=BRAND["border"]),
        legend=dict(font=dict(color=BRAND["muted"])),
    )
)
pio.templates["context_first"] = _brand_template
pio.templates.default = "plotly_dark+context_first"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"], .stMarkdown, p, li, span, div {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}
    h1, h2, h3, h4 {{
        font-family: 'Montserrat', system-ui, sans-serif;
        letter-spacing: -0.02em;
        font-weight: 600;
    }}

    /* Logo-style gradient lockup: Context Blue through Light Blue */
    .main-header {{
        font-family: 'Montserrat', system-ui, sans-serif;
        font-size: 3rem;
        font-weight: 600;
        letter-spacing: -0.02em;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, {BRAND['blue']} 0%, {BRAND['blue_light']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    /* Section headers carry the blue synthesis line from the logo */
    .section-header {{
        font-family: 'Montserrat', system-ui, sans-serif;
        font-size: 2rem;
        font-weight: 600;
        letter-spacing: -0.02em;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: {BRAND['white']};
        border-left: 3px solid {BRAND['blue']};
        padding-left: 0.75rem;
    }}

    .metric-box, .info-box, .success-box, .warning-box, .error-box {{
        background-color: {BRAND['card']};
        color: {BRAND['white']};
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid {BRAND['border']};
        margin: 1rem 0;
    }}
    .metric-box {{ border-left: 4px solid {BRAND['blue']}; }}
    .info-box    {{ border-left: 4px solid {BRAND['blue_light']}; }}
    .success-box {{ border-left: 4px solid {BRAND['success']}; }}
    .warning-box {{ border-left: 4px solid {BRAND['warning']}; }}
    .error-box   {{ border-left: 4px solid {BRAND['danger']}; }}

    /* Sidebar: card surface with a brand divider */
    section[data-testid="stSidebar"] {{
        background-color: {BRAND['card']};
        border-right: 1px solid {BRAND['border']};
    }}

    a, a:visited {{ color: {BRAND['blue']}; }}
    a:hover {{ color: {BRAND['blue_light']}; }}

    .stTabs [data-baseweb="tab-list"] {{ border-bottom: 1px solid {BRAND['border']}; }}
    .stTabs [aria-selected="true"] {{ color: {BRAND['blue']} !important; }}

    hr, [data-testid="stDivider"] {{ border-color: {BRAND['border']}; }}
    code {{ color: {BRAND['blue_light']}; }}
    .stCaption, [data-testid="stCaptionContainer"] {{ color: {BRAND['muted']}; }}

    /* Brand logo containers — clear space per Brand Guide §6 */
    .brand-logo {{
        display: flex;
        align-items: center;
        margin: 0.5rem 0 1.25rem 0;
    }}
    .brand-logo img {{ height: auto; max-width: 100%; }}

    /* Divider echoing the logo's blue synthesis line */
    .brand-rule {{
        height: 2px;
        background: linear-gradient(90deg, {BRAND['blue']} 0%, rgba(65,165,238,0) 100%);
        margin: 0 0 1rem 0;
    }}

    .brand-tagline {{
        text-align: center;
        color: {BRAND['muted']};
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        margin-top: -1.25rem;
        margin-bottom: 2rem;
    }}

    /* Shown only if a logo file is missing */
    .brand-fallback {{
        font-family: 'Montserrat', system-ui, sans-serif;
        font-weight: 600;
        letter-spacing: -0.02em;
        font-size: 1.6rem;
        color: {BRAND['white']};
    }}
    .brand-fallback-accent {{ color: {BRAND['blue']}; }}
</style>
""", unsafe_allow_html=True)

# Navigation
def main():
    render_logo(LOGO_HORIZONTAL, 340, centered=True)
    st.markdown('<h1 class="main-header">RAG Understanding</h1>', unsafe_allow_html=True)
    st.markdown('<p class="brand-tagline">From scattered context to focused clarity</p>', unsafe_allow_html=True)
    
    # Sidebar navigation — brand mark sits above the nav
    with st.sidebar:
        render_logo(LOGO_HORIZONTAL, 210)
        st.markdown('<div class="brand-rule"></div>', unsafe_allow_html=True)
    st.sidebar.title("📚 Learning Modules")
    
    page = st.sidebar.selectbox(
        "Choose a module:",
        [
            "🏠 Home",
            "🔍 RAG Fundamentals", 
            "🏗️ RAG Architectures",
            "⚙️ Implementation Strategies",
            "🌍 Real-World Applications",
            "⚡ Performance & Optimization",
            "📋 Best Practices & Tips",
            "🤖 Live RAG Demo (Qdrant + OpenAI)",
            "🚀 Advanced RAG",
        ]
    )
    
    if page == "🏠 Home":
        show_home()
    elif page == "🔍 RAG Fundamentals":
        show_rag_fundamentals()
    elif page == "🏗️ RAG Architectures":
        show_rag_architectures()
    elif page == "⚙️ Implementation Strategies":
        show_implementation_strategies()
    elif page == "🌍 Real-World Applications":
        show_real_world_applications()
    elif page == "⚡ Performance & Optimization":
        show_performance_optimization()
    elif page == "📋 Best Practices & Tips":
        show_best_practices()
    elif page == "🤖 Live RAG Demo (Qdrant + OpenAI)":
        show_rag_lab()
    elif page == "🚀 Advanced RAG":
        show_advanced_rag()

def show_home():
    st.markdown("""
    ## Welcome to the RAG Understanding Interactive Tutorial! 🚀
    
    This comprehensive interactive application will help you master Retrieval-Augmented Generation (RAG) 
    through hands-on examples, visualizations, and practical demonstrations.
    
    ### What You'll Learn:
    - **RAG Fundamentals**: Understanding the core concepts, components, and how RAG works
    - **RAG Architectures**: 9 different RAG patterns from Naive to Agentic RAG
    - **Implementation Strategies**: Step-by-step guides for building RAG systems
    - **Real-World Applications**: Practical examples and use cases
    - **Performance & Optimization**: Making your RAG systems fast and efficient
    - **Best Practices**: Industry tips and common pitfalls to avoid
    - **🤖 Live RAG Demo**: End-to-end pipeline using real Qdrant Cloud + OpenAI — ask questions
      against documents you ingested, compare RAG vs No-RAG, inspect retrieved chunks, and
      compare prompt strategies side-by-side
    
    ### How to Use This Tutorial:
    1. **Navigate** through modules using the sidebar
    2. **Interact** with visualizations and examples
    3. **Experiment** with different parameters and configurations
    4. **Learn** through hands-on practice and real-world scenarios
    
    ### Getting Started:
    Start with "RAG Fundamentals" to build your foundation, then explore other modules based on your interests.
    
    ---
    
    **Pro Tip**: Each module builds on previous concepts, so we recommend following the order in the sidebar!
    
    ### 🎯 Quick Navigation Guide:
    
    **For Beginners:**
    - Start with RAG Fundamentals
    - Explore the first few RAG Architectures
    - Try Implementation Strategies
    
    **For Intermediate Users:**
    - Jump to specific RAG Architectures
    - Focus on Performance & Optimization
    - Study Real-World Applications
    
    **For Advanced Users:**
    - Deep dive into Agentic RAG
    - Master Performance & Optimization
    - Review Best Practices for production systems
    """)

if __name__ == "__main__":
    main()
