import streamlit as st
import subprocess
import re, time

# Define available scan options
scan_options = {
    "Ping Scan": "nmap -sP",
    "TCP Port Scan": "nmap -p1-65535",
    "UDP Port Scan": "nmap -pU 1-65535",
    "Version Scan": "nmap -sV",
    "Operating System Scan": "nmap -O",
    "Vulnerability Scan": "nmap --script=vuln",
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
        # Create a progress bar
        progress_bar = st.progress(0)

        # Run the scan in the background
        scan_command = f"{scan_options[selected_scan]} {filtered_target}"
        result = subprocess.run(scan_command, shell=True, capture_output=True, text=True)

        # Simulate a long-running process (replace with actual progress tracking)
        for i in range(100):
            time.sleep(0.1)
            progress_bar.progress(i + 1)

        # Display the scan results
        with st.expander("Scan Results"):
            st.markdown(f"<p>{result.stdout}</p>")

if __name__ == "__main__":
    main()