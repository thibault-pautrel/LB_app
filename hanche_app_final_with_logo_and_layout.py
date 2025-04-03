
import streamlit as st

import streamlit as st
st.set_page_config(page_title="Évaluation de hanche", layout="wide")

from PIL import Image
import os

# Load and display the Lightback logo
logo_path = os.path.join(os.path.dirname(__file__), "lightback_logo.png")
logo = Image.open(logo_path)
st.image(logo, width=150)
st.markdown("## 🟡 Lightback – Évaluation de la hanche")
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages

st.set_page_config(page_title="Évaluation de hanche", layout="wide")
st.title("🦵 Évaluation fonctionnelle et analytique de la hanche")

# Patient name input
st.sidebar.header("🧍 Infos patient")
patient_name = st.sidebar.text_input("Nom du patient", value="Patient X")
evaluation_date = datetime.now().strftime("%d/%m/%Y")

# === ÉVALUATION ANALYTIQUE ===
st.header("✅ Évaluation analytique")
with st.form("analytique"):
    col1, col2 = st.columns(2)
    with col1:
        ri = st.checkbox("Rotation interne ≥ 30°", key="ri")
        re = st.checkbox("Rotation externe ≥ 45°", key="re")
        thomas = st.checkbox("Test de Thomas : genou en-dessous de l’horizontale", key="thomas")
    with col2:
        faber = st.checkbox("FABER sans douleur", key="faber")
        fadir = st.checkbox("FADIR sans douleur", key="fadir")
        chaine_post = st.checkbox("Chaîne postérieure plaquée au mur", key="chaine_post")
        adducteurs = st.checkbox("Adducteurs collés au mur (90°)", key="adducteurs")
    submit_analytique = st.form_submit_button("Valider analytique")

analytique_scores = {
    "Rotation int.": int(ri),
    "Rotation ext.": int(re),
    "Thomas": int(thomas),
    "FABER": int(faber),
    "FADIR": int(fadir),
    "Chaîne post.": int(chaine_post),
    "Adducteurs": int(adducteurs)
}

# === ÉVALUATION FONCTIONNELLE ===
st.header("💪 Évaluation fonctionnelle")
with st.form("fonctionnelle"):
    st.subheader("2.1. Squat Overhead")
    squat_inputs = [
        st.checkbox("Attitude penchée en avant", key="squat1"),
        st.checkbox("Genoux qui rentrent", key="squat2"),
        st.checkbox("Lombaires en cyphose", key="squat3"),
        st.checkbox("Squat incomplet (>90°)", key="squat4"),
        st.checkbox("Asymétrie D/G", key="squat5"),
        st.checkbox("Effondrement voute plantaire", key="squat6"),
        st.checkbox("Talons décollés", key="squat7"),
        st.checkbox("Coudes fléchis", key="squat8")
    ]

    st.subheader("2.2. Step Down")
    step_inputs = [
        st.checkbox("Inclinaison latérale du tronc", key="step1"),
        st.checkbox("Drop du bassin", key="step2"),
        st.checkbox("Valgus dynamique", key="step3"),
        st.checkbox("Absence de contrôle", key="step4"),
        st.checkbox("Perte d’équilibre", key="step5"),
        st.checkbox("Effondrement voute plantaire (Step Down)", key="step6"),
        st.checkbox("A-coups à la remontée", key="step7")
    ]
    submit_fonctionnelle = st.form_submit_button("Valider fonctionnelle")

squat_score = sum([not v for v in squat_inputs])
step_score = sum([not v for v in step_inputs])
fonctionnelle_scores = {
    "Attitude penchée en avant": 1 - int(squat_inputs[0]),
    "Genoux qui rentrent": 1 - int(squat_inputs[1]),
    "Lombaires en cyphose": 1 - int(squat_inputs[2]),
    "Squat incomplet (>90°)": 1 - int(squat_inputs[3]),
    "Asymétrie D/G": 1 - int(squat_inputs[4]),
    "Effondrement voute plantaire (Squat)": 1 - int(squat_inputs[5]),
    "Talons décollés": 1 - int(squat_inputs[6]),
    "Coudes fléchis": 1 - int(squat_inputs[7]),
    "Inclinaison latérale du tronc": 1 - int(step_inputs[0]),
    "Drop du bassin": 1 - int(step_inputs[1]),
    "Valgus dynamique": 1 - int(step_inputs[2]),
    "Absence de contrôle": 1 - int(step_inputs[3]),
    "Perte d’équilibre": 1 - int(step_inputs[4]),
    "Effondrement voute plantaire (Step)": 1 - int(step_inputs[5]),
    "A-coups à la remontée": 1 - int(step_inputs[6])
}

def draw_radar(scores, title):
    categories = list(scores.keys())
    values = list(scores.values()) + [list(scores.values())[0]]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color='blue', linewidth=2)
    ax.fill(angles, values, color='skyblue', alpha=0.4)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.set_yticklabels(['0', '0.5', '1.0'])
    ax.set_ylim(0, 1)
    ax.yaxis.grid(True, linestyle='dashed', color='gray')
    ax.xaxis.grid(True)
    ax.set_title(title, size=14, pad=20)
    circle = plt.Circle((0, 0), 1, transform=ax.transData._b, color='black', fill=False, linestyle='dotted')
    ax.add_artist(circle)
    return fig

col_r1, col_r2 = st.columns(2)
with col_r1:
    st.subheader("Radar analytique")
    st.pyplot(draw_radar(analytique_scores, "Analytique"))
