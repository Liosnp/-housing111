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

# 引入 Bootstrap 的 CDN
bootstrap_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.2/dist/umd/popper.min.js"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
  <title>Housing Data App</title>
</head>
<body>

<div class="container">
  <div class="row">
    <div class="col-md-12">
      <h1 class="display-4">Housing Data App by YANLIN LIU</h1>
      <p class="lead">See more filters in the sidebar.</p>
    </div>
  </div>
  
  <div class="row mt-4">
    <div class="col-md-6">
      <h3>House Price Distribution</h3>
      <div id="histogram-placeholder"></div>
    </div>
    
    <div class="col-md-6">
      <h3>Map Visualization</h3>
      <div id="map-placeholder"></div>
    </div>
  </div>
</div>

</body>
</html>
"""

# 渲染 HTML
components.html(bootstrap_html, height=600)

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
sns.set()
plt.figure(figsize=(8, 6))
plt.hist(data['median_house_value'], bins=30, range=(200000, 500001),edgecolor='steelblue')
plt.xlabel("Median House Value")
plt.ylabel("Frequency")
st.pyplot(plt)