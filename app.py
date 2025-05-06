import streamlit as st
from agent import agent_executor

st.title("👕 Hava Durumuna Göre Kıyafet Önerisi")
st.markdown("Bugünkü havaya göre ne giymeliyim? Şehri seç, sana önerelim!")

city = st.text_input("Şehir adını girin", placeholder="İstanbul, Ankara, İzmir...")

if st.button("Öner"):
    if not city:
        st.warning("Lütfen bir şehir adı girin.")
    else:
        try:
            result = agent_executor.invoke({"input": f"Get the weather for {city} and recommend appropriate clothing."})
            st.success("İşte sana özel öneriler 👇")
            st.markdown(result["output"])
        except Exception as e:
            st.error("Bir hata oluştu.")
            st.code(str(e), language="bash")
