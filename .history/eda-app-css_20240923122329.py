
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk

# 加载数据，使用st.cache_data缓存
@st.cache_data
def load_data():
    data = pd.read_csv("housing.csv") 
    return data

data = load_data()

# 应用的CSS样式，但是streamlit好像有保护机制不支持大量页面的改变
st.markdown(
    """
    <style>
    /* 设置背景渐变 */
    .main {
        background: linear-gradient(135deg, #f3ec78, #af4261);
    }

    /* 标题字体颜色和样式 */
    h1 {
        font-family: 'Arial', sans-serif;
        color: #333 !important;
        font-size: 3em !important;
    }

    /* 恢复 sidebar 并添加渐变背景 */
    .css-1d391kg { 
        background: linear-gradient(135deg, #f3ec78, #af4261);
    }

    /* 自定义按钮 */
    .stButton>button {
        background-color: #008CBA !important;
        color: white !important;
        padding: 10px 24px !important;
        font-size: 16px !important;
        border-radius: 12px !important;
        transition: 0.3s !important;
    }

    .stButton>button:hover {
        background-color: #005f73 !important;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.1) !important;
    }

    /* 自定义滑块，添加小花背景 */
    .stSlider > div > div {
        background: url('https://www.publicdomainpictures.net/pictures/320000/nahled/flower-background.jpg') !important;
        border-radius: 10px !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# 应用标题
st.title("Housing Data App by YANLIN LIU")

# 侧边栏：多选框选择位置类型和收入水平过滤
st.sidebar.header("Filter Options")
location_types = data['ocean_proximity'].unique()
location_filter = st.sidebar.multiselect("Choose Location Type", options=location_types, default=location_types)

income_filter = st.sidebar.radio(
    "Choose Income Level",
    ("Low", "Medium", "High"),
    index=1
)

# 根据收入水平筛选
if income_filter == "Low":
    data = data[data["median_income"] <= 2.5]
elif income_filter == "Medium":
    data = data[(data["median_income"] > 2.5) & (data["median_income"] < 4.5)]
else:
    data = data[data["median_income"] >= 4.5]

# 根据位置类型筛选
data = data[data["ocean_proximity"].isin(location_filter)]

# 主体内容：房价滑块
price_slider = st.slider(
    "Minimal Median House Price",
    int(data["median_house_value"].min()),
    int(data["median_house_value"].max()),
    (int(data["median_house_value"].min()), int(data["median_house_value"].max()))
)

# 使用PyDeck显示房价的点图
st.subheader("See more filters in the sidebar")
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=data["latitude"].mean(),
        longitude=data["longitude"].mean(),
        zoom=10,
        pitch=0,  # 平面视角
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',  # 使用ScatterplotLayer绘制点图
            data=data[['latitude', 'longitude']],
            get_position='[longitude, latitude]',
            get_radius=2000,  # 半径
            get_fill_color=[255, 0, 0, 60],  # 使用RGBA设置颜色 (60表示透明度)
            pickable=True
        ),
    ],
))

# 绘制房价直方图
st.subheader("House Price Distribution")
plt.figure(figsize=(8, 6))
plt.hist(data["median_house_value"], bins=30,  range=(200000, 500001), color='royalblue', edgecolor='steelblue')
# median_house_value=500001有900多个样本
plt.xlabel("Median House Value")
plt.ylabel("Frequency")
st.pyplot(plt)