FROM eclipse-mosquitto:2.0.8

ARG MQTT_USER
ARG MQTT_PASSWORD

ENV PASSWORD_FILE /mosquitto/config/pwfile
ENV CONF_FILE /mosquitto/config/mosquitto.conf
ENV DATA_DIR /mosquitto/data/

RUN touch ${PASSWORD_FILE} && \
    mosquitto_passwd -b ${PASSWORD_FILE} ${MQTT_USER} ${MQTT_PASSWORD} && \
    touch ${CONF_FILE} && \
    echo 'allow_anonymous false' >> ${CONF_FILE} && \
    echo 'listener 1883' >> ${CONF_FILE} && \
    echo 'listener 9001' >> ${CONF_FILE} && \
    echo 'protocol websockets' >> ${CONF_FILE} && \
    echo 'persistence true' >> ${CONF_FILE} && \
    echo 'persistence_file mosquitto.db' >> ${CONF_FILE} && \
    echo "persistence_location ${DATA_DIR}" >> ${CONF_FILE} && \
    echo "password_file ${PASSWORD_FILE}" >> ${CONF_FILE}
