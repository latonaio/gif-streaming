FROM latonaio/l4t:latest

# Definition of a Device & Service
ENV POSITION=Runtime \
    SERVICE=gif-streaming \
    AION_HOME=/var/lib/aion
# ENV GRPC_TRACE=all
# ENV GRPC_VERBOSITY=DEBUG
# Setup Directoties
RUN mkdir -p /${AION_HOME}/$POSITION/$SERVICE

WORKDIR /${AION_HOME}/$POSITION/$SERVICE


ADD . .

# Install dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt

CMD ["python3", "main.py"]
