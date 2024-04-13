FROM eclipse-mosquitto:2.0.8

ARG MQTT_USER
ARG MQTT_PASSWORD

ENV PASSWORD_FILE /mosquitto/config/pwfile

COPY ./mosquitto.conf /mosquitto/config/mosquitto.conf

RUN touch ${PASSWORD_FILE} && \
    mosquitto_passwd -b ${PASSWORD_FILE} ${MQTT_USER} ${MQTT_PASSWORD} && \
    echo "password_file ${PASSWORD_FILE}" >> /mosquitto/config/mosquitto.conf
