# =========================
# app_bien_ban_streamlit.py
# =========================
import streamlit as st
from google import genai
from docx import Document

# =========================
# 1) Nhập GEMINI_API_KEY
# =========================
API_KEY = st.text_input("Nhập GEMINI_API_KEY:", type="password")
if not API_KEY:
    st.warning("Vui lòng nhập GEMINI_API_KEY để tiếp tục.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# =========================
# 2) Giao diện upload file audio
# =========================
st.title("🤖 Trợ Lý Viết Biên Bản (VBI HCM - Gemini)")

uploaded_file = st.file_uploader(
    "Tải lên file ghi âm (.mp3, .wav, .flac):",
    type=["mp3", "wav", "flac"]
)

meeting_notes = st.text_area(
    "HOẶC Dán Nội Dung Cuộc Họp Thô vào đây:",
    height=200
)

# =========================
# 3) Xử lý khi nhấn nút "Soạn thảo biên bản"
# =========================
if st.button("Soạn thảo biên bản"):

    if uploaded_file is None and not meeting_notes.strip():
        st.warning("Vui lòng tải lên file hoặc dán nội dung cuộc họp.")
        st.stop()

    with st.spinner("Đang xử lý..."):

        system_instruction = """
        Bạn là chuyên gia viết biên bản họp cho công ty bảo hiểm phi nhân thọ.
        Hãy phiên âm file audio và viết thành biên bản họp hoàn chỉnh.
        Biên bản gồm: thời gian, địa điểm, người tham dự, nội dung chính, kết luận,
        công việc tiếp theo và người phụ trách.
        Văn phong hành chính, rõ ràng, ngắn gọn.
        """

        try:
            # --- Ưu tiên: file audio ---
            if uploaded_file is not None:
                st.info("Đang upload file audio lên Gemini...")

                # Lưu file tạm trên server Streamlit
                with open(f"/tmp/{uploaded_file.name}", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                filepath = f"/tmp/{uploaded_file.name}"

                # Upload lên Gemini
                gem_file = client.files.upload(file=filepath)

                contents = [
                    system_instruction,
                    gem_file,
                    "Hãy phiên âm file và viết biên bản họp hoàn chỉnh."
                ]
                model_to_use = "gemini-2.5-pro"

            # --- Nếu chỉ có text ---
            else:
                contents = system_instruction + "\n\nNội dung cuộc họp:\n" + meeting_notes
                model_to_use = "gemini-2.5-flash"

            # Gọi API tạo biên bản
            response = client.models.generate_content(
                model=model_to_use,
                contents=contents,
                config={"temperature": 0.1}
            )

            biens_ban_text = response.text

            st.subheader("📄 Biên bản hoàn chỉnh")
            st.text_area("Kết quả", biens_ban_text, height=300)

            # Xuất ra Word
            doc = Document()
            doc.add_heading('BIÊN BẢN CUỘC HỌP', 0)
            doc.add_paragraph(biens_ban_text)
            word_filename_

