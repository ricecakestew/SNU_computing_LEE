import streamlit as st
import pandas as pd
import numpy as np

# ── 여기서부터 자유롭게 수정하세요 ───────────────

st.title("CGM 데이터 시각화 앱")   # ← 제목을 바꿔보세요

# ── 사이드바 ──────────────────────────────────
st.sidebar.title("설정")

n = st.sidebar.slider(
    "데이터 개수",
    min_value=10,    # ← 최솟값을 바꿔보세요
    max_value=100,   # ← 최댓값을 바꿔보세요
    value=30
)

# ── 메인 화면 ─────────────────────────────────
st.write("CGM 데이터를 시각화하는 앱입니다.")   # ← 설명을 바꿔보세요

data = pd.DataFrame(
    np.random.normal(140, 30, n)
)

st.line_chart(data)

st.dataframe(data.head(5))

# ── 여기까지 ──────────────────────────────────
