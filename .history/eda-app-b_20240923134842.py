import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import seaborn as sns
import streamlit.components.v1 as components

# 加载数据，使用st.cache_data缓存
@st.cache_data
def load_data():
    data = pd.read_csv("housing.csv") 
    return data

data = load_data()

# 引入 Google Fonts 和高级风格的 CSS
bootstrap_aos_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  
  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Roboto:wght@300;500&display=swap" rel="stylesheet">
  
  <!-- AOS CSS for scroll animations -->
  <link href="https://cdn.jsdelivr.net/npm/aos@2.3.1/dist/aos.css" rel="stylesheet">

  <!-- jQuery and Bootstrap JS -->
  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.2/dist/umd/popper.min.js"></script>

  <!-- AOS JS -->
  <script src="https://cdn.jsdelivr.net/npm/aos@2.3.1/dist/aos.js"></script>

  <title>Housing Data App</title>

  <style>
    /* 设置背景渐变效果，使用较柔和的颜色 */
    body {
      background: linear-gradient(135deg, #f9d423, #ff4e50);
      color: #fff;
      font-family: 'Montserrat', sans-serif;
    }

    /* 设置容器 */
    .container {
      margin-top: 50px;
    }

    /* 设置卡片样式，带圆角和阴影 */
    .card {
      background-color: rgba(255, 255, 255, 0.2);
      border: none;
      border-radius: 12px;
      box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    }

    /* 标题样式 */
    h1, h3 {
      font-family: 'Montserrat', sans-serif;
      font-weight: 700;
    }

    /* 副标题文字样式 */
    p.lead {
      font-family: 'Roboto', sans-serif;
      font-weight: 300;
    }

    /* 滑块样式 */
    .stSlider > div > div > div {
        background: #f9d423;
        border-radius: 8px;
    }

    /* 按钮样式 */
    .stButton>button {
        background-color: #ff4e50 !important;
        color: white !important;
        padding: 10px 24px !important;
        border-radius: 10px !important;
        transition: 0.3s ease-in-out !important;
        font-family: 'Montserrat', sans-serif;
    }

    .stButton>button:hover {
        background-color: #f9d423 !important;
        color: #fff !important;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1) !important;
    }

    /* AOS 动效初始化 */
    script {
      AOS.init();
    }
  </style>
</head>
<body>

<!-- Initialize AOS animations -->
<script>
  AOS.init();
</script>

<div class="container">
  <!-- 顶部介绍 -->
  <div class="row">
    <div class="col-md-12">
      <h1 class="display-4" data-aos="fade-up">Housing Data App by YANLIN LIU</h1>
      <p class="lead" data-aos="fade-up">See more filters in the sidebar.</p>
    </div>
  </div>

  <!-- 卡片内容 -->
  <div class="row mt-4">
    <div class="col-md-6">
      <div class="card" data-aos="fade-right">
        <div class="card-body">
          <h3 class="card-title">House Price Distribution</h3>
          <div id="histogram-placeholder"></div>
        </div>
      </div>
    </div>

    <div class="col-md-6">
      <div class="card" data-aos="fade-left">
        <div class="card-body">
          <h3 class="card-title">Map Visualization</h3>
          <div id="map-placeholder"></div>
        </div>
      </div>
    </div>
  </div>
</div>

</body>
</html>
"""

# 渲染 HTML 和动态效果
components.html(bootstrap_aos_html, height=1000)

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
sns.set()
plt.figure(figsize=(8, 6))
plt.hist(data['median_house_value'], bins=30, range=(200000, 500001), edgecolor='steelblue')
plt.xlabel("Median House Value")
plt.ylabel("Frequency")
st.pyplot(plt)