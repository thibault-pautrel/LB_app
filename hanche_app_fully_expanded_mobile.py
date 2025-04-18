
import streamlit as st
from datetime import datetime
import json

st.set_page_config(page_title="Évaluation de hanche", layout="wide")

decision_tree = {'question': 'Localisation de la douleur ?', 'options': {'Douleur antérieure de hanche': {'question': 'Test de Thomas positif ?', 'yes': {'diagnosis': 'Douleur psoas'}, 'no': {'question': 'FABER positif ?', 'yes': {'diagnosis': 'Pubalgie'}, 'no': {'question': 'Raideur de hanche ?', 'yes': {'question': 'Amplitude limitée ?', 'yes': {'question': 'Perte rotation interne ?', 'yes': {'diagnosis': 'Arthrose coxo-fémorale'}, 'no': {'diagnosis': 'Raideur de hanche'}}, 'no': {'diagnosis': 'Raideur de hanche'}}, 'no': {'diagnosis': 'Conflit fémoro-acétabulaire'}}}}, 'Douleur postérieure de hanche': {'question': 'FADIR positif ?', 'yes': {'diagnosis': 'Syndrôme fessier profond'}, 'no': {'question': 'Douleur profonde ne dépassant pas la fesse ?', 'yes': {'question': 'Pas de signes neuros ?', 'yes': {'diagnosis': 'Lombalgie'}, 'no': {'diagnosis': 'Syndrome fessier profond'}}, 'no': {'question': 'Lasègue positif ?', 'yes': {'question': 'Signes neuros sur territoire L5-S1 ?', 'yes': {'diagnosis': 'Sciatique vraie'}, 'no': {'diagnosis': 'Syndrôme fessier profond'}}, 'no': {'question': 'Extension debout positif ?', 'yes': {'diagnosis': 'Douleur facettaire'}, 'no': {'question': 'Raideur matinale ?', 'yes': {'diagnosis': 'Lombalgie inflammatoire'}, 'no': {'question': 'Douleur en flexion lombaire ?', 'yes': {'diagnosis': 'Lésion ligamentaire/discale'}, 'no': {'diagnosis': 'Lombalgie'}}}}}}}, 'Douleur latérale de hanche': {'question': 'Douleur à la pression/palpation latérale ?', 'yes': {'question': 'Douleur si résistance à l’ABD isométrique en décubitus latéral ?', 'yes': {'question': 'Douleur unipodale >30’’ + faiblesse musculaire ?', 'yes': {'diagnosis': 'Tendinopathie du moyen fessier'}, 'no': {'diagnosis': 'Bursite trochantérienne'}}, 'no': {'question': 'Test d’Obert positif ?', 'yes': {'diagnosis': 'Syndrome bandelette ilio-tibiale proximale'}, 'no': {'diagnosis': 'Douleur latérale non spécifique'}}}, 'no': {'diagnosis': 'Contracture fessière latérale'}}, 'Douleur sacro-iliaque': {'question': 'Test de Gaenslen positif ?', 'yes': {'question': 'Squeeze test positif ?', 'yes': {'diagnosis': 'Atteinte sacro-iliaque'}, 'no': {'diagnosis': 'Atteinte sacro-iliaque'}}, 'no': {'question': 'Compression test ?', 'yes': {'diagnosis': 'Atteinte sacro-iliaque'}, 'no': {'diagnosis': 'Douleur sacro-iliaque non spécifique'}}}}}

# === Decision tree logic ===
def traverse_tree(tree, path):
    node = tree
    for step in path:
        if "options" in node:
            node = node["options"][step]
        elif step in node:
            node = node[step]
    return node

def run_decision_tree():
    st.header("🌳 Arbre Décisionnel Interactif")

    if "tree_path" not in st.session_state:
        st.session_state.tree_path = []

    if "diagnosis" not in st.session_state:
        st.session_state.diagnosis = None

    def reset():
        st.session_state.tree_path = []
        st.session_state.diagnosis = None

    st.button("🔁 Recommencer", on_click=reset)

    patient_name = st.text_input("Nom du patient")
    date = st.text_input("Date", value=datetime.now().strftime("%d/%m/%Y"))

    node = traverse_tree(decision_tree, st.session_state.tree_path)

    if st.session_state.diagnosis:
        st.success(f"💡 Diagnostic suggéré : **{st.session_state.diagnosis}**")
        return

    if "question" in node:
        st.markdown(f"### {node['question']}")
        if "options" in node:
            for label in node["options"]:
                if st.button(label, key=f"opt_{len(st.session_state.tree_path)}_{label}"):
                    st.session_state.tree_path.append(label)
        else:
            if st.button("Oui", key=f"yes_{len(st.session_state.tree_path)}"):
                st.session_state.tree_path.append("yes")
            if st.button("Non", key=f"no_{len(st.session_state.tree_path)}"):
                st.session_state.tree_path.append("no")
    elif "diagnosis" in node:
        st.session_state.diagnosis = node["diagnosis"]
        st.success(f"💡 Diagnostic suggéré : **{node['diagnosis']}**")
        record = {
            "nom": patient_name,
            "date": date,
            "diagnostic": node["diagnosis"],
            "réponses": st.session_state.tree_path,
        }
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = []
        data.append(record)
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def show_history():
    st.header("📖 Historique des diagnostics")
    try:
        with open("history.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            for entry in reversed(data[-10:]):
                st.markdown(f"- **{entry['date']}** – {entry['nom']} → 🩺 {entry['diagnostic']}")
    except FileNotFoundError:
        st.info("Aucun historique enregistré.")

def main():
    st.markdown("## 🦵 Application d'aide au diagnostic de la hanche")
    tabs = st.tabs(["🏠 Accueil", "🧠 Arbre décisionnel", "📖 Historique"])

    with tabs[0]:
        st.write("Bienvenue dans l'outil d'évaluation interactive de la hanche.")
        st.info("Utilisez l'onglet **Arbre décisionnel** pour commencer une évaluation.")
    with tabs[1]:
        run_decision_tree()
    with tabs[2]:
        show_history()

if __name__ == "__main__":
    main()
