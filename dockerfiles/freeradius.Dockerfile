FROM freeradius/freeradius-server:3.2.7

ARG KAFKA_BOOTSTRAP_SERVER

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Create the required directory for your custom Python scripts
RUN mkdir -p /cgn_ec_freeradius

ENV PYTHONPATH="/cgn_ec_freeradius:$PYTHONPATH"

RUN /usr/bin/python3 -m pip install confluent-kafka==2.8.2

# Set the virtual environment as default
ENV PATH="/venv/bin:$PATH"

# Copy your custom Python scripts to /cgn_ec_freeradius/mods-config/python3
COPY ./producer/radius/python3 /cgn_ec_freeradius

# Ensure permissions for the custom Python script
RUN chown -R freerad:freerad /cgn_ec_freeradius && \
    chmod -R 755 /cgn_ec_freeradius

COPY ./producer/radius/dictionaries/* /usr/share/freeradius

RUN echo '$INCLUDE dictionary.nfware' >> /usr/share/freeradius/dictionary