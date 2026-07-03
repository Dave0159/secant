"""
Aplikasi Metode Secant (Secant Method) - Streamlit
Fitur:
1. User input persamaan f(x) = 0
2. Grafik fungsi ditampilkan agar user bisa memilih x0 dan x1
3. User input x0, x1, toleransi, dan maksimum iterasi
4. Program menjalankan metode secant, menampilkan tabel iterasi,
   jumlah iterasi, dan status konvergen / tidak konvergen
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations,
    implicit_multiplication_application, convert_xor
)

st.set_page_config(page_title="Metode Secant", page_icon="image.png", layout="wide")

# ---------------------------------------------------------
# STYLING
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        color-scheme: light dark;
        --background-color: #f7f9fc;
        --secondary-background-color: #ffffff;
        --text-color: #0f172a;
        --border-color: #eef0f5;
        --muted-color: #475569;
        --plot-gridcolor: #eef0f5;
        --plot-line-color: #4f46e5;
    }

    /* Override for dark mode */
    @media (prefers-color-scheme: dark) {
        :root {
            --background-color: #071029;
            --secondary-background-color: #0b1220;
            --text-color: #e6eef8;
            --border-color: rgba(255,255,255,0.06);
            --muted-color: #cbd5e1;
            --plot-gridcolor: rgba(255,255,255,0.06);
            --plot-line-color: #8b5cf6;
        }
        .section-card { box-shadow: 0 4px 16px rgba(2,6,23,0.6); }
        .hero { box-shadow: 0 10px 30px rgba(79, 70, 229, 0.18); }
        div[data-testid="stMetric"] { background: var(--secondary-background-color); border-color: var(--border-color); }
        div[data-testid="stDataFrame"] table { background: transparent; color: var(--text-color); }
    }

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        color: var(--text-color);
    }

    .main {
        background: linear-gradient(180deg, var(--background-color) 0%, #eef1f8 100%);
    }

    .hero {
        background: linear-gradient(120deg, #4f46e5 0%, #7c3aed 100%);
        padding: 2rem 2.2rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 1.6rem;
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.25);
    }
    .hero h1 { margin: 0; font-weight: 700; font-size: 2rem; }
    .hero p { margin: 0.4rem 0 0 0; opacity: 0.92; font-size: 1rem; }

    .section-card {
        background: var(--secondary-background-color);
        padding: 1.4rem 1.6rem;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(30, 41, 59, 0.06);
        margin-bottom: 1.3rem;
        border: 1px solid var(--border-color);
        color: var(--text-color);
    }
    .section-title {
        font-weight: 600;
        font-size: 1.1rem;
        color: var(--text-color);
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .func-badge {
        background: rgba(79, 70, 229, 0.12);
        color: var(--text-color);
        padding: 0.6rem 1rem;
        border-radius: 10px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 1rem;
        border-left: 4px solid #6366f1;
        margin-top: 0.4rem;
    }

    div[data-testid="stMetric"] {
        background: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 0.8rem 1rem;
        color: var(--text-color);
    }
    div[data-testid="stMetricValue"] { font-size: 1.5rem; font-weight: 700; color: var(--text-color); }
    div[data-testid="stMetricLabel"] { color: var(--muted-color); }

    .stButton>button {
        background: linear-gradient(120deg, #4f46e5, #7c3aed);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.6rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 6px 16px rgba(79, 70, 229, 0.3);
        transition: transform 0.15s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); }

    div[data-testid="stDataFrame"] { font-size: 1.05rem; }
    div[data-testid="stCaption"] { color: var(--muted-color); }

    .status-convergen {
        background: linear-gradient(120deg, #10b981, #059669);
        color: white; padding: 1rem 1.3rem; border-radius: 12px;
        font-weight: 600; font-size: 1.05rem;
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.25);
    }
    .status-divergen {
        background: linear-gradient(120deg, #ef4444, #dc2626);
        color: white; padding: 1rem 1.3rem; border-radius: 12px;
        font-weight: 600; font-size: 1.05rem;
        box-shadow: 0 6px 16px rgba(239, 68, 68, 0.25);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>Kalkulator Metode Secant</h1>
    <p>Masukkan persamaan, lihat grafiknya, lalu tentukan x₀ dan x₁ untuk mencari akar persamaan secara interaktif.</p>
</div>
""", unsafe_allow_html=True)