with col_r2:
    st.subheader("Radar fonctionnel")
    st.pyplot(draw_radar(fonctionnelle_scores, "Fonctionnel"))

st.subheader("🎯 Score global")
total_score = sum(analytique_scores.values()) + squat_score + step_score
total_score_22 = round((total_score / 22) * 22, 1)
fig2, ax2 = plt.subplots(figsize=(8, 1.5))
cmap = plt.get_cmap('RdYlGn')
gradient = np.linspace(0, 1, 256).reshape(1, -1)
ax2.imshow(gradient, aspect='auto', cmap=cmap, extent=[0, 22, 0, 1])
ax2.axvline(total_score_22, color='black', linewidth=3)
ax2.text(total_score_22 + 0.3, 0.5, f"{total_score_22:.1f} pts", va='center', fontsize=10)
ax2.text(2, 1.1, "Rouge (0-12)", color='red', fontsize=9)
ax2.text(13, 1.1, "Orange (12-18)", color='darkorange', fontsize=9)
ax2.text(19, 1.1, "Vert (18-22)", color='green', fontsize=9)
ax2.set_xlim(0, 21)
ax2.axis('off')
st.pyplot(fig2)


def generate_pdf():
    buffer = BytesIO()
    with PdfPages(buffer) as pdf:
        fig = plt.figure(figsize=(8.27, 11.69))  # A4 page size
        gs = fig.add_gridspec(4, 2, height_ratios=[0.5, 2.5, 2.5, 1])

        # Header
        ax0 = fig.add_subplot(gs[0, :])
        ax0.axis("off")
        ax0.text(0.5, 0.6, "Évaluation fonctionnelle et analytique de la hanche", ha="center", fontsize=14)
        ax0.text(0.01, 0.3, f"Nom du patient : {patient_name}", fontsize=10)
        ax0.text(0.01, 0.1, f"Date : {evaluation_date}", fontsize=10)
        ax0.text(0.65, 0.1, f"Score global : {total_score_22} / 22", fontsize=10)

        # Radar analytique
        ax1 = fig.add_subplot(gs[1, 0], polar=True)
        categories1 = list(analytique_scores.keys())
        values1 = list(analytique_scores.values())
        values1 += values1[:1]
        angles1 = np.linspace(0, 2 * np.pi, len(categories1), endpoint=False).tolist()
        angles1 += angles1[:1]
        ax1.plot(angles1, values1, color='blue', linewidth=2)
        ax1.fill(angles1, values1, color='skyblue', alpha=0.4)
        ax1.set_xticks(angles1[:-1])
        ax1.set_xticklabels(categories1, fontsize=8)
        ax1.set_yticks([0.0, 0.5, 1.0])
        ax1.set_yticklabels(['0', '0.5', '1.0'])
        ax1.set_ylim(0, 1)
        ax1.set_title("Radar Analytique", size=10)
        ax1.add_artist(plt.Circle((0, 0), 1, transform=ax1.transData._b, color='black', fill=False, linestyle='dotted'))

        # Radar fonctionnel
        ax2 = fig.add_subplot(gs[1, 1], polar=True)
        categories2 = list(fonctionnelle_scores.keys())
        values2 = list(fonctionnelle_scores.values()) + [list(fonctionnelle_scores.values())[0]]
        angles2 = np.linspace(0, 2 * np.pi, len(categories2), endpoint=False).tolist()
        angles2 += angles2[:1]
        ax2.plot(angles2, values2, color='blue', linewidth=2)
        ax2.fill(angles2, values2, color='skyblue', alpha=0.4)
        ax2.set_xticks(angles2[:-1])
        ax2.set_xticklabels(categories2, fontsize=6)
        ax2.set_yticks([0.0, 0.5, 1.0])
        ax2.set_yticklabels(['0', '0.5', '1.0'])
        ax2.set_ylim(0, 1)
        ax2.set_title("Radar Fonctionnel", size=10)
        ax2.add_artist(plt.Circle((0, 0), 1, transform=ax2.transData._b, color='black', fill=False, linestyle='dotted'))

        # Score bar
        ax3 = fig.add_subplot(gs[3, :])
        cmap = plt.get_cmap('RdYlGn')
        gradient = np.linspace(0, 1, 256).reshape(1, -1)
        ax3.imshow(gradient, aspect='auto', cmap=cmap, extent=[0, 21, 0, 1])
        ax3.axvline(total_score_22, color='black', linewidth=3)
        ax3.text(total_score_22 + 0.3, 0.5, f"{total_score_22:.1f} pts", va='center', fontsize=10)
        ax3.text(2, 1.1, "Rouge (0-12)", color='red', fontsize=9)
        ax3.text(13, 1.1, "Orange (12-18)", color='darkorange', fontsize=9)
        ax3.text(19, 1.1, "Vert (18-21)", color='green', fontsize=9)
        ax3.set_xlim(0, 21)
        ax3.axis('off')

        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

    buffer.seek(0)
    return buffer


st.subheader("📄 Exporter l’évaluation en PDF")
if st.button("📤 Télécharger le rapport PDF"):
    pdf_bytes = generate_pdf()
    st.download_button(
        label="📥 Télécharger le rapport",
        data=pdf_bytes,
        file_name=f"Evaluation_Hanche_{patient_name.replace(' ', '_')}.pdf",
        mime='application/pdf'
    )
