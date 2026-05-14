import streamlit as st
import pandas as pd

st.title("CGM 혈당 데이터 대시보드")
st.caption("10강 실습 과제: Streamlit을 활용한 Dexcom Clarity 혈당 데이터 시각화")

st.header("소개")
st.write("""
이 대시보드는 Dexcom Clarity에서 내보낸 CSV 파일을 불러와
혈당 이벤트 로그(EGV)만 추출한 뒤, 혈당 변화와 요약 지표를 시각화합니다.
사용자는 슬라이더를 이용해 분석할 기간을 선택할 수 있습니다.
""")

st.header("CSV 파일 업로드")
uploaded_file = st.file_uploader("Dexcom Clarity CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    raw_df = pd.read_csv(uploaded_file)

    st.header("원본 데이터 미리보기")
    st.dataframe(raw_df.head(20))

    # 필요한 컬럼명
    event_col = "이벤트 유형"
    time_col = "타임스탬프(YYYY-MM-DDThh:mm:ss)"
    glucose_col = "포도당 값 (mg/dL)"

    # 혈당 이벤트 로그(EGV)만 추출
    df = raw_df[raw_df[event_col] == "EGV"].copy()

    # 높음/낮음 전처리
    df[glucose_col] = df[glucose_col].replace({
        "높음": 400,
        "낮음": 40
    })

    # 시간 및 혈당값 변환
    df[time_col] = pd.to_datetime(df[time_col], errors="coerce")
    df[glucose_col] = pd.to_numeric(df[glucose_col], errors="coerce")

    # 결측 제거 및 시간순 정렬
    df = df.dropna(subset=[time_col, glucose_col])
    df = df.sort_values(time_col)

    st.header("전처리된 혈당 이벤트 로그")
    st.write(f"총 {len(df)}개의 혈당 기록을 불러왔습니다.")
    st.dataframe(df[[time_col, glucose_col]].head(100))

    st.header("분석 기간 설정")

    min_date = df[time_col].min().date()
    max_date = df[time_col].max().date()

    selected_range = st.slider(
        "표시할 기간을 선택하세요",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )

    filtered_df = df[
        (df[time_col].dt.date >= selected_range[0]) &
        (df[time_col].dt.date <= selected_range[1])
    ]

    st.header("요약 지표")

    avg_glucose = filtered_df[glucose_col].mean()
    max_glucose = filtered_df[glucose_col].max()
    min_glucose = filtered_df[glucose_col].min()

    tir = (
        ((filtered_df[glucose_col] >= 70) & (filtered_df[glucose_col] <= 180)).mean()
        * 100
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("평균 혈당", f"{avg_glucose:.1f} mg/dL")
    col2.metric("최고 혈당", f"{max_glucose:.0f} mg/dL")
    col3.metric("최저 혈당", f"{min_glucose:.0f} mg/dL")
    col4.metric("TIR", f"{tir:.1f}%")

    st.header("선택 기간 데이터")
    st.dataframe(filtered_df[[time_col, glucose_col]])

    st.header("혈당 변화 그래프")

    chart_df = filtered_df[[time_col, glucose_col]].copy()
    chart_df = chart_df.rename(columns={
        time_col: "시간",
        glucose_col: "혈당"
    })

    chart_df = chart_df.set_index("시간")

    st.line_chart(chart_df)

    st.markdown("""
    ### 전처리 기준
    - `이벤트 유형`이 `EGV`인 행만 혈당 이벤트 로그로 사용했습니다.
    - Dexcom Clarity에서 `높음`으로 기록된 값은 400 mg/dL로 대체했습니다.
    - Dexcom Clarity에서 `낮음`으로 기록된 값은 40 mg/dL로 대체했습니다.
    - 선택한 기간에 따라 표, 요약 지표, 그래프가 함께 바뀝니다.
    """)

else:
    st.info("Dexcom Clarity에서 내보낸 CSV 파일을 업로드하세요.")
