# Gandi-DNS-Updater

This container is a simple script that updates a Gandi A record with the current 
public IP address of the host machine.

## Usage

1. Create a Gandi API key at https://account.gandi.net/
2. Run the container with the following command:

    ```bash
    $ sudo docker run -d --name gandi-dns-updater \
            -e GANDI_API_KEY=<API_KEY> \
            -e DOMAIN=<DOMAIN> \
            -e SUBDOMAIN=<SUBDOMAIN> \
            ghcr.io/owner/repository/gandi-dns-updater:latest
    ```
 
or copy and run docker-compose file:

   ```bash
   $ sudo docker-compose up -d
   ```
