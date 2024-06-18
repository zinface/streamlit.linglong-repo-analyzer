import streamlit as st


def _max_width_(prcnt_width:int = 75):
    '''调整 steamlit 页面显示宽度的比例，默认 75%'''
    max_width_str = f"max-width: {prcnt_width}rem;"
    st.markdown(f""" 
                <style> 
                .block-container{{{max_width_str}}}
                </style>    
                """, 
                unsafe_allow_html=True,
    )