x = sp.Symbol('x')

# ---------------------------------------------------------
# 1. INPUT PERSAMAAN
# ---------------------------------------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">1. Masukkan Persamaan</div>', unsafe_allow_html=True)

eq_str = st.text_input(
    "Bentuk f(x) = 0, gunakan sintaks Python/sympy",
    value="x**3 - x - 2",
    placeholder="contoh: x^3 - 5x + 1, x**3 - x - 2, sin(x) - x/2, exp(x) - 3*x",
    label_visibility="collapsed"
)

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,  # biar "5x" -> 5*x, "2x^2" -> 2*x**2
    convert_xor,                          # biar "^" dibaca sebagai pangkat (**)
)

LOCAL_DICT = {
    "x": x,
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
    "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
    "exp": sp.exp, "log": sp.log, "ln": sp.log,
    "sqrt": sp.sqrt, "pi": sp.pi, "e": sp.E, "E": sp.E,
    "Abs": sp.Abs, "abs": sp.Abs,
}

def parse_function(expr_str):
    # Bersihkan penulisan umum yang sering dipakai orang tapi bukan sintaks Python murni
    cleaned = expr_str.strip()
    cleaned = cleaned.replace("÷", "/").replace("×", "*").replace("−", "-")
    # dukung pangkat dobel "**" tetap aman, "^" ditangani oleh convert_xor
    try:
        expr = parse_expr(cleaned, local_dict=LOCAL_DICT, transformations=TRANSFORMATIONS)
        f_lamb = sp.lambdify(x, expr, modules=["numpy"])
        return expr, f_lamb, None
    except Exception as e:
        return None, None, str(e)

expr, f, err = parse_function(eq_str)

if err:
    st.error(f"❌ Persamaan tidak valid: {err}")
    st.stop()

