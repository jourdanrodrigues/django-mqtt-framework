FROM eclipse-mosquitto:2.0.8

ARG MQTT_USER
ARG MQTT_PASSWORD

ENV PASSWORD_FILE /mosquitto/config/pwfile
ENV CONF_FILE /mosquitto/config/mosquitto.conf
ENV DATA_DIR /mosquitto/data/

RUN touch ${PASSWORD_FILE} && \
    mosquitto_passwd -b ${PASSWORD_FILE} ${MQTT_USER} ${MQTT_PASSWORD} && \
    sed -i 's|^#allow_anonymous .*|allow_anonymous false|' ${CONF_FILE} && \
    sed -i 's|^#listener$|listener 1883|' ${CONF_FILE} && \
    sed -i 's|^#protocol .*|protocol mqtt|' ${CONF_FILE} && \
    sed -i "s|^#persistence_location$|persistence_location ${DATA_DIR}|" ${CONF_FILE} && \
    sed -i 's|^#persistence_file \(.*\)|persistence_file \1|' ${CONF_FILE} && \
    sed -i "s|^#persistence .*|persistence true|" ${CONF_FILE} && \
    sed -i "s|^#password_file|password_file ${PASSWORD_FILE}|" ${CONF_FILE}
