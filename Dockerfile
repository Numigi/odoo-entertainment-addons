FROM quay.io/numigi/odoo-public:12.0
MAINTAINER numigi <contact@numigi.com>

USER root

COPY .docker_files/test-requirements.txt .
RUN pip3 install -r test-requirements.txt

ENV THIRD_PARTY_ADDONS /mnt/third-party-addons
RUN mkdir -p "${THIRD_PARTY_ADDONS}" && chown -R odoo "${THIRD_PARTY_ADDONS}"
COPY ./gitoo.yml /gitoo.yml
RUN gitoo install-all --conf_file /gitoo.yml --destination "${THIRD_PARTY_ADDONS}"

USER odoo

COPY artist /mnt/extra-addons/artist
COPY artist_url_link /mnt/extra-addons/artist_url_link
COPY musical_artwork /mnt/extra-addons/musical_artwork
COPY recording /mnt/extra-addons/recording
COPY recording_artist /mnt/extra-addons/recording_artist
COPY recording_contributor /mnt/extra-addons/recording_contributor
COPY recording_kind /mnt/extra-addons/recording_kind
COPY recording_lang /mnt/extra-addons/recording_lang
COPY recording_subkind /mnt/extra-addons/recording_subkind
COPY recording_tag /mnt/extra-addons/recording_tag
COPY recording_url_link /mnt/extra-addons/recording_url_link
COPY recording_version /mnt/extra-addons/recording_version
COPY show_place /mnt/extra-addons/show_place

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
