import streamlit as st
import requests

# Sayfa Yapılandırması
st.set_page_config(page_title="Lise Ders Asistanı", page_icon="🎓", layout="centered")

st.title("🎓 Lise Ders Asistanı")
st.write("10. ve 11. sınıf müfredatına uygun akıllı ders çalışma arkadaşın.")

# Hugging Face ücretsiz model bağlantısı (Qwen 2.5 7B)
API_URL = "https://huggingface.co"

# Sohbet geçmişini hafızada tutma
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekrana yazdırma
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan soru alma
if prompt := st.chat_input("Dersinle ilgili bir soru sor (Örn: 11. Sınıf Fizik Vektörler)..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Yapay zekaya okul odaklı sistem komutu verme
    sistem_komutu = "Sen lise 10. ve 11. sınıf öğrencilerine yardımcı olan uzman bir öğretmensin. Soruları adım adım, formülleri açıklayarak, net ve Türkçe bir dille çöz."
    
    payload = {
        "inputs": f"<|system|>\n{sistem_komutu}\n<|user|>\n{prompt}\n<|assistant|>\n",
        "parameters": {"max_new_tokens": 1024, "temperature": 0.7}
    }

    with st.chat_message("assistant"):
        with st.spinner("Öğretmeniniz düşünüyor..."):
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    cevap = response.json()[0]['generated_text'].split("<|assistant|>\n")[-1]
                    st.markdown(cevap)
                    st.session_state.messages.append({"role": "assistant", "content": cevap})
                else:
                    st.error("Bağlantı hatası oluştu. Lütfen tekrar deneyin.")
            except:
                st.error("Bir sorun oluştu, lütfen soruyu tekrar gönderin.")
