import streamlit as st
from src.ui.panels.live_scoreboard import render_scoreboard

st.text(render_scoreboard(states=[]))
