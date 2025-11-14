# =========================
# 1) CÀI ĐẶT THƯ VIỆN
# =========================
!pip install -q google-genai python-docx
from google import genai
from google.colab import files
from docx import Document

# =========================
# 2) NHẬP API KEY GEMINI
# =========================
API_KEY = input("Nhập GEMINI_API_KEY: ").strip()
client = genai.Client(api_key=API_KEY)

# =========================
# 3) PROMPT
# =========================
system_instruction = """
Bạn là chuyên gia viết biên bản họp cho công ty bảo hiểm phi nhân thọ.
Hãy phiên âm file audio và viết thành biên bản họp hoàn chỉnh.
Biên bản gồm: thời gian, địa điểm, người tham dự, nội dung chính, kết luận,
công việc tiếp theo và người phụ trách.
Văn phong hành chính, rõ ràng, ngắn gọn.
"""

# =========================
# 4) UPLOAD FILE AUDIO
# =========================
print("👉 Chọn file audio (.mp3, .wav, .flac) để upload:")
uploaded = files.upload()
filename = next(iter(uploaded))
filepath = f"/content/{filename}"
print("File đã upload vào Colab:", filepath)

# =========================
# 5) UPLOAD FILE LÊN GEMINI (SDK 1.49.0)
# =========================
gem_file = client.files.upload(file=filepath)  # ✅ Chuẩn 1.49.0
print("✅ Đã upload lên Gemini:", gem_file.name)

# =========================
# 6) GỌI MODEL PHIÊN ÂM + TẠO BIÊN BẢN
# =========================
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=[
        system_instruction,
        gem_file,
        "Hãy phiên âm file và viết biên bản họp hoàn chỉnh."
    ],
    config={"temperature": 0.1}
)

biens_ban_text = response.text
print("\n📄 BIÊN BẢN HOÀN CHỈNH\n")
print(biens_ban_text)

# =========================
# 7) XUẤT RA WORD (.docx)
# =========================
doc = Document()
doc.add_heading('BIÊN BẢN CUỘC HỌP', 0)
doc.add_paragraph(biens_ban_text)
word_filename = filename.rsplit('.',1)[0] + "_BienBan.docx"
doc.save(word_filename)
print("\n✅ Biên bản đã lưu ra Word:", word_filename)

# Cho phép tải file Word từ Colab
files.download(word_filename)

# =========================
# 8) XOÁ FILE TẠM TRÊN GEMINI
# =========================
client.files.delete(name=gem_file.name)
print("\n✅ Đã xoá file tạm trên Gemini.")
