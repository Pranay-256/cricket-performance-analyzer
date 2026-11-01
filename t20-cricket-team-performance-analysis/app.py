import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as mpatches
from matplotlib.ticker import MaxNLocator
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
if "df2" not in st.session_state:
    st.session_state.df2 = None

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Cricket Team Performance Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────
# FRAGMENT SUPPORT
# Fragments let a section re-run on its own when a widget inside
# it changes, instead of re-drawing every chart on every tab.
# Falls back to a plain function on older Streamlit versions.
# ─────────────────────────────────────────────────────────────
_fragment_impl = getattr(st, "fragment", None) or getattr(st, "experimental_fragment", None)


def fragment(func):
    return _fragment_impl(func) if _fragment_impl else func


# ─────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap" rel="stylesheet">

<style>

/* ── Root tokens ─────────────────────────────────────────── */
:root {
    --bg-base:      #0d1117;
    --bg-card:      #161b22;
    --bg-card2:     #1c2330;
    --border:       #2a3444;
    --gold:         #c9a84c;
    --gold-light:   #e0c070;
    --teal:         #2dd4bf;
    --teal-dim:     #1a9e8f;
    --text-primary: #e6edf3;
    --text-muted:   #8b949e;
    --text-accent:  #c9a84c;
    --danger:       #e05252;
    --success:      #3fb950;
    --tab-active:   #c9a84c;
}

/* ── Base ────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif !important;
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
}

/* ── Streamlit chrome overrides ──────────────────────────── */
.stApp { background-color: var(--bg-base) !important; }
header[data-testid="stHeader"] { background: var(--bg-base) !important; border-bottom: 1px solid var(--border); }

/* ── FIX #6: Shift content up — reduce top padding ──────── */
.main .block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
}

/* ── FIX #1: Dataframe visibility fix ───────────────────── */
/* ── SAFE DATAFRAME STYLING (STREAMLIT-COMPATIBLE) ── */

/* Outer container */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    background: var(--bg-card) !important;
    padding: 4px;
}

/* Inner wrapper */
div[data-testid="stDataFrame"] > div {
    background: var(--bg-card) !important;
}

/* Text color (safe override) */
div[data-testid="stDataFrame"] * {
    color: var(--text-primary) !important;
}

/* Header styling (optional premium touch) */
div[data-testid="stDataFrame"] thead {
    background: rgba(201,168,76,0.08) !important;
}

/* Scrollbar inside dataframe */
div[data-testid="stDataFrame"] ::-webkit-scrollbar {
    height: 6px;
    width: 6px;
}

div[data-testid="stDataFrame"] ::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 4px;
}

div[data-testid="stDataFrame"] ::-webkit-scrollbar-thumb:hover {
    background: var(--gold);
}

/* ── FIX #2: Tab buttons look like real buttons ──────────── */
/* ── PREMIUM BUTTON-LIKE TABS ─────────────────────────── */

/* ── MINIMAL PREMIUM TABS (LIKE STREAMLIT DEFAULT) ───────── */

div[data-baseweb="tab-list"] {
    border-bottom: 1px solid var(--border) !important;
    gap: 18px;
}

/* Individual tabs */
div[data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600;
    font-size: 16px !important;

    color: var(--text-muted) !important;

    padding: 10px 6px !important;
    background: transparent !important;
    border: none !important;

    transition: all 0.2s ease;
}

/* Hover effect (subtle, not button-like) */
div[data-baseweb="tab"]:hover {
    color: var(--gold-light) !important;
}

/* ACTIVE TAB */
div[data-baseweb="tab"][aria-selected="true"] {
    color: var(--gold) !important;
    font-weight: 700 !important;
}

