import streamlit as st
import subprocess
st.title("Run Youtube Music using mpv")
ytm_url = st.text_input("Enter YouTube Music URL to Play", key="user_input")


# Initialize volume in session state if not present
if "current_vol" not in st.session_state:
    st.session_state.current_vol = 50

def update_volume():
    new_val = st.session_state.vol_slider
    cmd = f"echo 'set volume {new_val}' | socat - /tmp/mpvsocket"
    subprocess.run(cmd, shell=True)
    st.session_state.current_vol = new_val


def send_mpv_command(cmd):
    full_cmd = f"echo '{cmd}' | socat - /tmp/mpvsocket"
    subprocess.run(full_cmd, shell=True)

# Initialize the key in session state
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""


def add_to_queue(url):
    cmd = f'loadfile "{url}" append'
    full_shell_cmd = f"echo '{cmd}' | socat - /tmp/mpvsocket"
    subprocess.run(full_shell_cmd, shell=True)

def clear_text():
    st.session_state.user_input = ""

def stop_play():
    mpv_command = "pkill mpv && rm /tmp/mpvsocket"
    result = subprocess.run([mpv_command], capture_output=True, shell=True)
    st.write(result)
    #st.success(f"Result is , {result.stdout}! ")
        
#col1, col2 = st.columns([2, 1])
col1, col2, col3 = st.columns(3)    

with col2:
    st.button("Clear", on_click=clear_text)
    st.button("Stop Play", on_click=stop_play) 

# create button
with col1:
    if st.button("Play"):
        if ytm_url:
            mpv_command = "mpv --no-video --input-ipc-server=/tmp/mpvsocket " + ytm_url
            result = subprocess.run([mpv_command], capture_output=True, shell=True)
            st.success(f"Result is , {result.stdout}! ")
        else:
            st.warning("Please enter a YouTube Music URL first.")
            
    st.button("Add To Queue", on_click=add_to_queue(ytm_url))
    # The slider triggers 'update_volume' immediately on release
    st.slider("Volume Control",50, 120, key="vol_slider", on_change=update_volume)
    st.write(f"Current Volume: **{st.session_state.current_vol}%**")

   
#col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⏮️ Previous", use_container_width=True):
        send_mpv_command("playlist-prev")

with col2:
    # We use "cycle pause" so one button handles both Play and Pause
    if st.button("⏯️ Play / Pause", use_container_width=True):
        send_mpv_command("cycle pause")

with col3:
    if st.button("⏭️ Next", use_container_width=True):
        send_mpv_command("playlist-next")



