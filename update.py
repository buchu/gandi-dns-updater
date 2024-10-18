import requests
import time
import logging
import os
import socket

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_public_ip():
    """
    Function to get the public IP address using the ipify API.
    """
    try:
        response = requests.get("https://api.ipify.org")
        if response.status_code == 200:
            return response.text
        else:
            raise Exception("Failed to get public IP")
    except Exception as e:
        logging.error(f"Error getting public IP: {e}")
        return None


def get_current_dns_ip(domain, subdomain):
    """
    Function to resolve the current DNS A record for the given domain and subdomain.
    """
    try:
        full_domain = f"{subdomain}.{domain}"
        current_ip = socket.gethostbyname(full_domain)
        return current_ip
    except socket.gaierror as e:
        logging.error(f"Error resolving DNS for {subdomain}.{domain}: {e}")
        return None


def update_gandi_dns_record(domain, subdomain, ip_address, api_key):
    """
    Function to update the DNS A record on Gandi's LiveDNS API.
    Updates the record only if the public IP has changed.
    """
    url = f"https://api.gandi.net/v5/livedns/domains/{domain}/records/{subdomain}/A"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    data = {
        "rrset_values": [ip_address],
        "rrset_ttl": 300,  # Time to live (TTL) for the DNS record
    }

    # Make the API call to update the DNS record
    response = requests.put(url, json=data, headers=headers, verify=False)

    if response.status_code == 201:
        logging.info(f"DNS record for {subdomain}.{domain} updated to {ip_address}")
    else:
        logging.error(
            f"Failed to update DNS record: {response.status_code} - {response.text}"
        )


def main(api_key, domain, subdomain):
    """
    Main function to monitor the public IP and update Gandi DNS if the IP has changed.
    """

    public_ip = get_public_ip()
    if public_ip is None:
        logging.error("Could not retrieve public IP.")
    else:
        logging.info(f"Set current public IP: {public_ip} for {subdomain}.{domain}")
        update_gandi_dns_record(domain, subdomain, public_ip, api_key)

    while True:
        # Get the current public IP
        public_ip = get_public_ip()

        if public_ip is None:
            logging.error("Could not retrieve public IP.")
        else:
            # Get the current DNS IP
            current_dns_ip = get_current_dns_ip(domain, subdomain)

            if current_dns_ip is None:
                logging.error(f"Could not resolve DNS for {subdomain}.{domain}")
            else:
                logging.info(
                    f"Current DNS IP for {subdomain}.{domain} is {current_dns_ip}"
                )

                # Compare the public IP with the DNS IP before making the API call
                if public_ip != current_dns_ip:
                    logging.info(
                        f"Public IP {public_ip} is different from DNS IP "
                        f"{current_dns_ip}. Updating DNS record..."
                    )
                    update_gandi_dns_record(domain, subdomain, public_ip, api_key)
                else:
                    logging.info(
                        f"Public IP {public_ip} matches the DNS IP {current_dns_ip}. "
                        f"No update needed."
                    )

        # Sleep for 1 minute before checking again
        time.sleep(60)


if __name__ == "__main__":
    # Load sensitive data from environment variables for better security
    api_key = os.getenv("GANDI_API_KEY")
    domain = os.getenv("DOMAIN")
    subdomain = os.getenv("SUBDOMAIN")

    main(api_key, domain, subdomain)
