import streamlit as st
import subprocess

# Define available scan options
scan_options = {
    "Ping Scan": "nmap -sP",
    "TCP Port Scan": "nmap -p1-65535",
    "UDP Port Scan": "nmap -pU 1-65535",
    "Vulnerability Scan": "nmap -sV",
    "Operating System Scan": "nmap -O",
}

# Streamlit app
def main():
    st.title("Network Scanner")

    # User input for IP or domain
    target = st.text_input("Enter IP or Domain")

    # Dropdown for scan options
    selected_scan = st.selectbox("Select Scan Type", list(scan_options.keys()))

    # Button to initiate the scan
    if st.button("Scan"):
        # Run the scan in the background using subprocess
        scan_command = f"{scan_options[selected_scan]} {target}"
        result = subprocess.run(scan_command, shell=True, capture_output=True, text=True)

        # Display the scan results
        st.text_area("Scan Results", result.stdout, height=None, max_chars=None)

if __name__ == "__main__":
    main()