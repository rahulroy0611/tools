import streamlit as st
import subprocess
import re

# Define available scan options
scan_options = {
    "Ping Scan": "nmap -sP",
    "TCP Port Scan": "nmap -p1-65535",
    "UDP Port Scan": "nmap -pU 1-65535",
    "Vulnerability Scan": "nmap -sV",
    "Operating System Scan": "nmap -O",
}

# Function to filter input for common injection attacks
def filter_input(input_str):
    """Filters input for common injection attacks."""

    # Command Injection
    input_str = re.sub(r'[\;\|\&\(\)\{\}\[\]\<\>]', '', input_str)

    # SQL Injection (basic)
    input_str = re.sub(r'[\'\"\;\\]', '', input_str)

    # XSS
    input_str = re.sub(r'<script[^>]*>.*?</script>', '', input_str, flags=re.DOTALL)
    input_str = re.sub(r'(on|href|src)=[\"\'](.*?)[\"\']', '', input_str, flags=re.IGNORECASE)

    return input_str

# Streamlit app
def main():
    st.title("Network Scanner")

    # User input for IP or domain
    target = st.text_input("Enter IP or Domain")

    # Filter the input before using it
    filtered_target = filter_input(target)

    # Dropdown for scan options
    selected_scan = st.selectbox("Select Scan Type", list(scan_options.keys()))

    # Button to initiate the scan
    if st.button("Scan"):
        # Run the scan in the background using subprocess
        scan_command = f"{scan_options[selected_scan]} {filtered_target}"
        result = subprocess.run(scan_command, shell=True, capture_output=True, text=True)

        # Display the scan results in a non-editable and auto-expandable text area
        with st.expander("Scan Results"):
            st.text_area("", result.stdout, height=None, max_chars=None)

if __name__ == "__main__":
    main()