import streamlit as st
import os

st.set_page_config(page_title="Water Quality Advisor")
st.title("💧 Water Quality Advisor")
st.markdown("_This is an educational demo — not a certified laboratory test._")

ph = st.number_input("pH", 0.0, 14.0, 7.0, step=0.1)
tds = st.number_input("TDS (ppm)", 0, 5000, 350)
turb = st.number_input("Turbidity (NTU)", 0.0, 100.0, 2.0, step=0.1)
color = st.selectbox("Color", ["None", "Slight", "Strong"])
smell = st.selectbox("Smell", ["None", "Mild", "Strong"])

def decide(ph, tds, turb, color, smell):
    if ph < 6.0 or ph > 9.0:
        return "Not Drinkable"
    if tds > 1000 or turb > 10 or color == "Strong" or smell == "Strong":
        return "Not Drinkable"
    if tds > 500 or turb > 5 or color == "Slight" or smell == "Mild":
        return "Needs Testing"
    return "Likely Drinkable"

if st.button("Check Water Quality"):
    decision = decide(ph, tds, turb, color, smell)
    st.subheader(f"Decision: {decision}")

    OPENAI_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_KEY:
        import openai
        openai.api_key = OPENAI_KEY
        prompt = (
            f"Water analysis: pH {ph}, TDS {tds} ppm, Turbidity {turb} NTU, "
            f"Color {color}, Smell {smell}. Decision: {decision}. "
            "Write a short explanation (3–4 sentences) and one practical next step. "
            "Add this line: 'This is an educational tool and not a certified laboratory test.'"
        )
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=180
            )
            text = resp['choices'][0]['message']['content'].strip()
            st.write(text)
        except Exception:
            st.warning("AI explanation not available. Showing static message.")
            st.write(f"The water is judged '{decision}'. Consider lab testing or filtration.")
    else:
        st.write(f"The water is judged '{decision}'. Consider lab testing or filtration.")
