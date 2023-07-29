#!/bin/bash

# Check if the script is run with root privileges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root. Please use 'sudo'." 
   exit 1
fi

# create required directories
mkdir -p /srv/jellyfin/{config,cache}

# Define your Docker Compose file
COMPOSE_FILE="docker-compose.yml"

# Step 1: Run the container in detached mode using Docker Compose
docker-compose -f "$COMPOSE_FILE" up -d

# Step 2: Wait for the container to start (if necessary)
# You can add a sleep or loop to wait for the container to be ready if needed.

sleep 60

# Step 3: Run commands inside the container using `docker exec`
# Here, you can run the initial setup commands you need inside the container.

# Example: Run multiple commands inside the container
echo "install the ROCm OpenCL runtime"
docker exec -u root -it jellyfin bash -c '
  apt update && apt install -y curl gpg
  mkdir -p /etc/apt/keyrings
  curl -fsSL https://repo.radeon.com/rocm/rocm.gpg.key | gpg --dearmor -o /etc/apt/keyrings/rocm.gpg
  cat <<EOF | tee /etc/apt/sources.list.d/rocm.sources
Types: deb
URIs: https://repo.radeon.com/rocm/apt/latest
Suites: ubuntu
Components: main
Architectures: amd64
Signed-By: /etc/apt/keyrings/rocm.gpg
EOF
  apt update && apt install -y rocm-opencl-runtime
  # Add more commands here if needed for your specific setup.
'

echo "Check the VA-API codecs"
docker exec -it jellyfin /usr/lib/jellyfin-ffmpeg/vainfo --display drm --device /dev/dri/renderD128
echo "Check the OpenCL runtime status"
docker exec -it jellyfin /usr/lib/jellyfin-ffmpeg/ffmpeg -v debug -init_hw_device opencl
echo "Check the Vulkan runtime status"
docker exec -it jellyfin /usr/lib/jellyfin-ffmpeg/ffmpeg -v debug -init_hw_device vulkan

# Step 4: Stop and remove the container (optional)
# Uncomment the following line if you want to stop and remove the container after the setup is done.
# docker-compose -f "$COMPOSE_FILE" down

