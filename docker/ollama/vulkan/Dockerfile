FROM --platform=linux/amd64 library/ubuntu:noble
RUN \
    apt-get update && \
    apt-get install -y ca-certificates libcap2 libvulkan1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
COPY ./dist/lib/ollama/ /lib/ollama/
COPY ./dist/lib/ollama/vulkan/ /lib/ollama/vulkan/
COPY ./dist/bin/ /bin/

RUN find /lib/ollama && find /bin/ollama

EXPOSE 11434
ENV OLLAMA_HOST 0.0.0.0

USER root

RUN setcap "cap_perfmon=+ep" /bin/ollama

ENTRYPOINT ["/bin/ollama"]
CMD ["serve"]
