import streamlit as st
import boto3

def get_sso_token():
    # Implement your SSO token retrieval logic here
    # For example, you might use a library like boto3's STS client
    # to exchange an SSO code for a session token

    return "your_sso_session_token"

def get_ec2_public_ips(access_key, secret_key, session_token):
    """Retrieves public IP addresses of EC2 instances using provided credentials and session token."""

    try:
        # Create an AWS session with the provided credentials and session token
        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token
        )

        # Get an EC2 client
        ec2 = session.client('ec2')

        # List all EC2 instances
        response = ec2.describe_instances()

        # Extract public IP addresses from the response
        public_ips = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if 'PublicIpAddress' in instance:
                    public_ips.append(instance['PublicIpAddress'])

        return public_ips

    except Exception as e:
        st.error(f"Error: {e}")
        return []

def main():
    st.title("AWS EC2 Public IP Retriever (SSO)")

    # Get user input for access key, secret key, and SSO token
    access_key = st.text_input("Access Key ID")
    secret_key = st.text_input("Secret Access Key")
    session_token = st.text_input("SSO Session Token")

    # Button to retrieve public IP addresses
    if st.button("Retrieve Public IPs"):
        # If SSO session token is empty, try to get it automatically
        if not session_token:
            session_token = get_sso_token()

        public_ips = get_ec2_public_ips(access_key, secret_key, session_token)

        if public_ips:
            st.success("Public IP addresses:")
            for ip in public_ips:
                st.write(ip)
        else:
            st.error("No public IP addresses found.")

if __name__ == "__main__":
    main()