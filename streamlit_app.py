import streamlit as st
from pdf2image import convert_from_path
from PIL import Image
import os
from io import BytesIO
import tempfile

# Streamlit 웹앱 제목 설정
st.title("PDF to JPG Converter")

# 사용자로부터 PDF 파일 업로드 받기
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# PDF를 이미지로 변환하는 함수
def pdf_to_images(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read())
        tmp_file_path = tmp_file.name
    images = convert_from_path(tmp_file_path, dpi=300)
    os.remove(tmp_file_path)  # 변환 후 임시 파일 삭제
    return images

# 이미지 다운로드를 위한 함수
def image_to_bytes(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return buffered.getvalue()

# 사용자가 파일을 업로드한 경우
if uploaded_file:
    # PDF를 이미지로 변환
    images = pdf_to_images(uploaded_file)

    st.write(f"Total pages: {len(images)}")

    # 각 페이지를 이미지로 변환하고 화면에 표시
    for i, img in enumerate(images):
        st.image(img, caption=f"Page {i+1}", use_column_width=True)

        # 이미지 다운로드 버튼 추가
        img_bytes = image_to_bytes(img)
        st.download_button(
            label=f"Download Page {i+1} as JPG",
            data=img_bytes,
            file_name=f"page_{i+1}.jpg",
            mime="image/jpeg"
        )
