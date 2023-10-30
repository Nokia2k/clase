FROM ubuntu:rolling

RUN apt update && apt install kea --yes && rm -rf /var/cache/apt/*

COPY kea-dhcp4.config /etc/kea

CMD ["systemctl", "restart", "isc-kea-dhcp4-server"]
