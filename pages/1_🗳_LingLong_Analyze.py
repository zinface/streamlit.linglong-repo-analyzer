import streamlit as st
import requests
import json


from backend.streamlitsettings  import _max_width_
_max_width_(st.sidebar.slider('屏幕比例', 30, 100, 75))

@st.cache_data
def get_app_list():
    applist_url = 'https://mirror-repo-linglong.deepin.com/api/v0/web-store/apps??page=1&size=100000'
    return json.loads(requests.get(applist_url).content.decode('utf-8'))['data']['list']

# {
#     "id": 291,
#     "appId": "app.web.baidu.map",
#     "name": "baidumap",
#     "version": "0.9.1",
#     "arch": "arm64",
#     "icon": "https://mirror-repo-linglong.deepin.com/icon/app.web.baidu.map.svg",
#     "description": "百度地图网页版。"
# },

@st.cache_data
def cache_get(app_icon_url):
    resp = requests.get(app_icon_url)
    print(resp.content)
    if resp.status_code == 307:
        resp = requests.get(resp.headers['Location'])
    if resp.headers['Content-Type'] == 'image/svg+xml':
        return resp.content.decode( errors='ignore')    
    return resp.content

import base64
def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img width=128 height=128 src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)


def intro():
        
    st.subheader('LingLong App')
        
    applist = [i['appId'] for i in get_app_list()]

    appId = st.selectbox(f'选择应用 - {len(applist)} 项', options=applist)
    for i in get_app_list():
        if i['appId'] == appId:
                    
            c_icon, c_info = st.columns([0.1, 0.9])
            with c_icon:
                icon = cache_get(i['icon'])
                # st.code(type(icon))
                if isinstance(icon, bytes):
                    st.image(icon, width=128)
                elif isinstance(icon, str):
                    render_svg(icon)
                else:
                    st.warning(icon)
            with c_info:
                st.table(i)
            break


def show_app_list():
    
    st.subheader('LingLong Apps ')
    
    applist = []
    must_list = get_app_list()
    loading = st.progress(0, '加载中')
    
    flush_view = st.dataframe(applist)
    for i, v in enumerate(must_list):
        loading.progress(int(i / len(must_list) * 100), '加载中...')
        applist.append(v)
        
        if i % 30 == 0:
            flush_view.dataframe(applist, use_container_width=True)
    loading.progress(100, f'加载完成，共 {len(must_list)} 项')
    if st.sidebar.checkbox('显示完整表格', value=False):
        flush_view.dataframe(must_list, use_container_width=True, height=700)
    else:
        flush_view.dataframe(must_list, use_container_width=True, height=700, column_config={
            'icon': st.column_config.ImageColumn('icon', width=32)
        })

page_names = {
    '-': intro,
    '应用列表信息': show_app_list,
}

page_name = st.sidebar.selectbox('选择功能', page_names)
page_names[page_name]()