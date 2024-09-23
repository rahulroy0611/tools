import streamlit as st
import boto3
import io

# List of all AWS regions
regions = [
    "us-east-1", "us-east-2", "us-west-1", "us-west-2", "ap-south-1", "ap-northeast-1",
    "ap-northeast-2", "ap-northeast-3", "ap-southeast-1", "ap-southeast-2",
    "ca-central-1", "eu-central-1", "eu-north-1", "eu-west-1", "eu-west-2",
    "eu-west-3", "sa-east-1", "us-gov-east-1", "us-gov-west-1", "me-south-1"
]

def get_sso_token():
    # Implement your SSO token retrieval logic here
    # For example, you might use a library like boto3's STS client
    # to exchange an SSO code for a session token

    return "your_sso_session_token"

def get_ec2_private_ips(access_key, secret_key, session_token, region):
    """Retrieves public IP addresses of EC2 instances using provided credentials and region."""

    try:
        # Create an AWS session with the provided credentials and region
        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token,
            region_name=region
        )

        # Get an EC2 client
        ec2 = session.client('ec2')

        # List all EC2 instances
        response = ec2.describe_instances()

        # Extract public IP addresses from the response
        public_ips = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if 'PrivateIpAddress' in instance:
                    public_ips.append(instance['PrivateIpAddress'])

        return public_ips

    except Exception as e:
        st.error(f"Error: {e}")
        return []

def main():
    st.title("AWS EC2 Private IP Retriever (SSO)")

    # Get user input for access key, secret key, SSO token, and region
    access_key = st.text_input("Access Key ID")
    secret_key = st.text_input("Secret Access Key")
    session_token = st.text_input("SSO Session Token")
    region = st.selectbox("AWS Region", regions)

    # Button to retrieve public IP addresses
    if st.button("Retrieve Private IPs"):
        # If SSO session token is empty, try to get it automatically
        if not session_token:
            session_token = get_sso_token()

        public_ips = get_ec2_private_ips(access_key, secret_key, session_token, region)

        if public_ips:
            st.success("Retrive Private Addresses")
            # for ip in public_ips:
            #     st.write(ip)

            # Create a text file with the IP addresses
            text_data = "\n".join(public_ips)
            text_file = "ec2_private_ips.txt"

            # Download the text file
            st.download_button(
                label="Download",
                data=text_data,
                file_name=text_file
            )

if __name__ == "__main__":
    main()