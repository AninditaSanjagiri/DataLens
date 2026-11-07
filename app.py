"""
DataLens — CSV Dataset Intelligence
Generative AI CA Mini Project P10
Run: streamlit run app.py
"""

import ast
import builtins
import contextlib
import io
import os
import re
import textwrap
import warnings
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

st.set_page_config(
    page_title="DataLens | Dataset Intelligence",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------
# Design system
# ---------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
  --ink: #17211f;
  --muted: #687571;
  --line: #e6ebe8;
  --paper: #f7f9f7;
  --card: #ffffff;
  --green: #176b57;
  --green-soft: #e9f4ef;
  --lime: #d8edbd;
  --orange: #d58a48;
}
html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif;
}
.stApp {
  background: #f7f9f7;
  color: var(--ink);
}
h1, h2, h3, h4 {
  font-family: 'Manrope', sans-serif !important;
  letter-spacing: -0.035em;
  color: #17211f;
}
.block-container {
  max-width: 1440px;
  padding-top: 2.0rem;
  padding-bottom: 3rem;
}
[data-testid="stSidebar"] {
  background: #f0f4f0;
  border-right: 1px solid #e1e8e2;
}
[data-testid="stSidebar"] > div:first-child {
  padding-top: 1.6rem;
}
/* Keep sidebar labels readable even when the user's Streamlit theme is dark. */
[data-testid="stSidebar"],
[data-testid="stSidebar"] * {
  color: #243a32;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] small {
  color: #40564d !important;
}
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] [data-baseweb="select"] > div {
  background: #ffffff !important;
  color: #243a32 !important;
  border-color: #cbd8d0 !important;
}
[data-testid="stSidebar"] input::placeholder {
  color: #78877f !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label,
[data-testid="stSidebar"] [role="radiogroup"] label * {
  color: #243a32 !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] section {
  background: #ffffff;
  border: 1px dashed #b8c9bf;
  border-radius: 14px;
}
.stButton > button, .stDownloadButton > button {
  border-radius: 10px;
  border: 1px solid #cbd8d0;
  background: #ffffff;
  color: #1d4036;
  font-weight: 600;
  transition: all .18s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
  border-color: #176b57;
  color: #105541;
  background: #edf6f0;
  transform: translateY(-1px);
  box-shadow: 0 5px 16px rgba(23,107,87,.10);
}
.stButton > button[kind="primary"] {
  background: #176b57;
  color: white;
  border-color: #176b57;
}
.stButton > button[kind="primary"]:hover {
  background: #105541;
  color: white;
}
[data-testid="stTabs"] [role="tab"] {
  border-radius: 9px 9px 0 0;
  font-weight: 600;
  padding: .65rem 1rem;
  color: #52645b !important;
  opacity: 1 !important;
}
[data-testid="stTabs"] [role="tab"] p,
[data-testid="stTabs"] [role="tab"] span {
  color: #52645b !important;
  opacity: 1 !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"],
[data-testid="stTabs"] [role="tab"][aria-selected="true"] p,
[data-testid="stTabs"] [role="tab"][aria-selected="true"] span {
  color: #176b57 !important;
}
[data-testid="stMetric"] {
  background: white;
  border: 1px solid #e5ebe6;
  padding: 17px 18px;
  border-radius: 15px;
  box-shadow: 0 3px 14px rgba(25,55,40,.035);
  transition: transform .18s ease, box-shadow .18s ease;
}
[data-testid="stMetric"]:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 22px rgba(25,55,40,.08);
}
[data-testid="stMetricLabel"] p {
  color: #718078 !important;
  font-size: .82rem !important;
  font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
  color: #173d32;
  font-family: 'Manrope', sans-serif;
}
[data-testid="stExpander"] {
  border: 1px solid #e2e9e3;
  border-radius: 12px;
  background: #fff;
}
[data-testid="stDataFrame"], [data-testid="stTable"] {
  border: 1px solid #e4eae5;
  border-radius: 12px;
  overflow: hidden;
}
div[data-baseweb="input"] > div, div[data-baseweb="select"] > div,
.stTextArea textarea {
  border-radius: 10px !important;
}
.hero {
  background: linear-gradient(120deg, #eaf3ed 0%, #f5f8f3 58%, #f5efe4 100%);
  border: 1px solid #e0e9e1;
  border-radius: 22px;
  padding: 28px 32px;
  margin-bottom: 22px;
}
.brand-kicker {
  color: #176b57;
  text-transform: uppercase;
  letter-spacing: .16em;
  font-size: .72rem;
  font-weight: 800;
}
.hero-title {
  font-family: 'Manrope', sans-serif;
  font-size: clamp(2.2rem, 4vw, 3.15rem);
  line-height: 1.08;
  font-weight: 800;
  letter-spacing: -.06em;
  margin: 7px 0 9px 0;
  color: #172b25;
}
.hero-copy {
  color: #5c6d65;
  font-size: 1.02rem;
  max-width: 760px;
  line-height: 1.65;
}
.section-eyebrow {
  color: #176b57;
  font-size: .72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .13em;
  margin-bottom: 5px;
}
.panel {
  background: #fff;
  border: 1px solid #e4eae5;
  border-radius: 16px;
  padding: 18px 20px;
  transition: all .18s ease;
}
.panel:hover {
  border-color: #c4d7ca;
  box-shadow: 0 8px 22px rgba(28,70,48,.055);
}
.small-muted { color: #718078; font-size: .86rem; }
.pill {
  display: inline-block;
  background: #e9f4ef;
  color: #176b57;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: .76rem;
  font-weight: 700;
}
hr { border-color: #e4eae5 !important; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------
# API and data helpers
# ---------------------------------------------------------------------
def get_api_key() -> str:
    entered = st.session_state.get("api_key_input", "").strip()
    if entered:
        return entered
    try:
        secret = st.secrets.get("GEMINI_API_KEY", "")
        if secret:
            return str(secret).strip()
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY", "").strip()


def get_model_name() -> str:
    return st.session_state.get("model_name", "gemini-2.5-flash").strip()


def ask_llm(prompt: str, image_png: Optional[bytes] = None) -> str:
    key = get_api_key()
    if not key:
        return "[No Gemini API key. Add it in the sidebar or configure GEMINI_API_KEY.]"
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=key)
        contents = [prompt]
        if image_png:
            contents = [types.Part.from_bytes(data=image_png, mime_type="image/png"), prompt]
        response = client.models.generate_content(model=get_model_name(), contents=contents)
        return response.text or "[Gemini returned an empty response.]"
    except Exception as exc:
        return f"[Gemini error: {type(exc).__name__}: {exc}]"


def llm_failed(value: str) -> bool:
    return value.startswith("[")


@st.cache_data(show_spinner=False)
def load_csv(file_bytes: bytes) -> pd.DataFrame:
    return pd.read_csv(
        io.BytesIO(file_bytes),
        comment="#",
        low_memory=False,
        na_values=["?", " ?"],
        skipinitialspace=True,
    )


DATASET_LIBRARY = {
    "Kepler · Objects of Interest": {
        "description": "Kepler candidate table with disposition labels and transit measurements.",
        "source": "NASA Exoplanet Archive · cumulative",
        "target": "koi_disposition",
        "query": "select kepid,koi_name,koi_disposition,koi_period,koi_duration,koi_depth,koi_prad,koi_teq,koi_steff,koi_srad,koi_model_snr from cumulative",
        "local": ["kepler.csv", "NASA Exoplanet.csv"],
    },
    "TESS · Objects of Interest": {
        "description": "TESS candidates with follow-up dispositions and stellar/planet measurements.",
        "source": "NASA Exoplanet Archive · toi",
        "target": "tfopwg_disp",
        "query": "select toi,tid,tfopwg_disp,pl_orbper,pl_trandurh,pl_trandep,pl_rade,st_tmag,st_teff,st_logg,st_rad,st_mass,rastr,decstr from toi",
        "local": ["tess.csv", "TOI_2025.09.19_11.44.36.csv"],
    },
    "Confirmed Exoplanets": {
        "description": "Confirmed planets with orbital, planetary and host-star properties.",
        "source": "NASA Exoplanet Archive · pscomppars",
        "target": None,
        "query": "select pl_name,hostname,discoverymethod,disc_year,pl_orbper,pl_orbsmax,pl_orbeccen,pl_eqt,pl_rade,pl_bmasse,pl_dens,st_teff,st_mass,st_rad,st_age,sy_dist,sy_pnum from pscomppars where default_flag=1",
        "local": ["confirmed_planets_working.csv", "confirmed_planets.csv"],
    },
}


@st.cache_data(show_spinner=False, ttl=86400)
def fetch_nasa_table(query: str) -> pd.DataFrame:
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?" + urlencode({"query": query, "format": "csv"})
    request = Request(url, headers={"User-Agent": "DataLens-CA-Project/1.0"})
    with urlopen(request, timeout=60) as response:
        payload = response.read()
    return pd.read_csv(io.BytesIO(payload), comment="#", low_memory=False)


@st.cache_data(show_spinner=False)
def load_iris_sample() -> pd.DataFrame:
    from sklearn.datasets import load_iris
    bunch = load_iris(as_frame=True)
    frame = bunch.data.copy()
    frame["species"] = bunch.target.map(dict(enumerate(bunch.target_names)))
    return frame


def load_library_dataset(dataset_name: str):
    if dataset_name == "Iris":
        return load_iris_sample(), "scikit-learn built-in Iris dataset"
    meta = DATASET_LIBRARY[dataset_name]
    from pathlib import Path
    for filename in meta["local"]:
        local_path = Path("datasets") / filename
        if local_path.exists():
            return load_csv(local_path.read_bytes()), f"Local file: {local_path.as_posix()}"
    return fetch_nasa_table(meta["query"]), meta["source"]


def clean_frame(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).strip() for c in out.columns]
    out = out.loc[:, ~out.columns.duplicated()]
    return out


def tokens(name: str):
    name = re.sub(r"([a-z])([A-Z])", r"\1 \2", str(name)).lower()
    return [t for t in re.split(r"[^a-z0-9]+", name) if t]


def pretty(name: str) -> str:
    return " ".join(tokens(name))


def is_num(series: pd.Series) -> bool:
    return pd.api.types.is_numeric_dtype(series) and not pd.api.types.is_bool_dtype(series)


def schema_text(df: pd.DataFrame) -> str:
    sample = df.iloc[:4, :30].to_string()
    return f"Shape: {df.shape}\nDtypes:\n{df.dtypes.to_string()}\nSample:\n{sample}"


# ---------------------------------------------------------------------
# Profiling, target inference and recommendations
# ---------------------------------------------------------------------
TARGET_HINTS = ["disposition", "disp", "target", "label", "class", "status", "churn", "income", "outcome"]


def guess_target(df: pd.DataFrame):
    for hint in TARGET_HINTS:
        for col in df.columns:
            if hint in col.lower() and 1 < df[col].nunique(dropna=True) <= 30:
                return col
    return None


def is_classification(series: pd.Series) -> bool:
    s = series.dropna()
    if s.empty:
        return False
    return (not is_num(s)) or s.nunique() <= 15


def recommend_task(df: pd.DataFrame, target):
    if target is None:
        return (
            "Clustering / exploratory analysis",
            "No target is selected. Explore natural groups, anomalies and relationships. "
            "Choose a meaningful outcome column if you want a supervised task.",
        )
    series = df[target].dropna()
    n = series.nunique()
    if n < 2:
        return "Target needs review", f"'{target}' has fewer than two distinct non-missing values."
    if is_classification(series):
        kind = "Binary classification" if n == 2 else "Multi-class classification"
        return kind, f"'{target}' contains {n} distinct classes. Check class balance and leakage before modelling."
    return "Regression", f"'{target}' is numeric with {n:,} distinct values."


def column_summary(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "Data type": df.dtypes.astype(str),
        "Missing (%)": (df.isna().mean() * 100).round(2),
        "Unique values": df.nunique(dropna=True),
        "Non-null": df.notna().sum(),
    }).sort_values("Missing (%)", ascending=False)


def draw_columns(df: pd.DataFrame, cols, ncols=3, per_row_height=3.0):
    cols = list(cols)
    if not cols:
        return None
    nrows = int(np.ceil(len(cols) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(14, per_row_height * nrows))
    axes = np.array(axes, dtype=object).reshape(-1)
    for ax, col in zip(axes, cols):
        series = df[col].dropna()
        if series.empty:
            ax.text(.5, .5, "No non-missing values", ha="center", va="center")
            ax.set_title(col, fontsize=9)
        elif series.nunique() <= 1:
            ax.bar(["constant"], [len(series)], color="#d58a48")
            ax.set_title(f"{col} · constant", fontsize=9)
        elif is_num(series):
            values = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
            if len(values):
                ax.hist(values, bins=min(30, max(8, int(np.sqrt(len(values)))),), color="#4f8a73", alpha=.88)
            ax.set_title(col, fontsize=9)
        else:
            series.astype(str).value_counts().head(12).plot.bar(ax=ax, color="#4f8a73")
            ax.tick_params(axis="x", labelrotation=35)
            ax.set_title(col, fontsize=9)
        ax.tick_params(labelsize=7)
        ax.grid(axis="y", alpha=.15)
    for ax in axes[len(cols):]:
        ax.axis("off")
    fig.tight_layout()
    return fig


def fig_to_png(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    return buf.getvalue()


def lifecycle_fallback(task: str, target) -> str:
    target_line = f"Target: `{target}`." if target else "No target selected; begin with exploratory analysis."
    return f"""
1. **Validate the data:** inspect missing values, duplicates, constant columns and invalid ranges.
2. **Define the prediction goal:** {target_line} Confirm the target is available at prediction time.
3. **Prepare features:** remove identifiers and leakage columns; impute missing values and encode categoricals.
4. **Create a holdout split:** use stratification for classification and a suitable split strategy for regression.
5. **Train baselines:** compare a simple baseline with tree-based models.
6. **Evaluate appropriately:** use macro-F1 / balanced accuracy for imbalanced classification, or MAE / RMSE / R² for regression.
7. **Review errors and fairness:** inspect subgroup performance, uncertainty and data limitations.
8. **Document and deploy:** save preprocessing with the model and monitor data drift.
"""


# ---------------------------------------------------------------------
# U2: generated pandas code with conservative AST checks
# ---------------------------------------------------------------------
SAFE_BUILTIN_NAMES = {
    "len", "range", "min", "max", "sum", "sorted", "round", "abs", "list", "dict",
    "set", "tuple", "str", "int", "float", "bool", "enumerate", "zip", "print",
    "any", "all", "isinstance", "map", "filter", "reversed", "pow", "divmod",
    "frozenset", "slice", "repr", "format", "ValueError", "KeyError", "TypeError",
}
SAFE_BUILTINS = {name: getattr(builtins, name) for name in SAFE_BUILTIN_NAMES}


def extract_code(text: str) -> str:
    match = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.S | re.I)
    return (match.group(1) if match else text).strip()


def validate_generated_code(code: str):
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return f"Syntax error: {exc}"
    forbidden_nodes = (ast.Import, ast.ImportFrom, ast.With, ast.AsyncWith, ast.Lambda,
                       ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef, ast.Global,
                       ast.Nonlocal, ast.Delete, ast.Await, ast.Yield, ast.Raise)
    for node in ast.walk(tree):
        if isinstance(node, forbidden_nodes):
            return f"Disallowed syntax: {type(node).__name__}"
        if isinstance(node, ast.Name) and node.id.startswith("__"):
            return "Disallowed private/dunder name."
        if isinstance(node, ast.Attribute) and node.attr.startswith("_"):
            return "Disallowed private/dunder attribute."
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id not in SAFE_BUILTIN_NAMES and node.func.id not in {"exec"}:
                return f"Disallowed function call: {node.func.id}"
    return None


def run_generated_code(code: str, df: pd.DataFrame):
    error = validate_generated_code(code)
    if error:
        return None, error
    env = {"__builtins__": SAFE_BUILTINS, "pd": pd, "np": np, "df": df.copy(), "result": None}
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec(compile(code, "<generated-pandas>", "exec"), env, env)
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"
    shown = env.get("result")
    if shown is None:
        shown = output.getvalue() or "Code ran successfully but did not assign `result` or print output."
    if isinstance(shown, (pd.DataFrame, pd.Series)):
        shown = shown.copy()
    return shown, None


def answer_question(df: pd.DataFrame, question: str):
    prompt = (
        "You are writing a small pandas analysis snippet for a DataFrame named df. "
        "Only use df, pd and np. Do not import modules, access files, use network, "
        "or call system functions. Assign the final answer to a variable named result. "
        "Return only one Python code block.\n\n"
        f"{schema_text(df)}\n\nUser question: {question}"
    )
    reply = ask_llm(prompt)
    if llm_failed(reply):
        return "", None, reply
    code = extract_code(reply)
    result, error = run_generated_code(code, df)
    if error:
        retry = ask_llm(prompt + f"\n\nYour previous code failed with: {error}\nFix the code. Return only Python.")
        if not llm_failed(retry):
            code = extract_code(retry)
            result, error = run_generated_code(code, df)
    if error:
        return code, None, f"Execution failed after one retry: {error}"
    explanation = ask_llm(
        f"Question: {question}\nCode:\n{code}\nOutput:\n{str(result)[:3500]}\n"
        "Explain the result in 2-4 concise sentences. Mention any caveats."
    )
    return code, result, explanation


# ---------------------------------------------------------------------
# U3: semantic grouping and chart interpretation
# ---------------------------------------------------------------------
@st.cache_resource(show_spinner="Loading the sentence-transformer model…")
def get_embedder():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


@st.cache_data(show_spinner=False)
def embed_texts(texts: tuple) -> np.ndarray:
    return get_embedder().encode(list(texts), normalize_embeddings=True, show_progress_bar=False)


def column_texts(df: pd.DataFrame, cols):
    descriptions = []
    for col in cols:
        sample = ", ".join(df[col].dropna().astype(str).unique()[:4])
        descriptions.append(f"column {pretty(col)}; dtype {df[col].dtype}; example values {sample}")
    return tuple(descriptions)


def semantic_groups(df: pd.DataFrame, cols, n_groups: int):
    from sklearn.cluster import AgglomerativeClustering
    embeddings = embed_texts(column_texts(df, cols))
    try:
        model = AgglomerativeClustering(n_clusters=n_groups, metric="cosine", linkage="average")
    except TypeError:
        model = AgglomerativeClustering(n_clusters=n_groups, affinity="cosine", linkage="average")
    labels = model.fit_predict(embeddings)
    groups = {}
    for col, label in zip(cols, labels):
        groups.setdefault(int(label), []).append(col)
    return groups


# ---------------------------------------------------------------------
# U5: identifiers, sensitive columns and imbalance
# ---------------------------------------------------------------------
SENSITIVE_TOKENS = {
    "gender", "sex", "race", "ethnicity", "ethnic", "religion", "age", "marital",
    "nationality", "country", "disability", "disease", "health", "diagnosis",
    "income", "salary", "wage", "zip", "zipcode", "postal", "address", "email",
    "phone", "ssn", "birth", "dob",
}
SENSITIVE_REFERENCES = [
    "gender or sex of a person", "race or ethnicity", "religion", "age of a person",
    "marital status", "nationality or native country", "health condition or disease",
    "income or salary", "home address or zip code", "email address or phone number",
    "national identity number or SSN", "date of birth",
]
ID_EXACT = {"id", "uid", "index", "kepid", "tid", "toi", "hostname", "rowid", "oid", "objectid"}
ID_EXCEPTIONS = {"toi_created", "ra", "dec", "rastr", "decstr", "ra_deg", "dec_deg"}


def keyword_sensitive(columns):
    hits = {}
    for col in columns:
        found = sorted(set(tokens(col)) & SENSITIVE_TOKENS)
        if "age" in found and (set(tokens(col)) & {"st", "stellar", "planet", "pl"}):
            found.remove("age")
        if found:
            hits[col] = found
    return hits


def find_identifiers(df: pd.DataFrame):
    found = []
    for col in df.columns:
        low = col.lower()
        parts = set(tokens(col))
        if low in ID_EXCEPTIONS:
            continue
        by_name = bool(parts & ID_EXACT)
        series = df[col].dropna()
        # Only use uniqueness as a secondary clue for text/integer-like fields.
        by_unique = (
            len(series) > 50
            and series.nunique() / max(1, len(series)) > .98
            and (not is_num(series) or pd.api.types.is_integer_dtype(series))
            and not (parts & {"ra", "dec", "time", "date", "period", "radius", "mass"})
        )
        if by_name or by_unique:
            found.append(col)
    return found


def embedding_sensitive(columns, threshold=0.62):
    reference = embed_texts(tuple(SENSITIVE_REFERENCES))
    embeddings = embed_texts(tuple(pretty(col) for col in columns))
    similarities = embeddings @ reference.T
    results = []
    for i, col in enumerate(columns):
        best = int(similarities[i].argmax())
        score = float(similarities[i, best])
        if score >= threshold:
            results.append((col, SENSITIVE_REFERENCES[best], round(score, 3)))
    return results


def imbalance_info(df: pd.DataFrame, target):
    if target is None or target not in df.columns or not is_classification(df[target].dropna()):
        return None
    counts = df[target].dropna().astype(str).value_counts()
    if len(counts) < 2:
        return None
    shares = counts / counts.sum()
    ratio = float(counts.iloc[0] / max(1, counts.iloc[-1]))
    smallest = float(shares.iloc[-1])
    if smallest < .10 or ratio >= 10:
        severity = "Severe"
    elif smallest < .25 or ratio >= 3:
        severity = "Moderate"
    else:
        severity = "Balanced"
    return {"counts": counts, "shares": shares, "ratio": ratio, "severity": severity}


def audit_dataset(df: pd.DataFrame, target):
    empty = [col for col in df.columns if df[col].isna().all()]
    work = df.drop(columns=empty) if empty else df
    missing = work.isna().mean() * 100
    high_missing = [col for col in work.columns if missing[col] > 50]
    duplicates = int(work.duplicated().sum())
    constants = [col for col in work.columns if work[col].nunique(dropna=True) <= 1]
    ids = find_identifiers(work)
    sensitive = keyword_sensitive(work.columns)
    imbalance = imbalance_info(work, target)
    penalties = []
    avg_missing = float(missing.mean()) if len(missing) else 0
    if avg_missing > 2:
        penalties.append((f"Average missingness is {avg_missing:.1f}%", min(20, round(avg_missing / 2))))
    if empty:
        penalties.append((f"{len(empty)} completely empty columns", 5))
    if high_missing:
        penalties.append((f"{len(high_missing)} columns have over 50% missing", min(10, len(high_missing))))
    if duplicates:
        penalties.append((f"{duplicates} duplicate rows", 5))
    if constants:
        penalties.append((f"{len(constants)} constant columns", min(5, len(constants))))
    if ids:
        penalties.append((f"{len(ids)} identifier-like columns", min(6, 2 * len(ids))))
    if sensitive:
        penalties.append((f"{len(sensitive)} potentially sensitive columns", min(15, 5 * len(sensitive))))
    if imbalance and imbalance["severity"] != "Balanced":
        penalties.append((f"{imbalance['severity']} class imbalance", 15 if imbalance["severity"] == "Severe" else 8))
    if len(work) < 500:
        penalties.append(("Fewer than 500 rows", 10))
    elif len(work) < 1000:
        penalties.append(("Fewer than 1,000 rows", 5))
    return {
        "empty": empty, "avg_missing": avg_missing, "high_missing": high_missing,
        "duplicates": duplicates, "constants": constants, "ids": ids,
        "sensitive": sensitive, "imbalance": imbalance, "penalties": penalties,
        "score": max(0, 100 - sum(p for _, p in penalties)),
    }


# ---------------------------------------------------------------------
# U4: CTGAN and utility evaluation
# ---------------------------------------------------------------------
def pick_ctgan_columns(df, target, exclude, max_num=15, max_cat=4):
    usable = lambda col: (
        col not in exclude and col != target
        and df[col].notna().mean() > .90
        and df[col].nunique(dropna=True) > 1
    )
    numeric = [c for c in df.columns if is_num(df[c]) and usable(c)]
    numeric = sorted(numeric, key=lambda c: (df[c].isna().mean(), df[c].nunique()))[:max_num]
    categorical = [
        c for c in df.columns
        if not is_num(df[c]) and usable(c) and df[c].nunique(dropna=True) <= 20
    ][:max_cat]
    selected = numeric + categorical
    if target and target not in selected:
        selected.append(target)
    return selected


def prepare_ctgan_frame(df, cols):
    sub = df[cols].copy()
    for col in cols:
        if is_num(sub[col]):
            sub[col] = pd.to_numeric(sub[col], errors="coerce")
            median = sub[col].median()
            sub[col] = sub[col].fillna(median if pd.notna(median) else 0)
            sub[col] = sub[col].replace([np.inf, -np.inf], np.nan).fillna(median if pd.notna(median) else 0)
        else:
            mode = sub[col].mode(dropna=True)
            fill = mode.iloc[0] if len(mode) else "Unknown"
            sub[col] = sub[col].fillna(fill).astype(str)
    return sub


def encode_feature_sets(train, test, synth, target):
    features = [c for c in train.columns if c != target]
    combined = pd.concat(
        [train[features], test[features], synth[features]],
        keys=["real_train", "real_test", "synthetic"],
    )
    combined = pd.get_dummies(combined, dummy_na=True).astype(float)
    return combined.loc["real_train"], combined.loc["real_test"], combined.loc["synthetic"]


def evaluate_tstr(train, test, synthetic, target, classification):
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, r2_score
    x_train, x_test, x_synth = encode_feature_sets(train, test, synthetic, target)
    if classification:
        model_type = RandomForestClassifier
        # Align target labels as strings for consistent categorical handling.
        y_train = train[target].astype(str)
        y_synth = synthetic[target].astype(str)
        y_test = test[target].astype(str)
        # A synthetic sample missing a real class cannot learn that class.
        if set(y_synth.unique()) != set(y_train.unique()):
            warnings.warn("Synthetic sample does not contain every real training class.")
        models = [
            ("Train on REAL, test on real", x_train, y_train),
            ("Train on SYNTHETIC, test on real", x_synth, y_synth),
        ]
        metrics = {}
        for name, x, y in models:
            model = model_type(n_estimators=120, random_state=42, n_jobs=-1, class_weight="balanced")
            model.fit(x, y)
            pred = model.predict(x_test)
            metrics[name] = {
                "accuracy": round(float(accuracy_score(y_test, pred)), 3),
                "macro_f1": round(float(f1_score(y_test, pred, average="macro", zero_division=0)), 3),
            }
        return metrics
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_squared_error
    y_train = pd.to_numeric(train[target], errors="coerce")
    y_synth = pd.to_numeric(synthetic[target], errors="coerce")
    y_test = pd.to_numeric(test[target], errors="coerce")
    metrics = {}
    for name, x, y in [
        ("Train on REAL, test on real", x_train, y_train),
        ("Train on SYNTHETIC, test on real", x_synth, y_synth),
    ]:
        model = RandomForestRegressor(n_estimators=120, random_state=42, n_jobs=-1)
        model.fit(x, y)
        pred = model.predict(x_test)
        metrics[name] = {
            "MAE": round(float(mean_absolute_error(y_test, pred)), 3),
            "RMSE": round(float(np.sqrt(mean_squared_error(y_test, pred))), 3),
            "R2": round(float(r2_score(y_test, pred)), 3),
        }
    return metrics


def run_ctgan(df, target, exclude, max_rows, epochs):
    from ctgan import CTGAN
    from sklearn.model_selection import train_test_split

    cols = pick_ctgan_columns(df, target, exclude)
    if len(cols) < 2:
        raise ValueError("Not enough usable columns. Select a dataset with at least two usable fields.")
    sub = prepare_ctgan_frame(df, cols)
    sub = sub.sample(min(len(sub), max_rows), random_state=42).reset_index(drop=True)
    if len(sub) < 100:
        raise ValueError("CTGAN requires at least 100 usable rows for this demo.")
    classification = target is not None and is_classification(df[target].dropna())
    if target and classification:
        sub[target] = sub[target].astype(str)
    discrete = [c for c in cols if not is_num(sub[c])]
    stratify = None
    if target and classification:
        counts = sub[target].value_counts()
        if len(counts) > 1 and counts.min() >= 2:
            stratify = sub[target]
    train, test = train_test_split(
        sub, test_size=.25, random_state=42, stratify=stratify
    )
    train = train.reset_index(drop=True)
    test = test.reset_index(drop=True)
    # CTGAN requires batch size divisible by pac (10 by default) and an even batch size.
    batch_size = max(10, min(500, (len(train) // 10) * 10))
    model = CTGAN(epochs=int(epochs), batch_size=batch_size, verbose=False)
    model.fit(train, discrete)
    synthetic = model.sample(len(train))
    result = {
        "columns": cols, "train": train, "test": test, "synthetic": synthetic,
        "classification": classification, "target": target, "metrics": None,
    }
    if target:
        result["metrics"] = evaluate_tstr(train, test, synthetic, target, classification)
    return result


def compare_data_quality(real, synthetic, numeric_cols):
    rows = []
    for col in numeric_cols:
        r = pd.to_numeric(real[col], errors="coerce").dropna()
        s = pd.to_numeric(synthetic[col], errors="coerce").dropna()
        if len(r) and len(s):
            rows.append({
                "Column": col,
                "Real mean": r.mean(),
                "Synthetic mean": s.mean(),
                "Real std": r.std(),
                "Synthetic std": s.std(),
                "Mean difference (%)": abs(r.mean() - s.mean()) / (abs(r.mean()) + 1e-9) * 100,
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------
# Header and sidebar
# ---------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="padding:4px 2px 16px 2px">
      <div style="font-family:Manrope;font-size:1.55rem;font-weight:800;color:#173d32;letter-spacing:-.06em">◈ DataLens</div>
      <div style="font-size:.78rem;color:#718078;margin-top:2px">CSV intelligence workspace</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("#### Start exploring")
    source_mode = st.radio("Choose a data source", ["Dataset library", "Upload your own CSV"], key="source_mode")
    uploaded = None
    selected_library_dataset = None
    if source_mode == "Dataset library":
        selected_library_dataset = st.selectbox(
            "Choose a sample dataset",
            ["Kepler · Objects of Interest", "TESS · Objects of Interest", "Confirmed Exoplanets", "Iris"],
            key="library_dataset",
        )
        if selected_library_dataset == "Iris":
            st.caption("150 rows · 4 numeric features · 3 species · classification")
        else:
            meta = DATASET_LIBRARY[selected_library_dataset]
            st.caption(meta["description"])
            st.caption(f"Source: {meta['source']}")
    else:
        uploaded = st.file_uploader("Upload a CSV file", type=["csv"])
    st.markdown("---")
    st.markdown("#### AI configuration")
    st.text_input("Gemini API key", type="password", key="api_key_input", placeholder="Paste your API key")
    st.text_input("Gemini model", value="gemini-2.5-flash", key="model_name")
    if get_api_key():
        st.caption("● Gemini key detected")
    else:
        st.caption("○ Add a key to enable AI-powered features")
    st.markdown("---")
    st.markdown(
        "<div class='small-muted'>NASA samples are retrieved from the official Exoplanet Archive and cached. Uploaded files are processed in this app session. Avoid confidential data on public deployments.</div>",
        unsafe_allow_html=True,
    )


st.markdown("""
<div class="hero">
  <div class="brand-kicker">Dataset intelligence · Generative AI</div>
  <div class="hero-title">DataLens<span style="color:#d58a48">.</span></div>
  <div class="hero-copy">A clearer view of your data. Profile a CSV, discover its machine-learning potential, ask questions in plain English, explore semantic column groups and assess synthetic-data quality before modelling.</div>
</div>
""", unsafe_allow_html=True)

if source_mode == "Upload your own CSV" and uploaded is None:
    left, right = st.columns([1.25, .75], gap="large")
    with left:
        st.markdown("### Start with a dataset")
        st.write("Upload a CSV to generate a profile, identify modelling opportunities and uncover data-quality risks.")
        st.info("Switch to Dataset library in the sidebar to try Kepler, TESS, confirmed exoplanets or Iris.")
    with right:
        st.markdown("### What DataLens can do")
        for title, desc in [
            ("Profile & task", "Understand columns, missingness and suitable ML tasks."),
            ("Ask your data", "Generate and execute pandas analysis from natural-language questions."),
            ("Semantic groups", "Cluster related columns with sentence embeddings and interpret charts with Gemini."),
            ("Synthetic data", "Train CTGAN and compare synthetic rows with real observations."),
            ("Risk check", "Find identifiers, potentially sensitive fields and class imbalance."),
        ]:
            st.markdown(f"<div class='panel' style='margin-bottom:9px'><b>{title}</b><div class='small-muted'>{desc}</div></div>", unsafe_allow_html=True)
    st.stop()

try:
    if source_mode == "Dataset library":
        with st.spinner(f"Loading {selected_library_dataset}…"):
            raw_df, dataset_source = load_library_dataset(selected_library_dataset)
        dataset_label = selected_library_dataset
    else:
        raw_df = load_csv(uploaded.getvalue())
        dataset_source = f"Uploaded file: {uploaded.name}"
        dataset_label = uploaded.name
    df = clean_frame(raw_df)
except Exception as exc:
    st.error(f"Could not load the selected dataset: {type(exc).__name__}: {exc}")
    if source_mode == "Dataset library" and selected_library_dataset != "Iris":
        st.info("If NASA is unavailable, put a downloaded CSV in the project's datasets folder using a supported filename.")
    st.stop()

if df.empty or len(df.columns) == 0:
    st.error("The uploaded file has no readable rows or columns.")
    st.stop()

file_key = f"{dataset_label}:{df.shape}:{len(df.columns)}"
empty_cols = [c for c in df.columns if df[c].isna().all()]
work = df.drop(columns=empty_cols) if empty_cols else df.copy()

guess = guess_target(work)
if source_mode == "Dataset library":
    preferred_target = "species" if selected_library_dataset == "Iris" else DATASET_LIBRARY[selected_library_dataset]["target"]
    if preferred_target in work.columns:
        guess = preferred_target
target_options = ["(none)"] + list(work.columns)
with st.sidebar:
    target_default = target_options.index(guess) if guess in target_options else 0
    target_choice = st.selectbox(
        "Target column",
        target_options,
        index=target_default,
        key=f"target_{file_key}",
        help="Choose the outcome column for supervised-learning recommendations and imbalance checks.",
    )
target = None if target_choice == "(none)" else target_choice

task, task_reason = recommend_task(work, target)
report = audit_dataset(df, target)
file_size_mb = uploaded.size / (1024 * 1024) if uploaded is not None else df.memory_usage(deep=True).sum() / (1024 * 1024)

# ---------------------------------------------------------------------
# KPI strip
# ---------------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4, gap="medium")
k1.metric("Readiness score", f"{report['score']}/100", help="Heuristic score based on missingness, duplicates, constant columns, identifiers, sensitivity flags and class imbalance.")
k2.metric("Rows", f"{len(df):,}")
k3.metric("Columns", f"{len(df.columns):,}")
k4.metric("Recommended task", task, help=task_reason)

st.markdown(
    f"<div style='display:flex;gap:9px;align-items:center;flex-wrap:wrap;margin:10px 0 22px 0'>"
    f"<span class='pill'>{dataset_label}</span>"
    f"<span class='small-muted'>{file_size_mb:.2f} MB · {df.shape[0]:,} records · {df.shape[1]:,} fields · {dataset_source}</span>"
    f"</div>",
    unsafe_allow_html=True,
)

with st.expander("How was the readiness score calculated?"):
    st.write("This is a transparent heuristic, not a certified data-quality or privacy score.")
    if report["penalties"]:
        for reason, points in report["penalties"]:
            st.write(f"• {reason}: −{points} points")
    else:
        st.success("No configured deductions were triggered.")
    if report["empty"]:
        st.caption("Completely empty columns are excluded from the working profile.")

# ---------------------------------------------------------------------
# Main workspace navigation (no U1-U5 labels)
# ---------------------------------------------------------------------
tab_profile, tab_ask, tab_groups, tab_synth, tab_risk = st.tabs([
    "Profile & task", "Ask your data", "Column groups", "Synthetic data", "Risk check"
])

# ---------------------------------------------------------------------
# Profile & task
# ---------------------------------------------------------------------
with tab_profile:
    st.markdown("<div class='section-eyebrow'>Explore your dataset</div>", unsafe_allow_html=True)
    st.subheader("Profile & task")
    st.write(task_reason)
    if empty_cols:
        st.warning(f"{len(empty_cols)} completely empty columns are excluded from the profile: {', '.join(empty_cols[:12])}")
    summary = column_summary(work)
    st.markdown("#### Column overview")
    st.dataframe(summary, use_container_width=True, height=300)
    col_a, col_b = st.columns([1.1, .9])
    with col_a:
        st.markdown("#### Distribution explorer")
        # Keep identifiers in the source data, but do not treat them as useful
        # distributions. High-cardinality text columns are also poor bar charts.
        identifier_cols = set(report.get("ids", []))
        constant_cols = set(report.get("constants", []))
        numeric_features = [
            c for c in work.columns
            if c not in identifier_cols
            and c not in constant_cols
            and c != target
            and is_num(work[c].dropna())
            and work[c].nunique(dropna=True) > 1
        ]
        categorical_features = [
            c for c in work.columns
            if c not in identifier_cols
            and c not in constant_cols
            and c != target
            and not is_num(work[c].dropna())
            and 1 < work[c].nunique(dropna=True) <= 20
        ]
        plot_candidates = ([target] if target and target in work.columns and work[target].nunique(dropna=True) > 1 else []) + numeric_features + categorical_features
        defaults = ([target] if target and target in plot_candidates else []) + numeric_features[:5]
        chosen = st.multiselect(
            "Choose columns to visualise (up to 12)",
            plot_candidates,
            default=defaults[:6],
            max_selections=12,
            key=f"profile_plot_{file_key}_{target}",
            help="Identifiers, constant columns and high-cardinality text fields are excluded from this explorer, but remain in your dataset.",
        )
        if identifier_cols:
            st.caption("Excluded identifier-like columns: " + ", ".join(sorted(identifier_cols)[:10]))
        if constant_cols:
            st.caption("Excluded constant columns: " + ", ".join(sorted(constant_cols)[:10]))
        related_targets = [
            c for c in work.columns
            if c != target and any(token in c.lower() for token in ("disposition", "_disp", "target", "label"))
        ]
        if target and related_targets:
            st.warning(
                "Other outcome-like columns are retained but not auto-plotted: "
                + ", ".join(related_targets[:8])
                + ". Check whether they encode the same decision or information unavailable at prediction time before modelling."
            )
        fig = draw_columns(work, chosen)
        if fig:
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        else:
            st.caption("Choose a target, numerical measurement or low-cardinality category to see its distribution.")
    with col_b:
        st.markdown("#### Suggested ML lifecycle")
        st.write("A practical starting sequence based on the selected task.")
        if st.button("Generate dataset-specific steps", type="primary", key=f"lifecycle_{file_key}_{target}"):
            prompt = (
                f"Dataset schema:\n{schema_text(work)}\nTask: {task}\nTarget: {target}\n"
                "Give 7 concise, concrete ML lifecycle steps tailored to this dataset. "
                "Mention possible leakage, data preparation, split strategy and suitable metrics."
            )
            response = ask_llm(prompt)
            st.session_state[f"lifecycle_{file_key}_{target}"] = lifecycle_fallback(task, target) if llm_failed(response) else response
            if llm_failed(response):
                st.warning(response)
        lifecycle = st.session_state.get(f"lifecycle_{file_key}_{target}")
        if lifecycle:
            st.markdown(lifecycle)
        else:
            st.markdown(lifecycle_fallback(task, target))


# ---------------------------------------------------------------------
# Ask your data
# ---------------------------------------------------------------------
with tab_ask:
    st.markdown("<div class='section-eyebrow'>Natural language analysis</div>", unsafe_allow_html=True)
    st.subheader("Ask your data")
    st.write("Ask a question. Gemini drafts pandas code, DataLens executes it against the uploaded DataFrame, then Gemini explains the result.")
    st.warning("Generated code runs in-process with restricted syntax checks. This is a classroom-demo guardrail, not a hardened security sandbox. Do not expose it to untrusted public users.")
    question = st.text_input(
        "What would you like to know?",
        placeholder="Which 10 columns have the highest percentage of missing values?",
        key=f"question_{file_key}",
    )
    if st.button("Analyse dataset", type="primary", disabled=not bool(question.strip()), key=f"ask_{file_key}"):
        with st.spinner("Gemini is writing and running pandas code…"):
            code, result, explanation = answer_question(work, question.strip())
        st.session_state[f"ask_result_{file_key}"] = (code, result, explanation)
    answer = st.session_state.get(f"ask_result_{file_key}")
    if answer:
        code, result, explanation = answer
        st.markdown("#### Generated pandas code")
        st.code(code or "# No code returned", language="python")
        if result is not None:
            st.markdown("#### Execution result")
            if isinstance(result, pd.DataFrame):
                st.dataframe(result, use_container_width=True)
            elif isinstance(result, pd.Series):
                st.dataframe(result.to_frame(), use_container_width=True)
            else:
                st.write(result)
        st.markdown("#### Explanation")
        st.write(explanation)


# ---------------------------------------------------------------------
# Column groups
# ---------------------------------------------------------------------
with tab_groups:
    st.markdown("<div class='section-eyebrow'>Semantic structure</div>", unsafe_allow_html=True)
    st.subheader("Column groups")
    st.write("Sentence Transformers embeds each column's name, type and sample values. Similar columns are grouped; Gemini can interpret a chart from a selected group.")
    cols_for_embedding = list(work.columns)[:150]
    if len(work.columns) > 150:
        st.info("This dataset has more than 150 columns. The first 150 are used to keep embedding time manageable.")
    if len(cols_for_embedding) < 3:
        st.info("At least three columns are required for semantic grouping.")
    else:
        max_groups = min(15, len(cols_for_embedding) - 1)
        group_count = st.slider("Number of groups", 2, max_groups, min(8, max_groups), key=f"group_count_{file_key}")
        if st.button("Discover column groups", type="primary", key=f"make_groups_{file_key}"):
            try:
                with st.spinner("Embedding columns and discovering semantic groups…"):
                    groups = semantic_groups(work, cols_for_embedding, group_count)
                st.session_state[f"groups_{file_key}"] = groups
                st.success(f"Created {len(groups)} semantic groups.")
            except Exception as exc:
                st.error(f"Column grouping failed: {type(exc).__name__}: {exc}")
        groups = st.session_state.get(f"groups_{file_key}")
        if groups:
            ordered_groups = sorted(groups.items(), key=lambda item: (-len(item[1]), item[0]))
            for group_id, group_cols in ordered_groups:
                with st.expander(f"Group {group_id + 1} · {len(group_cols)} columns"):
                    st.write(", ".join(group_cols))
            group_ids = [g for g, _ in ordered_groups]
            selected_group = st.selectbox(
                "Choose a group to visualise",
                group_ids,
                format_func=lambda gid: f"Group {gid + 1} · {len(groups[gid])} columns",
                key=f"group_select_{file_key}",
            )
            group_cols = groups[selected_group]
            varying_cols = [c for c in group_cols if work[c].nunique(dropna=True) > 1]
            constant_cols = [c for c in group_cols if c not in varying_cols]
            if constant_cols:
                st.info(f"Constant columns are excluded from the chart: {', '.join(constant_cols)}")
            visual_cols = varying_cols[:6]
            if visual_cols:
                group_fig = draw_columns(work, visual_cols)
                st.pyplot(group_fig, use_container_width=True)
                png = fig_to_png(group_fig)
                plt.close(group_fig)
                if st.button("Interpret this chart with Gemini Vision", type="primary", key=f"vision_{file_key}_{selected_group}"):
                    with st.spinner("Gemini is interpreting the chart…"):
                        interpretation = ask_llm(
                            f"Interpret these charts for columns {visual_cols} in a dataset. "
                            "Describe the observed distributions, unusual patterns, missingness caveats "
                            "and plausible domain meaning. Do not claim causation or infer units that are not shown.",
                            png,
                        )
                    st.session_state[f"vision_result_{file_key}_{selected_group}"] = interpretation
                vision_result = st.session_state.get(f"vision_result_{file_key}_{selected_group}")
                if vision_result:
                    st.markdown("#### Vision interpretation")
                    st.write(vision_result)
            else:
                st.info("This group contains only constant or empty columns. Choose another group to interpret.")


# ---------------------------------------------------------------------
# Synthetic data
# ---------------------------------------------------------------------
with tab_synth:
    st.markdown("<div class='section-eyebrow'>Generative modelling</div>", unsafe_allow_html=True)
    st.subheader("Synthetic data")
    st.write("Train a CTGAN model on selected columns, generate synthetic rows and compare distributions, correlations and downstream predictive utility.")
    st.warning("Synthetic data is not automatically anonymous or safe to share. Treat generated rows as experimental until privacy and fidelity are evaluated.")
    controls_a, controls_b = st.columns(2)
    max_rows = controls_a.slider("Maximum training rows", 500, 5000, 2000, step=500, key=f"ctgan_rows_{file_key}")
    epochs = controls_b.slider("CTGAN epochs", 10, 200, 50, step=10, key=f"ctgan_epochs_{file_key}")
    st.caption("Start with 500 rows and 10 epochs to check compatibility. Increase gradually after a successful run.")
    if st.button("Train CTGAN and compare", type="primary", key=f"train_ctgan_{file_key}_{target}"):
        try:
            with st.spinner("Training CTGAN and generating synthetic rows. This can take several minutes…"):
                result = run_ctgan(work, target, set(report["ids"]), max_rows, epochs)
            st.session_state[f"ctgan_result_{file_key}_{target}"] = result
            st.success(f"Generated {len(result['synthetic']):,} synthetic rows.")
        except Exception as exc:
            st.error(f"CTGAN pipeline failed: {type(exc).__name__}: {exc}")
    synth_result = st.session_state.get(f"ctgan_result_{file_key}_{target}")
    if synth_result:
        real = synth_result["train"]
        synthetic = synth_result["synthetic"]
        st.markdown("#### Columns used")
        st.write(", ".join(synth_result["columns"]))
        st.markdown("#### Real vs synthetic sample")
        real_col, synthetic_col = st.columns(2)
        real_col.caption("Real training rows")
        real_col.dataframe(real.head(8), use_container_width=True)
        synthetic_col.caption("Generated synthetic rows")
        synthetic_col.dataframe(synthetic.head(8), use_container_width=True)
        numeric_cols = [c for c in synth_result["columns"] if is_num(real[c])]
        st.markdown("#### Distribution comparison")
        if numeric_cols:
            selected_numeric = numeric_cols[:6]
            fig, axes = plt.subplots(2, 3, figsize=(14, 7))
            axes = axes.ravel()
            for ax, col in zip(axes, selected_numeric):
                r = pd.to_numeric(real[col], errors="coerce").dropna()
                s = pd.to_numeric(synthetic[col], errors="coerce").dropna()
                if len(r) and len(s):
                    lo = min(r.quantile(.01), s.quantile(.01))
                    hi = max(r.quantile(.99), s.quantile(.99))
                    if lo == hi:
                        lo, hi = float(r.min()), float(r.max()) + 1
                    bins = np.linspace(lo, hi, 26)
                    ax.hist(r.clip(lo, hi), bins=bins, density=True, alpha=.55, label="Real", color="#4f8a73")
                    ax.hist(s.clip(lo, hi), bins=bins, density=True, alpha=.5, label="Synthetic", color="#d58a48")
                    ax.set_title(col, fontsize=9)
                    ax.legend(fontsize=7)
                else:
                    ax.set_title(f"{col} · no values")
            for ax in axes[len(selected_numeric):]:
                ax.axis("off")
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        if len(numeric_cols) >= 2:
            common = [c for c in numeric_cols if real[c].nunique(dropna=True) > 1 and synthetic[c].nunique(dropna=True) > 1]
            if len(common) >= 2:
                real_corr = real[common].corr()
                synth_corr = synthetic[common].corr()
                difference = (real_corr - synth_corr).abs()
                mean_difference = float(np.nanmean(difference.values))
                st.markdown(f"#### Correlation difference · mean absolute difference: **{mean_difference:.3f}**")
                fig, ax = plt.subplots(figsize=(9, 6))
                image = ax.imshow(difference.values, cmap="YlGn", vmin=0, vmax=1)
                ax.set_xticks(range(len(common)))
                ax.set_yticks(range(len(common)))
                ax.set_xticklabels(common, rotation=90, fontsize=7)
                ax.set_yticklabels(common, fontsize=7)
                fig.colorbar(image, ax=ax)
                fig.tight_layout()
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)
        if synth_result["metrics"]:
            st.markdown("#### Train on synthetic, test on real")
            metrics_df = pd.DataFrame(synth_result["metrics"]).T
            st.dataframe(metrics_df, use_container_width=True)
            st.caption("Both models are evaluated on the same held-out real test set. A large gap suggests synthetic data may not preserve predictive relationships.")
        else:
            st.info("No target was selected, so downstream TSTR evaluation was skipped. Distribution and correlation comparisons are still available.")
        if synth_result["classification"] and target:
            class_share = pd.DataFrame({
                "Real": real[target].astype(str).value_counts(normalize=True),
                "Synthetic": synthetic[target].astype(str).value_counts(normalize=True),
            }).fillna(0)
            st.markdown("#### Target class proportions")
            st.bar_chart(class_share)
        quality = compare_data_quality(real, synthetic, numeric_cols)
        if not quality.empty:
            with st.expander("Numeric summary comparison"):
                st.dataframe(quality.round(3), use_container_width=True)
        st.download_button(
            "Download synthetic CSV",
            synthetic.to_csv(index=False).encode("utf-8"),
            file_name="datalens_synthetic_rows.csv",
            mime="text/csv",
        )


# ---------------------------------------------------------------------
# Risk check
# ---------------------------------------------------------------------
with tab_risk:
    st.markdown("<div class='section-eyebrow'>Before you model</div>", unsafe_allow_html=True)
    st.subheader("Risk check")
    risk_a, risk_b = st.columns(2)
    with risk_a:
        st.markdown("#### Identifiers")
        if report["ids"]:
            st.warning("Review these fields before modelling: " + ", ".join(report["ids"]))
        else:
            st.success("No identifier-like columns detected by the current heuristics.")
        st.markdown("#### Potentially sensitive fields")
        if report["sensitive"]:
            for col, labels in report["sensitive"].items():
                st.warning(f"{col}: {', '.join(labels)}")
        else:
            st.success("No sensitive columns detected by keyword rules.")
        if st.button("Run semantic sensitivity check", key=f"sensitive_semantic_{file_key}"):
            try:
                with st.spinner("Comparing column names with sensitive concepts…"):
                    hits = embedding_sensitive(list(work.columns), .62)
                st.session_state[f"sensitive_hits_{file_key}"] = hits
            except Exception as exc:
                st.error(f"Semantic sensitivity check failed: {type(exc).__name__}: {exc}")
        semantic_hits = st.session_state.get(f"sensitive_hits_{file_key}")
        if semantic_hits is not None:
            extra_hits = [h for h in semantic_hits if h[0] not in report["sensitive"]]
            if extra_hits:
                st.dataframe(pd.DataFrame(extra_hits, columns=["Column", "Closest concept", "Similarity"]), use_container_width=True)
            else:
                st.caption("No additional semantic matches above the selected threshold.")
    with risk_b:
        st.markdown("#### Class imbalance")
        imbalance = report["imbalance"]
        if imbalance is None:
            st.info("Select a classification target in the sidebar to inspect class balance.")
        else:
            st.metric("Imbalance severity", imbalance["severity"], f"Largest / smallest: {imbalance['ratio']:.1f}×")
            st.bar_chart(imbalance["counts"])
            if imbalance["severity"] == "Balanced":
                st.success("No strong class imbalance detected by the current threshold.")
            else:
                st.warning("Consider stratified splitting, class weights or resampling on the training split only. Evaluate with macro-F1, balanced accuracy or PR-AUC.")
            tiny = imbalance["counts"][imbalance["counts"] < 10]
            if len(tiny):
                st.error("Very small classes (<10 rows): " + ", ".join(tiny.index.astype(str)))
    st.markdown("#### Other data-quality checks")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Duplicate rows", f"{report['duplicates']:,}")
    m2.metric("Constant columns", f"{len([c for c in work.columns if work[c].nunique(dropna=True) <= 1]):,}")
    m3.metric("Columns >50% missing", f"{len(report['high_missing']):,}")
    m4.metric("Average missingness", f"{report['avg_missing']:.1f}%")
    if report["high_missing"]:
        st.write("High-missingness columns: " + ", ".join(report["high_missing"]))


# ---------------------------------------------------------------------
# Downloadable report
# ---------------------------------------------------------------------
report_lines = [
    f"# DataLens dataset report: {dataset_label}",
    "",
    f"- Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns",
    f"- Source: {dataset_source}",
    f"- Approximate dataset size: {file_size_mb:.2f} MB",
    f"- Selected target: {target or 'None'}",
    f"- Recommended task: {task}",
    f"- Task rationale: {task_reason}",
    f"- Readiness score: {report['score']}/100",
    "",
    "## Readiness score breakdown",
]
report_lines += [f"- {reason}: -{points}" for reason, points in report["penalties"]] or ["- No deductions triggered."]
report_lines += [
    "",
    "## Data quality",
    f"- Average missingness: {report['avg_missing']:.2f}%",
    f"- Duplicate rows: {report['duplicates']}",
    f"- Identifier-like columns: {', '.join(report['ids']) or 'None detected'}",
    f"- Potentially sensitive columns (keyword rules): {', '.join(report['sensitive']) or 'None detected'}",
    f"- Columns with >50% missing: {', '.join(report['high_missing']) or 'None'}",
]
if report["imbalance"]:
    report_lines.append(
        f"- Class imbalance: {report['imbalance']['severity']} "
        f"(largest/smallest class ratio {report['imbalance']['ratio']:.2f}×)"
    )
st.sidebar.markdown("---")
st.sidebar.download_button(
    "Download dataset report (.md)",
    "\n".join(report_lines).encode("utf-8"),
    file_name="datalens_report.md",
    mime="text/markdown",
    use_container_width=True,
)
st.sidebar.caption("DataLens · P10 · Dataset intelligence")
