import streamlit as st
import requests

def check_http_methods(domain):
    """Checks the available HTTP methods for a given domain name.

    Args:
        domain (str): The domain name to check.

    Returns:
        list: A list of available HTTP methods.
    """

    try:
        response = requests.options(f"http://{domain}")
        allowed_methods = response.headers.get('Allow', '').split(', ')
        return allowed_methods
    except requests.exceptions.RequestException as e:
        print(f"Error checking HTTP methods for {domain}: {e}")
        return []

def main():
    st.title("HTTP Methods Checker")

    domain = st.text_input("Enter a domain name:")

    if st.button("Check Methods"):
        allowed_methods = check_http_methods(domain)
        if allowed_methods:
            st.success(f"Available HTTP methods for {domain}: {allowed_methods}")
        else:
            st.error(f"No HTTP methods available for {domain}")

if __name__ == "__main__":
    main()