st.markdown(f'<div class="func-badge">f(x) = {sp.simplify(expr)}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

def compute_y_range(y_vals, extra_points=None, pad_frac=0.12):
    """
    Menentukan rentang sumbu-y yang enak dibaca.
    Fungsi curam seperti exp(x) bisa punya nilai yang meledak jauh di salah
    satu ujung range-x (mis. exp(10) ≈ 22000), sehingga auto-scale biasa
    membuat area di sekitar akar (yang nilainya kecil) jadi gepeng/tak
    terlihat. Di sini dipakai median + MAD (median absolute deviation) yang
    jauh lebih tahan terhadap nilai ekstrem dibanding min/max biasa.
    """
    finite = y_vals[np.isfinite(y_vals)]
    if finite.size == 0:
        return (-10.0, 10.0)

    actual_min, actual_max = float(np.min(finite)), float(np.max(finite))
    med = float(np.median(finite))
    mad = float(np.median(np.abs(finite - med))) * 1.4826  # skala setara std normal

    if mad < 1e-9:
        lo, hi = actual_min, actual_max
    else:
        lo = max(actual_min, med - 6 * mad)
        hi = min(actual_max, med + 6 * mad)

    if extra_points:
        ep = [float(v) for v in extra_points if np.isfinite(v)]
        if ep:
            lo = min(lo, min(ep))
            hi = max(hi, max(ep))

    if hi - lo < 1e-9:
        lo, hi = lo - 1, hi + 1

    pad = (hi - lo) * pad_frac
    return (lo - pad, hi + pad)

# ---------------------------------------------------------
# 2. GRAFIK + PARAMETER (berdampingan, grafik lebih kecil)
# ---------------------------------------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">2. Grafik & Parameter Iterasi</div>', unsafe_allow_html=True)

col_graph, col_params = st.columns([1.1, 1], gap="large")

with col_params:
    st.markdown("**Rentang sumbu (seperti kalkulator grafik)**")
    r1, r2 = st.columns(2)
    with r1:
        x_min = st.number_input("Batas bawah X", value=-10.0, step=1.0)
        y_min = st.number_input("Batas bawah Y", value=-10.0, step=1.0)
    with r2:
        x_max = st.number_input("Batas atas X", value=10.0, step=1.0)
        y_max = st.number_input("Batas atas Y", value=10.0, step=1.0)

    if x_min >= x_max:
        st.error("Batas bawah X harus lebih kecil dari batas atas X.")
        st.stop()
    if y_min >= y_max:
        st.error("Batas bawah Y harus lebih kecil dari batas atas Y.")
        st.stop()


    st.markdown("**Tebakan awal & parameter**")
    p1, p2 = st.columns(2)
    with p1:
        x0 = st.number_input("x₀", value=1.0, format="%.6f")
        tol = st.number_input("Toleransi error |x(i+1) - x(i)|", value=1e-6, format="%.10f")
    with p2:
        x1 = st.number_input("x₁", value=2.0, format="%.6f")
        max_iter = st.number_input("Maks. iterasi", value=50, min_value=1, step=1)

    f_tol = st.number_input(
        "Toleransi |f(x)| (memastikan hasil benar-benar dekat ke akar, bukan sekadar x berhenti bergerak)",
        value=1e-4, format="%.10f"
    )

    run = st.button(" ▷ Jalankan Metode Secant", type="primary", use_container_width=True)

x_vals = np.linspace(x_min, x_max, 1000)
try:
    with np.errstate(all="ignore"):
        y_vals = f(x_vals)
    y_vals = np.array(y_vals, dtype=float)
    y_vals[~np.isfinite(y_vals)] = np.nan  # titik overflow tidak digambar, bukan error
except Exception as e:
    st.error(f"❌ Gagal menghitung nilai fungsi: {e}")
    st.stop()

with col_graph:
    fig = go.Figure()
    fig.add_hline(y=0, line_color="#94a3b8", line_width=1)
    fig.add_vline(x=0, line_color="#94a3b8", line_width=1)
    fig.add_trace(go.Scatter(
        x=x_vals, y=y_vals,
        mode="lines",
        name="f(x)",
        line=dict(color="#4f46e5", width=2.5),
        hovertemplate="x = %{x:.4f}<br>f(x) = %{y:.4f}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="Grafik f(x) — sentuh/hover untuk lihat koordinat", font=dict(size=13, color="#1e1b4b")),
        xaxis_title="x",
        yaxis_title="f(x)",
        height=340,
        margin=dict(l=40, r=20, t=45, b=40),
        plot_bgcolor="white",
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        font=dict(family="Poppins, sans-serif", size=11),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#eef0f5", zeroline=False, range=[x_min, x_max])
    fig.update_yaxes(showgrid=True, gridcolor="#eef0f5", zeroline=False, range=[y_min, y_max])
    st.caption("💡 Sentuh/hover pada garis untuk lihat koordinat (x, f(x)). Gunakan grafik ini untuk memperkirakan x₀ dan x₁ yang dekat dengan akar.")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. PROSES METODE SECANT
# ---------------------------------------------------------
def secant_method(f, x0, x1, tol, max_iter, f_tol=1e-4):
    """
    Catatan penting soal exponential/fungsi curam:
    Jika hanya memakai |x(i+1) - x(i)| < tol sebagai syarat konvergen, fungsi
    yang naik sangat curam (mis. exp(x)) bisa membuat x "berhenti bergerak"
    (karena turunannya sangat besar) padahal f(x) masih jauh dari nol -> ini
    yang membuat program dulu SALAH melaporkan "konvergen" walau sebenarnya
    tidak ada akar di sekitar situ. Perbaikannya: syarat konvergen sekarang
    butuh KEDUANYA -> |x(i+1)-x(i)| < tol  DAN  |f(x(i+1))| < f_tol.
    Selain itu, jika hasil hitung meledak jadi inf/NaN (overflow khas fungsi
    eksponensial), iterasi langsung dihentikan dan dilaporkan tidak konvergen.
    """
    rows = []
    is_convergen = False
    root = None
    stop_reason = None

    x_prev, x_curr = float(x0), float(x1)
    with np.errstate(all="ignore"):
        f_prev = float(f(x_prev))
        f_curr = float(f(x_curr))

    if not (np.isfinite(f_prev) and np.isfinite(f_curr)):
        return [], False, None, (
            "f(x₀) atau f(x₁) tidak terdefinisi/tak hingga (overflow). "
            "Coba x₀/x₁ yang lain, lebih dekat ke sumbu-x pada grafik."
        )

    for i in range(1, int(max_iter) + 1):
        denom = (f_curr - f_prev)
        if denom == 0:
            rows.append({
                "Iterasi": i, "x(i-1)": x_prev, "x(i)": x_curr,
                "f(x(i-1))": f_prev, "f(x(i))": f_curr,
                "x(i+1)": None, "Error": None,
                "Keterangan": "Berhenti: pembagi nol"
            })
            stop_reason = "Pembagi nol: f(x(i)) - f(x(i-1)) = 0 sehingga iterasi tidak bisa dilanjutkan."
            break

        with np.errstate(all="ignore"):
            x_next = x_curr - f_curr * (x_curr - x_prev) / denom
            f_next = float(f(x_next)) if np.isfinite(x_next) else float("nan")

        # Deteksi overflow/NaN (khas fungsi eksponensial yang meledak)
        if not (np.isfinite(x_next) and np.isfinite(f_next)):
            rows.append({
                "Iterasi": i, "x(i-1)": x_prev, "x(i)": x_curr,
                "f(x(i-1))": f_prev, "f(x(i))": f_curr,
                "x(i+1)": None, "Error": None,
                "Keterangan": "Berhenti: nilai meledak ke tak hingga (overflow)"
            })
            stop_reason = (
                "Nilai x atau f(x) meledak ke tak hingga (overflow) — fungsi kemungkinan "
                "tidak memiliki akar real di arah pencarian ini."
            )
            break

        error = abs(x_next - x_curr)

        rows.append({
            "Iterasi": i,
            "x(i-1)": x_prev,
            "x(i)": x_curr,
            "f(x(i-1))": f_prev,
            "f(x(i))": f_curr,
            "x(i+1)": x_next,
            "Error": error,
            "Keterangan": "OK"
        })

        # Konvergen HANYA jika x sudah stabil DAN f(x) benar-benar dekat nol.
        # Ini mencegah "konvergen palsu" saat x berhenti bergerak akibat
        # turunan fungsi yang sangat curam (mis. exp(x)) padahal f(x) masih besar.
        if error < tol and abs(f_next) < f_tol:
            is_convergen = True
            root = x_next
            break

        x_prev, f_prev = x_curr, f_curr
        x_curr, f_curr = x_next, f_next

    if root is None and not is_convergen and rows:
        last = rows[-1]
        if last["x(i+1)"] is not None:
            root = last["x(i+1)"]
            if stop_reason is None:
                stop_reason = (
                    f"Toleransi belum tercapai hingga {max_iter} iterasi "
                    f"(|f(x)| terakhir ≈ {abs(f_curr):.6g}, belum di bawah {f_tol})."
                )

    return rows, is_convergen, root, stop_reason

if run:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">3. Hasil Iterasi</div>', unsafe_allow_html=True)

    try:
        rows, is_convergen, root, stop_reason = secant_method(f, x0, x1, tol, int(max_iter), f_tol)
    except Exception as e:
        st.error(f"❌ Terjadi error saat menjalankan iterasi: {e}")
        st.stop()

    if not rows and root is None and stop_reason:
        st.error(f"❌ Tidak dapat memulai iterasi: {stop_reason}")
        st.stop()

    jumlah_iterasi = len(rows)

    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.metric("Jumlah Iterasi", jumlah_iterasi)
    with col_res2:
        st.metric("Akar Ditemukan (x)", f"{root:.6f}" if root is not None else "-")
    with col_res3:
        st.metric("Status", "✅ KONVERGEN" if is_convergen else "❌ TIDAK KONVERGEN")

    if is_convergen:
        st.markdown(
            f'<div class="status-convergen">✅ Metode secant KONVERGEN setelah {jumlah_iterasi} iterasi. '
            f'Akar persamaan ≈ {root:.6f}, dengan f(akar) ≈ {f(root):.6e}</div>',
            unsafe_allow_html=True
        )
    else:
        alasan = f" Sebab: {stop_reason}" if stop_reason else ""
        st.markdown(
            f'<div class="status-divergen">❌ Metode secant TIDAK KONVERGEN dalam {jumlah_iterasi} iterasi '
            f'(maksimum {max_iter}).{alasan} Coba ubah x₀/x₁ berdasarkan grafik, '
            f'atau perbesar jumlah maksimum iterasi.</div>',
            unsafe_allow_html=True
        )

    st.write("")
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, height=min(38 * (len(df) + 1) + 3, 520))

    st.write("")
    st.markdown("**Visualisasi titik-titik iterasi**")

    iter_x = [x0, x1] + [r["x(i+1)"] for r in rows if r["x(i+1)"] is not None]
    iter_y = [float(f(v)) for v in iter_x]
    iter_labels = ["x₀", "x₁"] + [f"x{i+2}" for i in range(len(iter_x) - 2)]

    fig2 = go.Figure()
    fig2.add_hline(y=0, line_color="#94a3b8", line_width=1)
    fig2.add_vline(x=0, line_color="#94a3b8", line_width=1)
    fig2.add_trace(go.Scatter(
        x=x_vals, y=y_vals,
        mode="lines", name="f(x)",
        line=dict(color="#4f46e5", width=2.5),
        hovertemplate="x = %{x:.4f}<br>f(x) = %{y:.4f}<extra></extra>",
    ))
    fig2.add_trace(go.Scatter(
        x=iter_x, y=iter_y,
        mode="lines+markers", name="Titik iterasi",
        line=dict(color="#f59e0b", width=1.8, dash="dash"),
        marker=dict(size=9, color="#f59e0b", line=dict(width=1, color="white")),
        text=iter_labels,
        hovertemplate="%{text}<br>x = %{x:.6f}<br>f(x) = %{y:.6f}<extra></extra>",
    ))
    if root is not None:
        fig2.add_trace(go.Scatter(
            x=[root], y=[float(f(root))],
            mode="markers", name=f"Akar ≈ {root:.4f}",
            marker=dict(size=16, color="#ef4444", symbol="star", line=dict(width=1, color="white")),
            hovertemplate=f"Akar<br>x = {root:.6f}<br>f(x) = {float(f(root)):.6e}<extra></extra>",
        ))
    fig2.update_layout(
        title=dict(text="Konvergensi Metode Secant Menuju Akar — sentuh titik untuk lihat koordinat",
                    font=dict(size=13, color="#1e1b4b")),
        xaxis_title="x",
        yaxis_title="f(x)",
        height=460,
        margin=dict(l=40, r=20, t=45, b=40),
        plot_bgcolor="white",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Poppins, sans-serif", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig2.update_xaxes(showgrid=True, gridcolor="#eef0f5", zeroline=False, range=[x_min, x_max])
    if auto_zoom:
        y_lo2, y_hi2 = compute_y_range(y_vals, extra_points=iter_y)
        fig2.update_yaxes(showgrid=True, gridcolor="#eef0f5", zeroline=False, range=[y_lo2, y_hi2])
    else:
        fig2.update_yaxes(showgrid=True, gridcolor="#eef0f5", zeroline=False, range=[y_min, y_max])
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": True})

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
with st.expander("ℹ️ Tentang Metode Secant"):
    st.markdown(r"""
    Metode secant mencari akar persamaan $f(x) = 0$ menggunakan rumus:

    $$x_{i+1} = x_i - f(x_i) \cdot \frac{x_i - x_{i-1}}{f(x_i) - f(x_{i-1})}$$

    - Dibutuhkan dua tebakan awal, $x_0$ dan $x_1$ (tidak harus mengapit akar).
    - Iterasi dianggap **konvergen** jika $|x_{i+1} - x_i| < \text{toleransi}$ sebelum mencapai maksimum iterasi.
    - Jika toleransi tidak tercapai hingga maksimum iterasi, atau pembagi menjadi nol, iterasi dianggap **tidak konvergen**.
    """)
st.markdown('</div>', unsafe_allow_html=True)