/* 🔥 GOLD UNDERLINE (THIS IS THE KEY PART) */
div[data-baseweb="tab-highlight"] {
    background: linear-gradient(90deg, #c9a84c, #e0c070) !important;
    height: 3px !important;
    border-radius: 2px;
}

/* remove default border line artifacts */
div[data-baseweb="tab-border"] {
    background: transparent !important;
}

/* ── Sidebar ─────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* ── Radio buttons ───────────────────────────────────────── */
div[role="radiogroup"] label {
    font-family: 'Rajdhani', sans-serif !important;
    color: var(--text-primary) !important;
    font-size: 14px;
}

/* ── Buttons ─────────────────────────────────────────────── */
div.stButton > button {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700;
    font-size: 15px;
    letter-spacing: 0.5px;
    background: linear-gradient(135deg, #b8922e 0%, #e0c070 100%) !important;
    color: #0d1117 !important;
    border: none !important;
    border-radius: 8px !important;
    height: 46px !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 2px 12px rgba(201,168,76,0.15) !important;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #e0c070 0%, #c9a84c 100%) !important;
    box-shadow: 0 4px 20px rgba(201,168,76,0.30) !important;
    transform: translateY(-1px) !important;
}

/* ── Download buttons ────────────────────────────────────── */
div.stDownloadButton > button {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 500;
    font-size: 14px;
    background: transparent !important;
    color: var(--teal) !important;
    border: 1px solid var(--teal-dim) !important;
    border-radius: 7px !important;
    height: 40px !important;
    transition: all 0.2s ease !important;
}
div.stDownloadButton > button:hover {
    background: rgba(45,212,191,0.08) !important;
    border-color: var(--teal) !important;
    box-shadow: 0 0 10px rgba(45,212,191,0.15) !important;
}

/* ── Selectbox ───────────────────────────────────────────── */
div[data-baseweb="select"] > div {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}
div[data-baseweb="select"] span { color: var(--text-primary) !important; }

/* ── Expanders ───────────────────────────────────────────── */
div[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    margin-bottom: 10px;
}
div[data-testid="stExpander"] summary {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    color: var(--gold-light) !important;
    padding: 12px 16px !important;
}
div[data-testid="stExpander"] summary:hover {
    background: rgba(201,168,76,0.06) !important;
}
div[data-testid="stExpander"] > div > div {
    padding: 4px 20px 16px 20px !important;
    color: var(--text-primary) !important;
}

/* ── Alerts / messages ───────────────────────────────────── */
div[data-testid="stAlert"] {
    border-radius: 8px !important;
    font-family: 'Rajdhani', sans-serif !important;
}

/* ── Dividers ────────────────────────────────────────────── */
hr { border-color: var(--border) !important; }

/* ── Pyplot figures background ───────────────────────────── */
div[data-testid="stImage"] img { border-radius: 8px; }

/* ── File uploader ───────────────────────────────────────── */
div[data-testid="stFileUploader"] {
    background: var(--bg-card2) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 10px !important;
    padding: 8px;
}
div[data-testid="stFileUploader"] * { color: var(--text-primary) !important; }

/* ── FIX #5: Markdown / body text font → Rajdhani ────────── */
p, li {
    color: var(--text-primary) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 15px;
    line-height: 1.7;
}
strong { color: var(--text-primary) !important; font-family: 'Rajdhani', sans-serif !important; }
a { color: var(--teal) !important; text-decoration: none; }
a:hover { text-decoration: underline; color: var(--gold-light) !important; }

/* ── Scrollbar ───────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold); }

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# CHART THEME
# ─────────────────────────────────────────────────────────────
mpl.rcParams.update({
    "font.family":       "DejaVu Sans",
    "axes.titlesize":    14,
    "axes.titleweight":  "bold",
    "axes.labelsize":    11,
    "xtick.labelsize":   9,
    "ytick.labelsize":   9,
    "legend.fontsize":   9,
    "legend.framealpha": 1.0,
    "legend.edgecolor":  "#000000",
    "legend.facecolor":  "#ffffff",
    "legend.labelcolor": "#000000",
    "legend.title_fontsize": 9,
})

# ─────────────────────────────────────────────────────────────
# COLOUR PALETTES — thematically matched per chart
# ─────────────────────────────────────────────────────────────
BATTING_CMAP     = "YlOrRd"      # batting: warm gold→amber tones
BOWLING_CMAP     = "YlGnBu"      # bowling: cool blue→teal tones
ROLE_BAT_COLORS  = ["#c9a84c", "#dd8452", "#4c9be8"]
ROLE_BOWL_COLORS = ["#2dd4bf", "#4c72b0", "#c9a84c"]
ORDER_PAL        = "viridis"
SR_ROLE_COLORS   = {"batsman": "#c9a84c", "all-rounder": "#2dd4bf"}
ECO_ROLE_COLORS  = {"bowler": "#4c72b0", "all-rounder": "#2dd4bf"}
PHASE_COLOR_MAP  = {"Powerplay": "#e05252", "Middle Overs": "#e0c070", "Death Overs": "#3fb950"}
PHASE_ORDER      = ["Powerplay", "Middle Overs", "Death Overs"]

# Player Analytics: distinct palette, separate from other tabs
PLAYER_BAT_CMAP        = "RdPu"
PLAYER_BOWL_CMAP       = "PuBu"
PLAYER_BAT_LINE_COLOR  = "#e0529f"
PLAYER_BOWL_LINE_COLOR = "#5b7fd6"

# Figure sizes
BAR_W, BAR_H   = 10, 5      # horizontal bar charts
LINE_W, LINE_H = 8,  5      # line charts
PIE_W,  PIE_H  = 8,  6      # pie charts
SIDE_W, SIDE_H = 10, 4      # side-by-side (summary)

DESC_STYLE = ("font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e; "
              "line-height:1.6;")

# ─────────────────────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────────────────────
def section_heading(icon, title):
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, rgba(201,168,76,0.12) 0%, transparent 100%);
        border-left: 3px solid #c9a84c;
        border-radius: 0 8px 8px 0;
        padding: 10px 18px;
        margin: 18px 0 10px 0;
    ">
        <span style="font-family:'Rajdhani',sans-serif; font-weight:700;
                     font-size:20px; color:#e0c070; letter-spacing:0.4px;">
            {icon}&nbsp; {title}
        </span>
    </div>
    """, unsafe_allow_html=True)


def description(text, margin="-6px 0 10px 0"):
    st.markdown(f"""
    <p style="{DESC_STYLE} margin: {margin};">
        {text}
    </p>
    """, unsafe_allow_html=True)


def column_info(title, text):
    st.markdown(f"""
    <div style="
        background: #1c2330;
        border: 1px solid #2a3444;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 8px;
    ">
        <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                  font-size:15px; color:#c9a84c; margin:0 0 4px 0;">{title}</p>
        <p style="font-family:'Rajdhani',sans-serif; font-size:13px;
                  color:#8b949e; margin:0; line-height:1.55;">{text}</p>
    </div>
    """, unsafe_allow_html=True)


def kpi_card(icon, label, value, sub=""):
    sub_html = f"<p style='font-size:12px; color:#8b949e; margin:2px 0 0 0; font-family:Rajdhani,sans-serif;'>{sub}</p>" if sub else ""
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, #1c2330, #161b22);
        border: 1px solid #2a3444;
        border-top: 2px solid #c9a84c;
        border-radius: 10px;
        padding: 16px 18px;
        text-align: center;
        height: 100%;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    ">
        <div style="font-size:26px; margin-bottom:6px;">{icon}</div>
        <p style="font-family:'Rajdhani',sans-serif; font-size:12px;
                  color:#8b949e; margin:0 0 4px 0; text-transform:uppercase;
                  letter-spacing:0.8px;">{label}</p>
        <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                  font-size:22px; color:#e0c070; margin:0; line-height:1.1;">{value}</p>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def insight_line(number, text):
    st.markdown(f"""
    <div style="
        background: #161b22;
        border: 1px solid #2a3444;
        border-left: 3px solid #2dd4bf;
        border-radius: 0 8px 8px 0;
        padding: 10px 16px;
        margin-bottom: 8px;
        display: flex;
        align-items: flex-start;
        gap: 12px;
    ">
        <span style="font-family:'Rajdhani',sans-serif; font-weight:700;
                     font-size:16px; color:#2dd4bf; min-width:24px;">{number}.</span>
        <span style="font-family:'Rajdhani',sans-serif; font-size:14px;
                     color:#e6edf3; line-height:1.6;">{text}</span>
    </div>
    """, unsafe_allow_html=True)


def sub_heading(text, size=20, margin="4px 0 10px 0", color="#e0c070", tag="p", spacing=""):
    letter = f" letter-spacing:{spacing};" if spacing else ""
    st.markdown(f"""
    <{tag} style="font-family:'Rajdhani',sans-serif; font-weight:700;
              font-size:{size}px; color:{color}; margin:{margin};{letter}">
        {text}
    </{tag}>
    """, unsafe_allow_html=True)


def card_list(items, border_color=None, prefix=""):
    """Stacked small cards used in the About page."""
    left_border = f"border-left:3px solid {border_color}; " if border_color else ""
    radius = "0 6px 6px 0" if border_color else "6px"
    for item in items:
        st.markdown(f"""
        <div style="background:#1c2330; border:1px solid #2a3444; {left_border}
                    border-radius:{radius}; padding:8px 14px; margin-bottom:6px;
                    font-family:'Rajdhani',sans-serif; font-size:14px; color:#e6edf3;">
            {prefix}{item}
        </div>
        """, unsafe_allow_html=True)


def about_block(title, items, title_size=17, item_size=14, item_prefix="▸ &nbsp;"):
    body = "".join(
        f"<p style='font-family:Rajdhani,sans-serif; font-size:{item_size}px; color:#e6edf3; margin:3px 0;'>{item_prefix}{i}</p>"
        for i in items
    )
    st.markdown(f"""
    <div style="background:#1c2330; border:1px solid #2a3444; border-radius:8px;
                padding:12px 16px; margin-bottom:10px;">
        <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                  font-size:{title_size}px; color:#c9a84c; margin:0 0 6px 0;">
            {title}
        </p>
        {body}
    </div>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div style="text-align:center; padding:24px 0 6px 0;">
        <h1 style="font-family:'Rajdhani',sans-serif; font-weight:700;
                   font-size:38px; color:#e0c070; margin:0; letter-spacing:1px;">
            🏏 Cricket Team Performance Analyzer
        </h1>
        <p style="font-family:'Rajdhani',sans-serif; font-size:16px;
                  color:#8b949e; margin:6px 0 0 0;">
            Data-Driven Analysis of Your Cricket Team Performance (currently only supports T-20 Format)
        </p>
    </div>
    """, unsafe_allow_html=True)


def bottom_space():
    st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# CHART HELPERS  (one implementation for every chart type)
# ─────────────────────────────────────────────────────────────
def _finish(fig):
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def _style_legend(legend, title=None):
    if legend is None:
        return
    if title:
        legend.set_title(title)
    legend.get_frame().set_facecolor("#ffffff")
    legend.get_frame().set_edgecolor("#000000")
    legend.get_frame().set_alpha(1.0)
    for t in legend.get_texts():
        t.set_fontsize(9)
        t.set_fontweight("bold")
        t.set_color("#000000")
    legend.get_title().set_color("#000000")


def bar_chart(x, y, title, xlabel, ylabel, palette, grid_axis, figsize,
              hue=None, integer_y=False):
    fig, ax = plt.subplots(figsize=figsize, dpi=120)
    if hue is None:
        sns.barplot(x=x, y=y, palette=palette, ax=ax)
    else:
        sns.barplot(x=x, y=y, hue=hue, palette=palette, ax=ax)
        _style_legend(ax.get_legend(), "Role")
    if integer_y:
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(axis=grid_axis, linestyle="--", alpha=0.4)
    _finish(fig)


def line_chart(x, y, title, xlabel, ylabel, color):
    fig, ax = plt.subplots(figsize=(LINE_W, LINE_H), dpi=120)
    sns.lineplot(x=x, y=y, marker="o", color=color, ax=ax)
    ax.set_xticks(list(x))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # evenly spaced ticks, not one per data value
    ax.set_ylim(bottom=0)                                  # zero baseline so small changes aren't exaggerated
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(linestyle="--", alpha=0.4)
    _finish(fig)


def pie_chart(values, labels, legend_title, title, colors):
    fig, ax = plt.subplots(figsize=(PIE_W, PIE_H), dpi=120)
    wedges, _, autotexts = ax.pie(
        values, labels=None, autopct="%1.1f%%", startangle=90,
        wedgeprops={"edgecolor": "black"}, colors=colors
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_fontweight("bold")
        at.set_color("black")
    ax.legend(wedges, labels, title=legend_title, title_fontsize=9,
              loc="center left", bbox_to_anchor=(1, 0.5), fontsize=9,
              framealpha=1.0, edgecolor="#000000", facecolor="#ffffff",
              labelcolor="#000000")
    ax.get_legend().get_title().set_color("#000000")
    ax.set_title(title, fontsize=14, fontweight="bold")
    _finish(fig)


def pie_labels(names, values):
    return [f"{n}  —  {v}" for n, v in zip(names, values)]


def show_table(df):
    st.dataframe(df, use_container_width=True)


def one_based(df):
    df = df.copy()
    df.index = range(1, len(df) + 1)
    return df


# ─────────────────────────────────────────────────────────────
# CRICKET OVER ↔ BALL CONVERSION
# Overs are written as O.B (3.4 = 3 overs 4 balls), so they must
# be added as balls, never as decimals.
# ─────────────────────────────────────────────────────────────
def balls_to_overs(balls):
    return np.round(balls // 6 + (balls % 6) / 10, 1)


# ─────────────────────────────────────────────────────────────
# DATA VALIDATION
# ─────────────────────────────────────────────────────────────
def data_validation(df):
    out_over = pd.to_numeric(df["Out_Over"], errors="coerce")

    if (out_over > 20).any():
        raise ValueError("Current Version only supports T20 data (Out_Over cannot exceed 20)")
    if (df.groupby("Match_No")["Player_Name"].nunique() > 11).any():
        raise ValueError("A single match cannot have more than 11 players")
    if df["Player_Name"].nunique() > 22:
        raise ValueError("Dataset contains too many unique players. Please limit uploads to 2 matches at a time.")

    # NEW RULE: a team can take at most 10 wickets in a single match
    wickets = pd.to_numeric(df["Wickets_Taken"], errors="coerce")
    if (wickets.groupby(df["Match_No"]).sum() > 10).any():
        raise ValueError("Total wickets taken in a single match cannot be more than 10")

    if df["Match_No"].isnull().any():
        raise ValueError("Some players don't have Match Number information")
    if df["Batting_Position"].isnull().any():
        raise ValueError("Some players don't have Batting Position information")

    start      = df["Batting_Start_Over"]
    balls      = df["Balls_Played"]
    runs       = df["Runs_Scored"]
    overs      = df["Overs_Bowled"]
    runs_given = df["Runs_Given"]
    wkts       = df["Wickets_Taken"]

    batting_cols = [df["Role"], df["Batting_Position"], start, df["Out_Over"],
                    balls, runs, overs, runs_given, wkts]
    if (df["Player_Name"].isnull() & np.logical_or.reduce([c.notnull() for c in batting_cols])).any():
        raise ValueError("Some players don't have their name")

    # Batting columns
    bat_no_start_with_stats = start.isnull() & (df["Out_Over"].notnull() | balls.notnull() | runs.notnull())
    # Out_Over may legitimately be blank / "not-out" for a batter who was not dismissed
    bat_start_missing_stats = start.notnull() & (balls.isnull() | runs.isnull())
    bat_start_after_out     = start.notnull() & out_over.notnull() & (start > out_over)
    if bat_no_start_with_stats.any() or bat_start_missing_stats.any() or bat_start_after_out.any():
        raise ValueError("Invalid data found in batting columns")

    # Bowling columns
    did_not_bowl = overs.isnull() | (overs == 0)
    bowl_stats_without_overs = did_not_bowl & (runs_given.notnull() | wkts.notnull())
    bowl_overs_missing_stats = overs.notnull() & (overs > 0) & (runs_given.isnull() | wkts.isnull())
    if bowl_stats_without_overs.any() or bowl_overs_missing_stats.any():
        raise ValueError("Invalid data found in bowling columns")

    return True


# ─────────────────────────────────────────────────────────────
# DATA PROCESSING (CACHED)
# ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def process_data(df):
    df2 = df.copy()

    role = df2["Role"].str.strip().str.lower()
    role = role.fillna(role.mode()[0]).replace("wicketkeeper", "batsman")
    df2["Role"] = role

    df2["Out_Over"] = pd.to_numeric(df2["Out_Over"], errors="coerce")
    fill_zero = ["Batting_Start_Over", "Out_Over", "Balls_Played", "Runs_Scored", "Overs_Bowled"]
    df2[fill_zero] = df2[fill_zero].fillna(0)

    df2[["Runs_Given", "Wickets_Taken"]] = df2[["Runs_Given", "Wickets_Taken"]].fillna(0)

    df2["Batted"]  = df2["Batting_Start_Over"] > 0
    df2["Was_Out"] = df2["Out_Over"] > 0

    # Strike Rate
    balls_faced = df2["Balls_Played"]
    df2["Strike_Rate"] = np.where(balls_faced > 0, df2["Runs_Scored"] / balls_faced.where(balls_faced > 0, 1) * 100, 0.0)
    df2["Strike_Rate"] = df2["Strike_Rate"].round(2)

    # Balls bowled (O.B notation -> total balls) and Economy Rate
    full_overs = df2["Overs_Bowled"].astype(int)
    extra_balls = ((df2["Overs_Bowled"] - full_overs) * 10).round().astype(int)
    df2["Balls_Bowled"] = full_overs * 6 + extra_balls

    real_over = df2["Balls_Bowled"] / 6
    df2["Economy_Rate"] = np.where(real_over > 0, df2["Runs_Given"] / real_over.where(real_over > 0, 1), 0.0)
    df2["Economy_Rate"] = df2["Economy_Rate"].round(2)

    # Batting order group (used by Batting + Summary tabs)
    df2["Batting_Order"] = pd.cut(
        df2["Batting_Position"], bins=[0, 3, 7, 11], labels=["top", "middle", "lower"]
    ).astype(str)

    return df2


# ─────────────────────────────────────────────────────────────
# TEAM-LEVEL STATISTICS (CACHED — computed once per dataset and
# shared by the Batting, Bowling and Summary tabs)
# ─────────────────────────────────────────────────────────────
def _consistency_table(match_values, value_col):
    table = (
        match_values.groupby("Player_Name")[value_col]
        .agg(["mean", "std", "count"]).round(2).reset_index()
    )
    table = table[table["count"] > 1].copy()
    table["Consistency_Score"] = (table["mean"] / (table["std"] + 1)).round(2)
    table = table.sort_values(by="Consistency_Score", ascending=False).reset_index(drop=True)
    return one_based(table[["Player_Name", "Consistency_Score"]])


def _consistency_state(active_rows, value_col):
    """Returns (status, table) where status is 'single', 'unique' or 'ok'."""
    per_match = active_rows.groupby(["Match_No", "Player_Name"])[value_col].sum().reset_index()
    matches_per_player = active_rows.groupby("Player_Name")["Match_No"].nunique()
    if active_rows["Match_No"].nunique() == 1:
        return "single", None
    if (matches_per_player == 1).all():
        return "unique", None
    return "ok", _consistency_table(per_match, value_col)


@st.cache_data(show_spinner=False)
def compute_team_stats(df2):
    s = {}
    done_bat = df2[df2["Balls_Played"] > 0]
    done_bowl = df2[df2["Overs_Bowled"] > 0]

    # ── Batting: runs per player ──
    runs_by_player = (
        done_bat.groupby("Player_Name")
        .agg(Runs_Scored=("Runs_Scored", "sum"), Balls_Played=("Balls_Played", "sum"))
        .sort_values(by="Runs_Scored", ascending=False).astype(int).reset_index()
    )
    s["runs_by_player"] = runs_by_player

    top = runs_by_player[["Player_Name", "Runs_Scored"]].head(5).reset_index(drop=True)
    others = int(runs_by_player["Runs_Scored"].sum()) - int(top["Runs_Scored"].sum())
    batting_pie = top.copy()
    batting_pie.loc[len(batting_pie)] = ["Others", others]
    s["batting_pie"] = batting_pie[batting_pie["Runs_Scored"] > 0]

    # ── Batting: runs by role ──
    runs_role = (
        done_bat[done_bat["Runs_Scored"] > 0]
        .groupby("Role", as_index=False)["Runs_Scored"]
        .sum().sort_values(by="Runs_Scored", ascending=False).reset_index(drop=True)
    )
    runs_role["Runs_Scored"] = runs_role["Runs_Scored"].astype(int)
    s["runs_role"] = runs_role

    # ── Batting: strike rate (unfiltered; the tab filters to >= 10 balls) ──
    bat_ar = done_bat[done_bat["Role"].isin(["batsman", "all-rounder"])]
    s["bat_ar_empty"] = bat_ar.empty
    s["strike_rate"] = (
        bat_ar.groupby("Player_Name")
        .agg(Role=("Role", "first"), Strike_Rate=("Strike_Rate", "mean"),
             Runs_Scored=("Runs_Scored", "sum"), Balls_Played=("Balls_Played", "sum"))
        .sort_values(by="Strike_Rate", ascending=False).round(2).reset_index()
    )

    # ── Batting: consistency ──
    s["bat_consistency_state"], s["bat_consistency"] = _consistency_state(done_bat, "Runs_Scored")

    # ── Batting: batting order ──
    order_runs = (
        df2.groupby("Batting_Order", as_index=False)["Runs_Scored"]
        .sum().sort_values(by="Runs_Scored", ascending=False).reset_index(drop=True)
        .rename(columns={"Runs_Scored": "Total_Runs_Scored"})
    )
    s["order_runs"] = order_runs

    # average runs per batting innings (rows where the player actually batted)
    s["order_avg_runs"] = (
        done_bat.groupby("Batting_Order", as_index=False)["Runs_Scored"].mean().round(2)
        .sort_values(by="Runs_Scored", ascending=False).reset_index(drop=True)
        .rename(columns={"Runs_Scored": "Average_Runs_Scored"})
    )

    # ── Batting: phase-wise wickets lost ──
    overs_out = df2.loc[df2["Out_Over"] > 0, "Out_Over"]
    phase = np.select([overs_out <= 6, overs_out <= 15], ["Powerplay", "Middle Overs"], default="Death Overs")
    counts = pd.Series(phase, dtype=object).value_counts().reindex(PHASE_ORDER, fill_value=0)
    s["phase_wickets"] = (
        counts.rename_axis("Wicket_Phase").reset_index(name="Wickets_Lost")
        .sort_values(by="Wickets_Lost", ascending=False, kind="stable")
    )

    # ── Bowling: wickets per player ──
    bowl_by_player = (
        done_bowl.groupby("Player_Name", as_index=False)
        .agg(Wickets_Taken=("Wickets_Taken", "sum"), Balls_Bowled=("Balls_Bowled", "sum"))
        .sort_values(by="Wickets_Taken", ascending=False).reset_index(drop=True)
    )
    bowl_by_player["Wickets_Taken"] = bowl_by_player["Wickets_Taken"].astype(int)
    bowl_by_player["Overs_Bowled"] = balls_to_overs(bowl_by_player["Balls_Bowled"])
    s["bowl_by_player"] = bowl_by_player[["Player_Name", "Wickets_Taken", "Overs_Bowled"]]

    top_b = bowl_by_player[["Player_Name", "Wickets_Taken"]].head()
    other_w = int(bowl_by_player["Wickets_Taken"].sum()) - int(top_b["Wickets_Taken"].sum())
    bowling_pie = top_b.copy().reset_index(drop=True)
    bowling_pie.loc[len(bowling_pie)] = ["Others", other_w]
    bowling_pie.index += 1
    s["bowling_pie"] = bowling_pie[bowling_pie["Wickets_Taken"] > 0]

    # ── Bowling: wickets by role ──
    wk_role = (
        done_bowl[done_bowl["Wickets_Taken"] > 0]
        .groupby("Role", as_index=False)["Wickets_Taken"]
        .sum().sort_values(by="Wickets_Taken", ascending=False).reset_index(drop=True)
    )
    wk_role["Wickets_Taken"] = wk_role["Wickets_Taken"].astype(int)
    s["wickets_role"] = wk_role

    # average wickets per bowling innings (rows where the player actually bowled), by role
    s["wickets_role_avg"] = (
        done_bowl.groupby("Role", as_index=False)["Wickets_Taken"].mean().round(2)
        .sort_values(by="Wickets_Taken", ascending=False).reset_index(drop=True)
        .rename(columns={"Wickets_Taken": "Average_Wickets_Taken"})
    )

    # ── Bowling: economy (unfiltered; the tab filters to >= 2 overs) ──
    bowl_ar = done_bowl[done_bowl["Role"].isin(["bowler", "all-rounder"])]
    s["bowl_ar_empty"] = bowl_ar.empty
    s["economy"] = (
        bowl_ar.groupby("Player_Name", as_index=False)
        .agg(Role=("Role", "first"), Economy_Rate=("Economy_Rate", "mean"),
             Balls_Bowled=("Balls_Bowled", "sum"), Runs_Given=("Runs_Given", "sum"))
        .sort_values(by="Economy_Rate").round(2).reset_index(drop=True)
    )

    # ── Bowling: consistency ──
    s["bowl_consistency_state"], s["bowl_consistency"] = _consistency_state(done_bowl, "Wickets_Taken")

    # ── Summary: runs & wickets per match ──
    s["runs_wickets"] = (
        df2.groupby("Match_No", as_index=False)
        .agg({"Runs_Scored": "sum", "Wickets_Taken": "sum"}).astype(int)
    )

    return s


@st.cache_data(show_spinner=False)
def compute_player_match_stats(df2):
    """Per player, per match totals — used by the Player Analytics tab."""
    pm = (
        df2.groupby(["Player_Name", "Match_No"], as_index=False)
        .agg(Runs_Scored=("Runs_Scored", "sum"), Balls_Played=("Balls_Played", "sum"),
             Wickets_Taken=("Wickets_Taken", "sum"), Runs_Given=("Runs_Given", "sum"),
             Balls_Bowled=("Balls_Bowled", "sum"))
        .sort_values(["Player_Name", "Match_No"])
    )
    for col in ["Runs_Scored", "Balls_Played", "Wickets_Taken", "Runs_Given"]:
        pm[col] = pm[col].astype(int)
    pm["Match_No"] = pm["Match_No"].astype(int)
    return pm


@st.cache_data(show_spinner=False)
def read_file_bytes(path):
    with open(path, "rb") as f:
        return f.read()


# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
def render_footer():
    components.html("""
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
    <style>
        body { margin:0; padding:0; background:transparent; }

        .footer-wrapper {
            display: flex;
            justify-content: space-around;
            text-align: center;
            padding: 28px 0 8px 0;
            border-top: 1px solid #2a3444;
        }

        .footer-item { flex: 1; }

        .footer-item .title {
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            font-size: 16px;
            color: #c9a84c;
            margin-bottom: 4px;
        }

        .footer-item .subtitle {
            font-family: 'Rajdhani', sans-serif;
            color: #8b949e;
            font-size: 13px;
            margin-top: 0;
        }

        .footer-credit {
            text-align: center;
            font-family: 'Rajdhani', sans-serif;
            color: #8b949e;
            font-size: 13px;
            padding: 12px 0 4px 0;
        }
    </style>

    <div class="footer-wrapper">
        <div class="footer-item">
            <p class="title">&#128274; Secure &amp; Reliable</p>
            <p class="subtitle">Your data is processed securely</p>
        </div>
        <div class="footer-item">
            <p class="title">&#9889; Real Time Results</p>
            <p class="subtitle">Instant results in seconds</p>
        </div>
        <div class="footer-item">
            <p class="title">&#128200; 100% Accuracy</p>
            <p class="subtitle">Get 100% accurate Insights</p>
        </div>
    </div>

    <p class="footer-credit">Developed by Pranay Jha &nbsp;|&nbsp; Powered by Python and Streamlit</p>
    """, height=240)


# ─────────────────────────────────────────────────────────────
# TAB 1 — UPLOAD SECTION (fragment: radio / uploader changes no
# longer re-draw every chart in the other tabs)
# ─────────────────────────────────────────────────────────────
def _read_uploaded(file):
    return pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)


@fragment
def upload_section():
    upload_type = st.radio("", ["Upload Single Dataset", "Upload Multiple Datasets"])

    if upload_type == "Upload Single Dataset":
        uploaded_files = st.file_uploader("Upload Single Dataset", type=["csv", "xlsx"], accept_multiple_files=False)
    else:
        uploaded_files = st.file_uploader("Upload Multiple Datasets", type=["csv", "xlsx"], accept_multiple_files=True)

    if (uploaded_files is None or uploaded_files == []) and st.session_state.df2 is not None:
        st.session_state.df2 = None
        st.rerun()

    st.markdown("""
    <p style="color:#8b949e; font-size:13px; margin-top:6px;">
        A single dataset may contain data from one match or multiple matches combined.
    </p>
    """, unsafe_allow_html=True)

    if st.button("Confirm Upload", use_container_width=True):
        st.session_state.df2 = None
        notices = []

        if uploaded_files is None:
            notices.append(("error", "Please upload a dataset first."))
        else:
            files = uploaded_files if isinstance(uploaded_files, list) else [uploaded_files]
            if not files:
                notices.append(("error", "No dataset loaded."))
            else:
                try:
                    df = pd.concat([_read_uploaded(f) for f in files], ignore_index=True)
                    data_validation(df)
                    notices.append(("success", f"Dataset passed data validation | {df.shape[0]} rows loaded"))
                    st.session_state.df2 = process_data(df)
                    notices.append(("success", "Data cleaning and feature engineering completed."))
                except Exception as err:
                    st.session_state.df2 = None
                    notices.append(("error", f"Dataset is invalid: {err}"))

        # Other tabs depend on df2, so refresh the whole app once and show the messages there
        st.session_state.upload_notices = notices
        st.rerun()

    for kind, msg in st.session_state.pop("upload_notices", []):
        getattr(st, kind)(msg)


# ─────────────────────────────────────────────────────────────
# TAB 2 — BATTING ANALYTICS
# ─────────────────────────────────────────────────────────────
@fragment
def runs_per_match_section(done_batting):
    players = sorted(done_batting["Player_Name"].unique())
    selected = st.selectbox("Select Player", players, key="batting_runs_player_select")

    player_runs = (
        done_batting[done_batting["Player_Name"] == selected]
        .groupby("Match_No")["Runs_Scored"].sum().reset_index().sort_values("Match_No")
    )
    player_runs["Runs_Scored"] = player_runs["Runs_Scored"].astype(int)
    player_runs.index += 1
    show_table(player_runs)

    line_chart(player_runs["Match_No"].astype(int), player_runs["Runs_Scored"],
               f"{selected}'s Total Runs in Each Match", "Match No", "Runs Scored", "#c9a84c")


def render_batting_tab(df2):
    s = compute_team_stats(df2)

    # ── Individual runs ──
    section_heading("🏏", "Individual Runs Scored by Players")
    description("Total runs scored based on balls faced by each player across all matches, "
                "sorted from highest to lowest scorer.")
    runs_difference = one_based(s["runs_by_player"])
    show_table(runs_difference[["Player_Name", "Runs_Scored", "Balls_Played"]])
    bar_chart(runs_difference["Runs_Scored"], runs_difference["Player_Name"],
              "Individual Runs Scored by Players", "Runs Scored", "Players",
              sns.color_palette(BATTING_CMAP, len(runs_difference)), "x", (BAR_W, BAR_H))

    st.divider()

    # ── Runs contribution pie ──
    section_heading("📊", "Total Runs Contribution")
    description("Contribution of runs scored by each player to the team's total runs across all matches.")
    batting_data = s["batting_pie"]
    show_table(batting_data)
    pie_chart(batting_data["Runs_Scored"],
              pie_labels(batting_data["Player_Name"], batting_data["Runs_Scored"]),
              "Players", "Total Runs Contribution",
              sns.color_palette("YlOrRd", len(batting_data)))

    st.divider()

    # ── Runs per match ──
    section_heading("📈", "Player's Total Runs in Each Match")
    description("Total runs scored by each player in each match, allows tracking of performance "
                "trends across matches by selecting the player.")
    done_batting = df2[df2["Balls_Played"] > 0]
    if done_batting["Match_No"].nunique() > 1:
        runs_per_match_section(done_batting)
    else:
        st.warning("Player's Total Runs in Each Match is not applicable for a single-match dataset.")

    st.divider()

    # ── Runs by role ──
    section_heading("🎭", "Runs Scored Contribution Based on Roles")
    description("Total runs scored by players based on their roles (batsman, bowler, all-rounder) across all matches.")
    role_df = s["runs_role"]
    show_table(one_based(role_df))
    pie_chart(role_df["Runs_Scored"], pie_labels(role_df["Role"], role_df["Runs_Scored"]),
              "Roles", "Runs Scored Contribution Based on Roles",
              ROLE_BAT_COLORS[:len(role_df)])

    st.divider()

    # ── Strike rate comparison ──
    section_heading("⚡", "Strike-Rate Comparison — Batsmen vs All-Rounders")
    description("Comparison of strike rates between batsmen and all-rounders for players who have "
                "played 10 or more balls, to identify who is scoring faster.")
    if s["bat_ar_empty"]:
        st.warning("No batsmen or all-rounders found in the dataset.")
    else:
        sr = s["strike_rate"]
        sr = one_based(sr[sr["Balls_Played"] >= 10].reset_index(drop=True))
        show_table(sr[["Player_Name", "Role", "Strike_Rate"]])
        bar_chart(sr["Strike_Rate"], sr["Player_Name"],
                  "Strike-Rate Comparison — Batsmen vs All-Rounders", "Strike Rate", "Players",
                  SR_ROLE_COLORS, "x", (BAR_W, BAR_H), hue=sr["Role"])

    st.divider()

    # ── Batting consistency ──
    section_heading("📉", "Players Consistency in Batting")
    description("A consistency score for each player based on their average runs scored and variability across matches.")
    state = s["bat_consistency_state"]
    if state == "single":
        st.warning("Players Consistency in Batting is not applicable for a single-match dataset.")
    elif state == "unique":
        st.warning("The dataset only consists unique players in each match, Players consistency cannot be calculated without same player appearing in multiple matches.")
    else:
        bc = s["bat_consistency"]
        show_table(bc)
        bar_chart(bc["Consistency_Score"], bc["Player_Name"],
                  "Players Consistency in Batting", "Consistency Score", "Players",
                  sns.color_palette(BATTING_CMAP, len(bc)), "x", (BAR_W, BAR_H))

    st.divider()

    # ── Runs by batting order ──
    section_heading("🔢", "Total Runs by Batting Order")
    description("Total runs scored by players based on the batting order (top, middle, lower) across all matches.")
    order_runs = one_based(s["order_runs"])
    show_table(order_runs)
    bar_chart(order_runs["Batting_Order"], order_runs["Total_Runs_Scored"],
              "Total Runs by Batting Order", "Batting Order", "Total Runs Scored",
              ORDER_PAL, "y", (LINE_W, BAR_H))

    st.divider()

    # ── Average runs by batting order ──
    section_heading("📐", "Average Runs by Batting Order")
    description("Average runs scored per batting innings by players in each batting order group "
                "(top, middle, lower), counting only innings where the player actually batted.")
    order_avg = one_based(s["order_avg_runs"])
    show_table(order_avg)
    bar_chart(order_avg["Batting_Order"], order_avg["Average_Runs_Scored"],
              "Average Runs by Batting Order", "Batting Order", "Average Runs Scored",
              ORDER_PAL, "y", (LINE_W, BAR_H))

    st.divider()

    # ── Phase-wise wickets lost ──
    section_heading("🔻", "Phase-wise Wickets Lost Breakdown")
    description("Total wickets lost by the team in each match phase (powerplay, middle overs, death overs).")
    phase_wickets = one_based(s["phase_wickets"])
    show_table(phase_wickets)

    fig, ax = plt.subplots(figsize=(LINE_W, BAR_H), dpi=120)
    phase_pal = [PHASE_COLOR_MAP.get(p, "#8b949e") for p in phase_wickets["Wicket_Phase"]]
    sns.barplot(x=phase_wickets["Wicket_Phase"], y=phase_wickets["Wickets_Lost"], palette=phase_pal, ax=ax)
    ax.set_title("Phase-wise Wickets Lost", fontsize=14, fontweight="bold")
    ax.set_xlabel("Match Phases", fontsize=11)
    ax.set_ylabel("Wickets Lost", fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    handles = [mpatches.Patch(color=v, label=k) for k, v in PHASE_COLOR_MAP.items()]
    ax.legend(handles=handles, title="Phase", fontsize=9, framealpha=1.0, edgecolor="#000000",
              facecolor="#ffffff", labelcolor="#000000")
    ax.get_legend().get_title().set_color("#000000")
    _finish(fig)

    bottom_space()


# ─────────────────────────────────────────────────────────────
# TAB 3 — BOWLING ANALYTICS
# ─────────────────────────────────────────────────────────────
@fragment
def wickets_per_match_section(done_bowling):
    players = sorted(done_bowling["Player_Name"].unique())
    selected = st.selectbox("Select Player", players, key="bowling_wickets_player_select")

    player_wickets = (
        done_bowling[done_bowling["Player_Name"] == selected]
        .groupby("Match_No")["Wickets_Taken"].sum().reset_index().sort_values("Match_No")
    )
    player_wickets["Wickets_Taken"] = player_wickets["Wickets_Taken"].astype(int)
    player_wickets.index += 1
    show_table(player_wickets)

    line_chart(player_wickets["Match_No"].astype(int), player_wickets["Wickets_Taken"].astype(int),
               f"{selected}'s Total Wickets in Each Match", "Match No", "Wickets Taken", "#2dd4bf")


def render_bowling_tab(df2):
    s = compute_team_stats(df2)

    # ── Individual wickets ──
    section_heading("⚾", "Individual Wickets Taken by Players")
    description("Total wickets taken based on overs bowled by each player across all matches, "
                "sorted from highest to lowest wicket-taker.")
    bowling_diff = one_based(s["bowl_by_player"])
    show_table(bowling_diff)
    bar_chart(bowling_diff["Wickets_Taken"], bowling_diff["Player_Name"],
              "Individual Wickets Taken by Players", "Wickets Taken", "Players",
              sns.color_palette(BOWLING_CMAP, len(bowling_diff)), "x", (BAR_W, BAR_H))

    st.divider()

    # ── Wickets contribution pie ──
    section_heading("📊", "Total Wickets Contribution")
    description("Contribution of total wickets taken by each player to the team's total wickets across all matches.")
    bowling_data = s["bowling_pie"]
    show_table(bowling_data)
    pie_chart(bowling_data["Wickets_Taken"],
              pie_labels(bowling_data["Player_Name"], bowling_data["Wickets_Taken"]),
              "Players", "Total Wickets Contribution",
              sns.color_palette("YlGnBu", len(bowling_data)))

    st.divider()

    # ── Wickets per match ──
    section_heading("📈", "Player's Total Wickets in Each Match")
    description("Total wickets taken by each player in each match, allows tracking of performance "
                "trends across matches by selecting the player.")
    done_bowling = df2[df2["Overs_Bowled"] > 0]
    if done_bowling["Match_No"].nunique() > 1:
        wickets_per_match_section(done_bowling)
    else:
        st.warning("Player's Total Wickets in Each Match is not applicable for a single-match dataset.")

    st.divider()

    # ── Wickets by role ──
    section_heading("🎭", "Wickets Taken Contribution Based on Roles")
    description("Total wickets taken by players based on their roles (batsman, bowler, all-rounder) across all matches.")
    role_df = s["wickets_role"]
    show_table(one_based(role_df))
    pie_chart(role_df["Wickets_Taken"], pie_labels(role_df["Role"], role_df["Wickets_Taken"]),
              "Roles", "Wickets Taken Contribution Based on Roles",
              ROLE_BOWL_COLORS[:len(role_df)])

    st.divider()

    # ── Average wickets by role ──
    section_heading("📐", "Average Wickets by Role")
    description("Average wickets taken per bowling innings by players of each role "
                "(batsman, bowler, all-rounder), counting only innings where the player actually bowled.")
    role_avg = one_based(s["wickets_role_avg"])
    show_table(role_avg)
    bar_chart(role_avg["Role"], role_avg["Average_Wickets_Taken"],
              "Average Wickets by Role", "Role", "Average Wickets Taken",
              ROLE_BOWL_COLORS[:len(role_avg)], "y", (LINE_W, BAR_H))

    st.divider()

    # ── Economy rate comparison ──
    section_heading("💰", "Economy-Rate Comparison — Bowlers vs All-Rounders")
    description("Comparison of economy rates between bowlers and all-rounders for players who have "
                "bowled 2 or more overs, to identify who is conceding runs at a lower rate.")
    if s["bowl_ar_empty"]:
        st.warning("No bowlers or all-rounders found in the dataset.")
    else:
        eco = s["economy"]
        eco = one_based(eco[eco["Balls_Bowled"] >= 12].reset_index(drop=True))
        show_table(eco[["Player_Name", "Role", "Economy_Rate"]])
        bar_chart(eco["Economy_Rate"], eco["Player_Name"],
                  "Economy-Rate Comparison — Bowlers vs All-Rounders", "Economy Rate", "Players",
                  ECO_ROLE_COLORS, "x", (BAR_W, BAR_H), hue=eco["Role"])

    st.divider()

    # ── Bowling consistency ──
    section_heading("📉", "Players Consistency in Bowling")
    description("A consistency score for each player based on their average wickets taken and variability across matches.")
    state = s["bowl_consistency_state"]
    if state == "single":
        st.warning("Players Consistency in Bowling is not applicable for a single-match dataset.")
    elif state == "unique":
        st.warning("The dataset only consists unique players in each match, Players consistency cannot be calculated without same player appearing in multiple matches.")
    else:
        bc = s["bowl_consistency"]
        show_table(bc)
        bar_chart(bc["Consistency_Score"], bc["Player_Name"],
                  "Players Consistency in Bowling", "Consistency Score", "Players",
                  sns.color_palette(BOWLING_CMAP, len(bc)), "x", (BAR_W, BAR_H))

    bottom_space()


# ─────────────────────────────────────────────────────────────
# TAB 4 — PLAYER ANALYTICS (whole tab is a fragment: changing the
# player or match only re-runs this tab)
# ─────────────────────────────────────────────────────────────
@fragment
def render_player_tab(df2):
    pm_all = compute_player_match_stats(df2)

    description("Select a player to view their individual batting and bowling performance across all matches.",
                margin="4px 0 10px 0")

    all_players = sorted(df2["Player_Name"].unique())
    player = st.selectbox("Select Player", all_players, key="player_analytics_select_player")

    player_df = df2[df2["Player_Name"] == player]
    pm = pm_all[pm_all["Player_Name"] == player].reset_index(drop=True)

    role = player_df["Role"].mode().iloc[0]
    matches_played = player_df["Match_No"].nunique()

    avg_position = int(round(player_df["Batting_Position"].mean()))
    order_label = "top" if avg_position <= 3 else "middle" if avg_position <= 7 else "lower"

    has_batted = (pm["Balls_Played"] > 0).any()
    has_bowled = (pm["Balls_Bowled"] > 0).any()
    total_runs = int(pm["Runs_Scored"].sum())
    total_wickets = int(pm["Wickets_Taken"].sum())

    st.markdown(f"""
    <div style="font-family:'Rajdhani',sans-serif; font-weight:700;
                font-size:24px; color:#e0c070; margin:14px 0 12px 0;
                letter-spacing:0.4px;">
        🔎 {player}'s Information
    </div>
    """, unsafe_allow_html=True)

    insight_line(1, f"Selected player is a <strong>{role.title()}</strong>, based on the role they have.")
    insight_line(2, f"The player has played <strong>{matches_played}</strong> match(es).")
    insight_line(3, f"Usually bats at the <strong>{order_label} order</strong>.")
    if has_batted:
        insight_line(4, f"The player has scored <strong>{total_runs} runs</strong>.")
    if has_bowled:
        insight_line(5, f"The player has taken <strong>{total_wickets} wickets</strong>.")

    st.divider()

    # ════════════ BATTING ════════════
    section_heading("🏏", f"{player}'s Individual Batting Stats")
    description("A detailed match-by-match breakdown of the selected player's batting "
                "performance, including runs, strike rate, and contribution to the team's total.")

    if not has_batted:
        st.warning("The player has not done batting in any match, so we cannot present the batting insights for selected player.")
    else:
        mb = pm[["Match_No", "Runs_Scored", "Balls_Played"]].copy()
        mb["Strike_Rate"] = np.where(
            mb["Balls_Played"] > 0,
            mb["Runs_Scored"] / mb["Balls_Played"].where(mb["Balls_Played"] > 0, 1) * 100, 0.0
        ).round(2)
        mb.index = mb.index + 1

        batted = mb[mb["Balls_Played"] > 0]
        bat_consistency = (
            round(batted["Runs_Scored"].mean() / (batted["Runs_Scored"].std() + 1), 2)
            if len(batted) > 1 else None
        )
        total_balls = int(mb["Balls_Played"].sum())
        overall_sr = round((total_runs / total_balls) * 100, 2) if total_balls > 0 else 0.0

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            kpi_card("🏏", "Total Runs", f"{total_runs}")
        with k2:
            kpi_card("🎯", "Balls Played", f"{total_balls}")
        with k3:
            kpi_card("⚡", "Strike Rate", f"{overall_sr}")
        with k4:
            kpi_card("📉", "Batting Consistency", f"{bat_consistency}" if bat_consistency is not None else "N/A")

        st.divider()

        match_nos = mb["Match_No"].astype(int)

        section_heading("📊", f"{player}'s Runs in Each Match")
        description("Match-by-match runs scored by the player, based on the number of balls faced.")
        show_table(mb[["Match_No", "Runs_Scored", "Balls_Played"]])
        bar_chart(match_nos, mb["Runs_Scored"], f"{player}'s Runs in Each Match",
                  "Match No", "Runs Scored", sns.color_palette(PLAYER_BAT_CMAP, len(mb)), "y",
                  (BAR_W, BAR_H), integer_y=True)

        st.divider()

        section_heading("⚡", f"{player}'s Strike Rate in Each Match")
        description("Match-by-match strike rate of the player, indicating how quickly they have been scoring runs.")
        show_table(mb[["Match_No", "Strike_Rate"]])
        line_chart(match_nos, mb["Strike_Rate"], f"{player}'s Strike Rate in Each Match",
                   "Match No", "Strike Rate", PLAYER_BAT_LINE_COLOR)

        st.divider()

        section_heading("🥧", f"{player}'s Runs Contribution in a Match")
        description("Contribution of the selected player's runs to the team's total in a chosen "
                    "match, compared to the rest of the batting line-up.")
        selected_match = st.selectbox("Select Match", sorted(match_nos.unique()),
                                      key="player_analytics_batting_match_select")
        match_rows = pm_all[pm_all["Match_No"] == selected_match]
        match_rows = match_rows[match_rows["Balls_Played"] > 0]
        team_runs = int(match_rows["Runs_Scored"].sum())
        player_runs = int(match_rows.loc[match_rows["Player_Name"] == player, "Runs_Scored"].sum())
        pie_df = pd.DataFrame({"Label": [player, "Others"], "Runs": [player_runs, team_runs - player_runs]})
        pie_df = pie_df[pie_df["Runs"] > 0]

        if pie_df.empty:
            st.info(f"{player} did not score any runs in Match {selected_match}.")
        else:
            show_table(pie_df)
            pie_chart(pie_df["Runs"], pie_labels(pie_df["Label"], pie_df["Runs"]), "Players",
                      f"{player}'s Runs Contribution — Match {selected_match}",
                      sns.color_palette(PLAYER_BAT_CMAP, len(pie_df)))

        st.divider()

        section_heading("🎯", f"{player}'s Run Contribution Against the Team")
        description("Contribution of the selected player's total runs to the team's overall runs scored across all matches.")
        team_total_runs = int(pm_all.loc[pm_all["Balls_Played"] > 0, "Runs_Scored"].sum())
        pie_df = pd.DataFrame({"Label": [player, "Others"], "Runs": [total_runs, team_total_runs - total_runs]})
        pie_df = pie_df[pie_df["Runs"] > 0]

        if pie_df.empty:
            st.info(f"{player} has not scored any runs across all matches.")
        else:
            show_table(pie_df)
            pie_chart(pie_df["Runs"], pie_labels(pie_df["Label"], pie_df["Runs"]), "Players",
                      f"{player}'s Run Contribution Against the Team",
                      sns.color_palette(PLAYER_BAT_CMAP, len(pie_df)))

    st.divider()

    # ════════════ BOWLING ════════════
    section_heading("⚾", f"{player}'s Individual Bowling Stats")
    description("A detailed match-by-match breakdown of the selected player's bowling "
                "performance, including wickets, economy rate, and contribution to the team's total.")

    if not has_bowled:
        st.warning("The player has not done bowling in any match, so we cannot present the bowling insights for selected player.")
    else:
        mw = pm[["Match_No", "Wickets_Taken", "Runs_Given", "Balls_Bowled"]].copy()
        mw["Overs_Bowled"] = balls_to_overs(mw["Balls_Bowled"])
        mw["Economy_Rate"] = np.where(
            mw["Balls_Bowled"] > 0,
            mw["Runs_Given"] / (mw["Balls_Bowled"].where(mw["Balls_Bowled"] > 0, 1) / 6), 0.0
        ).round(2)
        mw.index = mw.index + 1

        bowled = mw[mw["Balls_Bowled"] > 0]
        bowl_consistency = (
            round(bowled["Wickets_Taken"].mean() / (bowled["Wickets_Taken"].std() + 1), 2)
            if len(bowled) > 1 else None
        )
        total_balls_bowled = int(mw["Balls_Bowled"].sum())
        total_overs = float(balls_to_overs(total_balls_bowled))
        overall_eco = round(float(mw["Runs_Given"].sum()) / (total_balls_bowled / 6), 2) if total_balls_bowled > 0 else 0.0

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            kpi_card("⚾", "Total Wickets", f"{total_wickets}")
        with k2:
            kpi_card("🎯", "Overs Bowled", f"{total_overs}")
        with k3:
            kpi_card("💰", "Economy Rate", f"{overall_eco}")
        with k4:
            kpi_card("📉", "Bowling Consistency", f"{bowl_consistency}" if bowl_consistency is not None else "N/A")

        st.divider()

        match_nos = mw["Match_No"].astype(int)

        section_heading("📊", f"{player}'s Wickets in Each Match")
        description("Match-by-match wickets taken by the player, based on the overs bowled.")
        show_table(mw[["Match_No", "Wickets_Taken", "Overs_Bowled"]])
        bar_chart(match_nos, mw["Wickets_Taken"], f"{player}'s Wickets in Each Match",
                  "Match No", "Wickets Taken", sns.color_palette(PLAYER_BOWL_CMAP, len(mw)), "y",
                  (BAR_W, BAR_H), integer_y=True)

        st.divider()

        section_heading("💰", f"{player}'s Economy Rate in Each Match")
        description("Match-by-match economy rate of the player, indicating how many runs they have conceded per over.")
        show_table(mw[["Match_No", "Economy_Rate"]])
        line_chart(match_nos, mw["Economy_Rate"], f"{player}'s Economy Rate in Each Match",
                   "Match No", "Economy Rate", PLAYER_BOWL_LINE_COLOR)

        st.divider()

        section_heading("🥧", f"{player}'s Wickets Contribution in a Match")
        description("Contribution of the selected player's wickets to the team's total in a chosen "
                    "match, compared to the rest of the bowling attack.")
        selected_match = st.selectbox("Select Match", sorted(match_nos.unique()),
                                      key="player_analytics_bowling_match_select")
        match_rows = pm_all[pm_all["Match_No"] == selected_match]
        match_rows = match_rows[match_rows["Balls_Bowled"] > 0]
        team_wkts = int(match_rows["Wickets_Taken"].sum())
        player_wkts = int(match_rows.loc[match_rows["Player_Name"] == player, "Wickets_Taken"].sum())
        pie_df = pd.DataFrame({"Label": [player, "Others"], "Wickets": [player_wkts, team_wkts - player_wkts]})
        pie_df = pie_df[pie_df["Wickets"] > 0]

        if pie_df.empty:
            st.info(f"{player} did not take any wickets in Match {selected_match}.")
        else:
            show_table(pie_df)
            pie_chart(pie_df["Wickets"], pie_labels(pie_df["Label"], pie_df["Wickets"]), "Players",
                      f"{player}'s Wickets Contribution — Match {selected_match}",
                      sns.color_palette(PLAYER_BOWL_CMAP, len(pie_df)))

        st.divider()

        section_heading("🎯", f"{player}'s Wicket Contribution Against the Team")
        description("Contribution of the selected player's total wickets to the team's overall wickets taken across all matches.")
        team_total_wkts = int(pm_all.loc[pm_all["Balls_Bowled"] > 0, "Wickets_Taken"].sum())
        pie_df = pd.DataFrame({"Label": [player, "Others"], "Wickets": [total_wickets, team_total_wkts - total_wickets]})
        pie_df = pie_df[pie_df["Wickets"] > 0]

        if pie_df.empty:
            st.info(f"{player} has not taken any wickets across all matches.")
        else:
            show_table(pie_df)
            pie_chart(pie_df["Wickets"], pie_labels(pie_df["Label"], pie_df["Wickets"]), "Players",
                      f"{player}'s Wicket Contribution Against the Team",
                      sns.color_palette(PLAYER_BOWL_CMAP, len(pie_df)))

    bottom_space()


# ─────────────────────────────────────────────────────────────
# TAB 5 — SUMMARY
# ─────────────────────────────────────────────────────────────
def _nth(df, n, col, default="N/A"):
    return df.iloc[n][col] if len(df) > n else default


def render_summary_tab(df2):
    s = compute_team_stats(df2)

    runs_by_player = s["runs_by_player"]
    bowl_by_player = s["bowl_by_player"]
    # same filters as the Batting / Bowling tabs: >= 10 balls faced, >= 2 overs (12 balls) bowled
    strike_rate = s["strike_rate"]
    strike_rate = strike_rate[strike_rate["Balls_Played"] >= 10].reset_index(drop=True)
    economy = s["economy"]
    economy = economy[economy["Balls_Bowled"] >= 12].reset_index(drop=True)
    runs_role = s["runs_role"]
    wickets_role = s["wickets_role"]
    order_runs = s["order_runs"]
    phase_wickets = s["phase_wickets"]

    top_scorer       = _nth(runs_by_player, 0, "Player_Name")
    top_scorer_runs  = int(_nth(runs_by_player, 0, "Runs_Scored", 0))
    top_scorer_balls = int(_nth(runs_by_player, 0, "Balls_Played", 0))
    top_wicket_taker   = _nth(bowl_by_player, 0, "Player_Name")
    top_wicket_taker_w = int(_nth(bowl_by_player, 0, "Wickets_Taken", 0))
    top_sr_player = _nth(strike_rate, 0, "Player_Name")
    top_sr_value  = _nth(strike_rate, 0, "Strike_Rate", 0)
    top_eco_player = _nth(economy, 0, "Player_Name")
    top_eco_value  = _nth(economy, 0, "Economy_Rate", 0)

    runs_role_1, runs_role_1_val = _nth(runs_role, 0, "Role"), _nth(runs_role, 0, "Runs_Scored", 0)
    runs_role_2, runs_role_2_val = _nth(runs_role, 1, "Role"), _nth(runs_role, 1, "Runs_Scored", 0)
    wkt_role_1, wkt_role_1_val = _nth(wickets_role, 0, "Role"), _nth(wickets_role, 0, "Wickets_Taken", 0)
    wkt_role_2, wkt_role_2_val = _nth(wickets_role, 1, "Role"), _nth(wickets_role, 1, "Wickets_Taken", 0)

    top_order    = _nth(order_runs, 0, "Batting_Order")
    second_order = _nth(order_runs, 1, "Batting_Order")

    top_phase      = _nth(phase_wickets, 0, "Wicket_Phase")
    top_phase_wkts = int(_nth(phase_wickets, 0, "Wickets_Lost", 0))

    # ── Runs & Wickets per match chart ──
    section_heading("📊", "Total Runs Scored and Wickets Taken in Each Match")
    description("Total runs scored and wickets taken by the team in each match.")

    runs_wickets = one_based(s["runs_wickets"])
    show_table(runs_wickets[["Match_No", "Runs_Scored", "Wickets_Taken"]])

    fig, ax = plt.subplots(1, 2, figsize=(SIDE_W, SIDE_H), dpi=120)
    n_matches = len(runs_wickets)

    sns.barplot(x=runs_wickets["Match_No"], y=runs_wickets["Runs_Scored"],
                palette=sns.color_palette(BATTING_CMAP, n_matches), ax=ax[0])
    ax[0].set_xlabel("Match Number", fontsize=11)
    ax[0].set_ylabel("Runs Scored", fontsize=11)
    ax[0].set_title("Runs Scored in Each Match", fontsize=12, fontweight="bold")
    ax[0].grid(axis="y", linestyle="--", alpha=0.4)

    sns.barplot(x=runs_wickets["Match_No"], y=runs_wickets["Wickets_Taken"],
                palette=sns.color_palette(BOWLING_CMAP, n_matches), ax=ax[1])
    ax[1].set_xlabel("Match Number", fontsize=11)
    ax[1].set_ylabel("Wickets Taken", fontsize=11)
    ax[1].set_title("Wickets Taken in Each Match", fontsize=12, fontweight="bold")
    ax[1].grid(axis="y", linestyle="--", alpha=0.4)
    _finish(fig)

    st.divider()

    # ── KPI cards ──
    sub_heading("🏆 Top Performers", size=24, margin="6px 0 14px 0", tag="div", spacing="0.4px")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("🏏", "Top Run Scorer", f"{top_scorer}", f"{top_scorer_runs} runs off {top_scorer_balls} balls")
    with c2:
        kpi_card("⚾", "Top Wicket Taker", f"{top_wicket_taker}", f"{top_wicket_taker_w} wickets")
    with c3:
        kpi_card("⚡", "Best Strike Rate", f"{top_sr_player}", f"SR: {top_sr_value}")
    with c4:
        kpi_card("💰", "Best Econ. Rate", f"{top_eco_player}", f"ER: {top_eco_value}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # ── Narrative insights ──
    sub_heading("📋 Team Performance Summary", size=22, margin="10px 0 12px 0", tag="div")

    insight_line(1, f"<strong>{top_scorer}</strong> is the highest run scorer with <strong>{top_scorer_runs} runs</strong>.")
    insight_line(2, f"<strong>{top_wicket_taker}</strong> is the highest wicket taker with <strong>{top_wicket_taker_w} wickets</strong>.")
    insight_line(3, f"<strong>{top_sr_player}</strong> has the highest strike rate of <strong>{top_sr_value}</strong>.")
    insight_line(4, f"<strong>{top_eco_player}</strong> has the best bowling economy rate of <strong>{top_eco_value}</strong>.")
    insight_line(5, f"<strong>{runs_role_1}s</strong> are the highest contributors in scoring runs with <strong>{runs_role_1_val} runs</strong>, followed by <strong>{runs_role_2}s</strong> with <strong>{runs_role_2_val} runs</strong>.")
    insight_line(6, f"<strong>{wkt_role_1}s</strong> are the highest contributors in taking wickets with <strong>{wkt_role_1_val} wickets</strong>, followed by <strong>{wkt_role_2}s</strong> with <strong>{wkt_role_2_val} wickets</strong>.")
    insight_line(7, f"The <strong>{top_order} order</strong> is the strongest batting unit, followed by the <strong>{second_order} order</strong>.")
    insight_line(8, f"The team has lost the most wickets in the <strong>{top_phase}</strong>, losing <strong>{top_phase_wkts} wickets</strong>.")

    bottom_space()


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:12px 0 8px 0;'>
        <span style="font-family:'Rajdhani',sans-serif; font-size:28px;
                     font-weight:700; color:#c9a84c; letter-spacing:1px;">
            🏏 Tool Menu
        </span>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("", ["Analyze your Dataset", "About"])

    st.markdown("<hr style='border-color:#2a3444; margin:12px 0;'>", unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:'Rajdhani',sans-serif; font-size:13px;
                color:#8b949e; line-height:1.9; padding:4px 0;">
        <strong style="color:#c9a84c;">Current Version:</strong> 2.1<br>
        <strong style="color:#c9a84c;">Last Updated:</strong> 16th September 2026<br>
        <strong style="color:#c9a84c;">Initial Release:</strong> 27th February 2026
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# MAIN PAGE
# ─────────────────────────────────────────────────────────────
left, center, right = st.columns([1, 3, 1])

with center:

    # ══════════════════════════════════════════════════════
    # ANALYZE PAGE
    # ══════════════════════════════════════════════════════
    if page == "Analyze your Dataset":

        render_header()
        st.markdown("")

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📊 Dataset", "🏏 Batting Analytics", "⚾ Bowling Analytics",
             "🎯 Player Analytics", "📋 Summary"]
        )

        # ── TAB 1 — DATASET ──
        with tab1:
            st.markdown("""
            <p style="color:#8b949e; font-size:13px; margin:6px 0 4px 0;">
                Supports <code style="color:#2dd4bf;">.csv</code> and
                <code style="color:#2dd4bf;">.xlsx</code> file formats
            </p>
            """, unsafe_allow_html=True)

            st.download_button("⬇ Download Template Dataset", read_file_bytes("template.csv"), "template.csv")

            st.markdown("""
            <p style="color:#8b949e; font-size:13px;">
                Download the template, fill in your match data, and upload it below.
            </p>
            """, unsafe_allow_html=True)

            st.divider()

            sub_heading("Upload Your Files", margin="4px 0 8px 0")
            st.markdown("""
            <p style="color:#8b949e; font-size:13px; margin-bottom:10px;">
                For testing refer to the example dataset attached below.
            </p>
            """, unsafe_allow_html=True)

            upload_section()

            st.divider()

            sub_heading("Data Validation Rules")

            with st.expander("🙎 Match & Player Info Columns", expanded=False):
                column_info("Match_No",
                    "The match number this player's performance belongs to. "
                    "Use 1 for your first match, 2 for your second, and so on. "
                    "Every row must have a match number — blank values are NOT allowed. "
                    "Preferred datatype: Integer (whole number, e.g. 1, 2, 3).")

                column_info("Player_Name",
                    "The full name or short name of the player. Every row must have a name — "
                    "blank values are NOT allowed. Use the same spelling consistently across all matches; "
                    "for example do not write 'Virat Kohli' in one match and 'V Kohli' in another, "
                    "as the tool will treat them as two different players. "
                    "Preferred datatype: Text (e.g. Rohit Sharma).")

                column_info("Role",
                    "The player's role in the team. Accepted values are: batsman, bowler, all-rounder, wicketkeeper. "
                    "Capitalisation do not matter — 'Batsman', 'BATSMAN', and 'batsman' are all accepted. However, spelling must be consistent same as the accepted values. "
                    "Blank values are allowed and will be auto-filled with the most common role in the dataset. "
                    "Important: A wicketkeeper who also bats can be entered as wicketkeeper or batsman. If entered wicketkeeper, they will be treated as a batsman for batting stats. "
                    "Preferred datatype: Text.")

            with st.expander("🏏 Batting Info Columns", expanded=False):
                column_info("Batting_Position",
                    "The position at which this player came in to bat, from 1 (opener) to 11 (last). "
                    "Every row must have a batting position — blank values are NOT allowed. "
                    "If two players opened the batting, one gets position 1 and the other gets position 2. "
                    "Do not repeat the same position number for two players in the same match. "
                    "Preferred datatype: Integer (whole number from 1 to 11).")

                column_info("Batting_Start_Over",
                    "The over number when this player walked in to bat. "
                    "For example, if a player came in during over 4, enter 4. "
                    "If they came in mid-over (e.g. during the 3rd ball of over 6), you can enter 6.3. "
                    "Leave this blank ONLY if the player did not bat at all in that match. "
                    "This value must always be less than or equal to Out_Over. "
                    "Preferred datatype: Numeric (e.g. 1, 4, 6.3).")

                column_info("Out_Over",
                    "The over number when this player got out. "
                    "For example, if a player was dismissed in over 14, enter 14. "
                    "If the player was NOT OUT (finished the innings without getting dismissed), "
                    "leave this blank or write 'not-out' — both are accepted. "
                    "This value must always be greater than or equal to Batting_Start_Over. "
                    "Cannot exceed 20 (this tool only supports T20 matches). "
                    "Preferred datatype: Numeric or leave blank / write not-out for not-out players.")

                column_info("Balls_Played",
                    "The total number of balls this player faced during their innings. "
                    "For example, if a player faced 34 balls, enter 34. "
                    "Leave blank ONLY if the player did not bat. "
                    "If a player batted but faced 0 balls (extremely rare), enter 0. "
                    "Must be filled if Batting_Start_Over is filled. "
                    "Preferred datatype: Integer (whole number).")

                column_info("Runs_Scored",
                    "The total runs scored by this player in their innings, including extras attributed to them. "
                    "If a player got out for a duck (0 runs), enter 0 — do not leave blank. "
                    "Leave blank ONLY if the player did not bat at all. "
                    "Must be filled if Batting_Start_Over is filled. "
                    "Preferred datatype: Integer (whole number, e.g. 0, 45, 102).")

            with st.expander("⚾ Bowling Info Columns", expanded=False):
                column_info("Overs_Bowled",
                    "The total overs bowled by this player in the match. "
                    "For complete overs, enter a whole number (e.g. 4). "
                    "For partial overs, use one decimal place where the digit after the decimal is the number of balls bowled — "
                    "for example, 3.4 means 3 complete overs and 4 balls (NOT 3.4 overs mathematically). "
                    "Valid ball values after the decimal are 1 through 5 only — "
                    "for example 2.6 is invalid because an over only has 6 balls and .6 would mean a complete over. "
                    "Leave blank or enter 0 if the player did not bowl. "
                    "Preferred datatype: Numeric (e.g. 2, 3.4, 4.0).")

                column_info("Runs_Given",
                    "The total runs conceded by this player while bowling (excluding extras not attributed to the bowler). "
                    "If the player bowled but gave 0 runs, enter 0. "
                    "Leave blank ONLY if the player did not bowl — blank values are auto-filled to 0 during cleaning "
                    "for players who have Overs_Bowled filled. "
                    "Must be filled if Overs_Bowled is filled. "
                    "Preferred datatype: Integer (whole number, e.g. 0, 24, 56).")

                column_info("Wickets_Taken",
                    "The number of wickets taken by this player while bowling. "
                    "If the player bowled but took no wickets, enter 0 — do not leave blank. "
                    "Leave blank ONLY if the player did not bowl — blank values are auto-filled to 0 during cleaning "
                    "for players who have Overs_Bowled filled. "
                    "Must be filled if Overs_Bowled is filled. "
                    "The total wickets taken by all players in a single match cannot be more than 10. "
                    "Runouts are generally not credited to a bowler and should not be counted here. "
                    "Preferred datatype: Integer (whole number, e.g. 0, 1, 2, 3).")

            st.divider()

            sub_heading("Example Dataset", margin="4px 0 10px 0")

            st.download_button("⬇ Download Example Dataset", read_file_bytes("match_data.csv"), "match_data.csv")

            bottom_space()

        # ── TAB 2–5 — need an uploaded dataset ──
        df2 = st.session_state.df2
        tabs_and_renderers = [
            (tab2, render_batting_tab),
            (tab3, render_bowling_tab),
            (tab4, render_player_tab),
            (tab5, render_summary_tab),
        ]
        for tab, renderer in tabs_and_renderers:
            with tab:
                if df2 is None:
                    st.warning("Please upload and confirm your dataset in the Dataset tab first.")
                else:
                    renderer(df2)

    # ══════════════════════════════════════════════════════
    # ABOUT PAGE
    # ══════════════════════════════════════════════════════
    elif page == "About":

        render_header()
        st.divider()

        with st.expander("👨‍💻 About the Developer — Pranay Jha", expanded=False):
            st.markdown("""
            <div style="font-family:'Rajdhani',sans-serif; font-size:14px;
                        color:#e6edf3; line-height:1.8;">
                Hello! My name is <strong style="color:#e0c070;">Pranay Jha</strong>, and I am currently pursuing a
                <strong style="color:#e0c070;">Bachelor of Technology (B.Tech) in Computer Science and Engineering</strong>.<br><br>
                I am actively learning and exploring the fields of <strong style="color:#e0c070;">Data Science, Data Analytics,
                and Data Visualization</strong>.<br><br>
                This project — <strong style="color:#c9a84c;">Cricket Team Performance Analyzer</strong> — has been developed
                as part of my learning journey in data analytics. The main goal is to demonstrate how structured data analysis
                and interactive dashboards can evaluate sports performance effectively.<br><br>
                The tool uses Python libraries including <strong style="color:#2dd4bf;">NumPy, Pandas, Matplotlib, Seaborn,
                and Streamlit</strong>.
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            sub_heading("🚀 Key Highlights", size=17, margin="0 0 8px 0", color="#c9a84c")
            card_list([
                "Work with <strong>real-world structured datasets</strong>",
                "Perform <strong>data cleaning and feature engineering</strong>",
                "Build <strong>interactive analytical dashboards</strong>",
                "Communicate insights through <strong>data visualization</strong>",
                "Design <strong>user-friendly analytical tools</strong>",
            ], prefix="▸ &nbsp;")

            st.markdown("<br>", unsafe_allow_html=True)
            sub_heading("🔗 Connect With Me", size=17, margin="0 0 8px 0", color="#c9a84c")

            st.markdown("""
            <div style="display:flex; gap:14px; flex-wrap:wrap;">
                <a href="https://github.com/Pranay-256" target="_blank"
                   style="display:inline-flex; align-items:center; gap:8px;
                          background:#1c2330; border:1px solid #2a3444;
                          border-radius:8px; padding:10px 18px;
                          font-family:'Rajdhani',sans-serif; font-size:14px;
                          color:#e6edf3; text-decoration:none;
                          transition:border-color 0.2s;">
                    <span style="font-size:18px;">🐙</span>
                    <strong>GitHub</strong> — Pranay-256
                </a>
                <a href="https://www.linkedin.com/in/pranay-jha-6582a937b/" target="_blank"
                   style="display:inline-flex; align-items:center; gap:8px;
                          background:#1c2330; border:1px solid #2a3444;
                          border-radius:8px; padding:10px 18px;
                          font-family:'Rajdhani',sans-serif; font-size:14px;
                          color:#e6edf3; text-decoration:none;">
                    <span style="font-size:18px;">💼</span>
                    <strong>LinkedIn</strong> — Pranay Jha
                </a>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("❗ Problem Statement", expanded=False):
            st.markdown("""
            <div style="font-family:'Rajdhani',sans-serif; font-size:14px;
                        color:#e6edf3; line-height:1.8; margin-bottom:10px;">
                Advanced cricket analytics is available only at the top of the game. Professional teams use
                expensive analytical tools and dedicated analysts, but the vast majority of players do not have
                access to anything like it. In <strong style="color:#e0c070;">gully cricket, friendly and turf
                tournaments, inter-school and inter-college competitions, and small district-level or
                state-level tournaments</strong>, players, coaches and associations usually have
                <strong>no access to advanced and costly cricket analytics tools</strong>.
            </div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:14px;
                        color:#e6edf3; line-height:1.8; margin-bottom:10px;">
                As a result, performance is judged by <strong>memory, personal observation and a quick look at
                the scorecard</strong>. Coaches cannot easily see where the team is losing wickets or which role
                is contributing the most, and players cannot see how consistent they really are. This makes it
                hard to build better strategies for future matches, and it also makes awards open to
                <strong>bias, favouritism or even cheating</strong>, because there is no transparent data
                behind the decision.
            </div>
            """, unsafe_allow_html=True)

            sub_heading("⚠️ Key Challenges", size=17, margin="8px 0", color="#c9a84c")
            card_list([
                "Player contributions are often judged <strong>subjectively</strong>, based on opinion rather than numbers",
                "Awards like <strong>Best Batsman / Bowler</strong> may not be fairly decided, and can be influenced by bias or cheating",
                "Bowling performance is usually evaluated <strong>only by wickets</strong>, ignoring economy rate",
                "There is no way to measure <strong>player consistency</strong>, so one good match can hide an average player",
                "Coaches cannot easily see <strong>where the team loses wickets</strong> or which batting order scores the most",
                "<strong>Match-to-match comparison</strong> is difficult without proper records",
                "Lack of a <strong>structured data system</strong> for multi-match analysis",
                "Advanced analytics tools are <strong>expensive and complex</strong>, so grassroots teams cannot use them",
            ], border_color="#e05252")

        with st.expander("🎯 Objective", expanded=False):
            st.markdown("""
            <div style="font-family:'Rajdhani',sans-serif; font-size:14px;
                        color:#e6edf3; line-height:1.8; margin-bottom:10px;">
                The aim of this project is to provide a <strong style="color:#e0c070;">simple, free and easy-to-use
                analytical tool</strong> that gives gully cricketers, local and school teams, coaches and small
                tournament organizers the kind of team analysis that was earlier available only through advanced
                and expensive tools — replacing manual judgements with <strong>data-driven insights</strong>.
            </div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:14px;
                        color:#e6edf3; line-height:1.8; margin-bottom:10px;">
                Using this tool, <strong style="color:#e0c070;">players and coaches</strong> can analyze their team
                performance effectively, find strengths and weaknesses, and create better strategies to perform
                well in future matches. <strong style="color:#e0c070;">Organizations and associations</strong> can
                give awards <strong>accurately and fairly</strong>, without any bias or cheating against any
                player or in favour of another.
            </div>
            """, unsafe_allow_html=True)

            sub_heading("📊 Core Focus Areas", size=17, margin="8px 0", color="#c9a84c")
            card_list([
                "Measuring <strong>individual batting contribution</strong>",
                "Evaluating <strong>bowling impact</strong> using wickets and economy rate",
                "Measuring <strong>player consistency</strong> across multiple matches",
                "Comparing performances between <strong>batsmen, bowlers, and all-rounders</strong>",
                "Identifying team strengths and weaknesses, such as <strong>batting order strength and phase-wise wickets lost</strong>",
                "Giving a <strong>detailed match-by-match view of every individual player</strong>",
                "Providing <strong>fair statistical summaries</strong> for team evaluation and unbiased awards",
            ], border_color="#3fb950", prefix="✓ &nbsp;")

            sub_heading("🏏 Target Users", size=17, margin="8px 0", color="#c9a84c")
            targets = ["Gully cricket players", "Friendly & turf tournaments", "Inter-school & inter-college teams",
                       "District & state level tournaments", "Players & coaches", "Associations & award committees"]
            cols = st.columns(3)
            for i, t in enumerate(targets):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div style="background:#1c2330; border:1px solid #2a3444; border-radius:8px;
                                padding:8px 12px; margin-bottom:8px; text-align:center;
                                font-family:'Rajdhani',sans-serif; font-size:13px; color:#e6edf3;">
                        {t}
                    </div>
                    """, unsafe_allow_html=True)

        with st.expander("🛠️ Tech Stack", expanded=False):
            st.markdown("""
            <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#e6edf3;
                      line-height:1.8; margin-bottom:10px;">
                Built using the <strong style="color:#e0c070;">Python data analytics ecosystem</strong>
                combined with an interactive dashboard framework.
            </p>
            """, unsafe_allow_html=True)

            tools = [
                ("🐍 Python",      "Core language for data processing and analytics"),
                ("🔢 NumPy",       "Numerical operations and structured numeric data"),
                ("🐼 Pandas",      "Data cleaning, manipulation, and aggregation"),
                ("📉 Matplotlib",  "Charts and plots for visualizing statistics"),
                ("🎨 Seaborn",     "Enhanced statistical and aesthetic visualizations"),
                ("🚀 Streamlit",   "Interactive dashboard for dynamic data exploration"),
            ]
            for name, desc in tools:
                st.markdown(f"""
                <div style="background:#1c2330; border:1px solid #2a3444; border-radius:8px;
                            padding:10px 16px; margin-bottom:7px; display:flex;
                            font-family:'Rajdhani',sans-serif; font-size:14px; color:#e6edf3;
                            gap:10px; align-items:flex-start;">
                    <strong style="color:#c9a84c; min-width:110px;">{name}</strong>
                    <span style="color:#8b949e;">{desc}</span>
                </div>
                """, unsafe_allow_html=True)

        with st.expander("📊 Analytical Approach & Visualizations", expanded=False):
            about_block("🏏 Batting Analysis", [
                "Individual runs scored",
                "Total runs contribution",
                "Runs per match per player",
                "Strike rate comparison",
                "Role-wise contribution",
                "Batting consistency",
                "Total and average runs by batting order",
                "Phase-wise wickets lost",
            ])

            about_block("🎯 Bowling Analysis", [
                "Individual wickets taken",
                "Total wickets contribution",
                "Wickets per match per player",
                "Role-wise wicket contribution",
                "Average wickets by role",
                "Economy rate comparison",
                "Bowling consistency",
            ])

            about_block("👤 Player Analysis", [
                "Player information: role, matches played and usual batting order",
                "Batting KPIs: total runs, balls played, strike rate and batting consistency",
                "Runs and strike rate in each match",
                "Player's runs contribution in a chosen match and against the whole team",
                "Bowling KPIs: total wickets, overs bowled, economy rate and bowling consistency",
                "Wickets and economy rate in each match",
                "Player's wickets contribution in a chosen match and against the whole team",
            ])

            about_block("📋 Summary Analysis", [
                "Team runs and wickets in each match",
                "Top performer KPI cards: top run scorer, top wicket taker, best strike rate and best economy rate",
                "Automated team performance summary with the strongest roles, batting order and the phase where most wickets were lost",
            ])

        with st.expander("🔄 Recent Updates", expanded=False):

            def version_block(version, date, items):
                body = "".join(
                    f"<p style='font-family:Rajdhani,sans-serif; font-size:13px; color:#e6edf3; margin:3px 0;'>— {i}</p>"
                    for i in items
                )
                st.markdown(f"""
                <div style="background:#1c2330; border:1px solid #2a3444; border-radius:8px;
                            padding:12px 16px; margin-bottom:10px;">
                    <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                              font-size:16px; color:#c9a84c; margin:0 0 4px 0;">
                        Version {version} &nbsp;·&nbsp;
                        <span style="color:#8b949e; font-size:14px; font-weight:500;">{date}</span>
                    </p>
                    {body}
                </div>
                """, unsafe_allow_html=True)

            version_block("2.1", "16th September 2026", [
                "Improved data validation rules",
                "Added the Player Analytics section",
                "Split batting order runs into Total and Average sections, and added Average Wickets by Role",
            ])
            version_block("2.01", "18th April 2026", [
                "Improved overall tool user interface",
                "Improved data validation and cleaning",
                "Added drop-down expanders for Dataset Columns Overview and About Section",
                "Improved visualization clarity and chart styling",
                "Added KPI cards for key performance indicators in the Summary tab",
                "Improved logic for line charts and Runs/Wickets Contributions",
                "Organized insights into clear analytical sections",
                "Fixed Bugs and issues"
            ])
            version_block("2.0", "16th March 2026", [
                "Improved overall tool user interface",
                "Added support for .xlsx dataset uploads",
                "Enhanced data validation and cleaning",
                "Added more detailed batting and bowling analytics",
                "Improved visualization clarity",
                "Added interactive player performance analysis",
            ])
            version_block("1.0", "27th February 2026", ["Initial release"])

        bottom_space()

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
render_footer()
