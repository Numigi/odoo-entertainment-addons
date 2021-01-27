FROM quay.io/numigi/odoo-public:12.latest
MAINTAINER numigi <contact@numigi.com>

USER root

COPY .docker_files/test-requirements.txt .
RUN pip3 install -r test-requirements.txt

ENV THIRD_PARTY_ADDONS /mnt/third-party-addons
RUN mkdir -p "${THIRD_PARTY_ADDONS}" && chown -R odoo "${THIRD_PARTY_ADDONS}"
COPY ./gitoo.yml /gitoo.yml
RUN gitoo install-all --conf_file /gitoo.yml --destination "${THIRD_PARTY_ADDONS}"

USER odoo

COPY account_recording_dimensions /mnt/extra-addons/account_recording_dimensions
COPY artist /mnt/extra-addons/artist
COPY artist_url_link /mnt/extra-addons/artist_url_link
COPY contact_birth_city /mnt/extra-addons/contact_birth_city
COPY musical_artwork /mnt/extra-addons/musical_artwork
COPY musical_catalog /mnt/extra-addons/musical_catalog
COPY partner_organization_membership /mnt/extra-addons/partner_organization_membership
COPY product_musical_relation /mnt/extra-addons/product_musical_relation
COPY project_role_show /mnt/extra-addons/project_role_show
COPY recording /mnt/extra-addons/recording
COPY recording_analytic /mnt/extra-addons/recording_analytic
COPY recording_artist /mnt/extra-addons/recording_artist
COPY recording_contributor /mnt/extra-addons/recording_contributor
COPY recording_external_revenue /mnt/extra-addons/recording_external_revenue
COPY recording_external_revenue_account /mnt/extra-addons/recording_external_revenue_account
COPY recording_genre /mnt/extra-addons/recording_genre
COPY recording_lang /mnt/extra-addons/recording_lang
COPY recording_lyrics /mnt/extra-addons/recording_lyrics
COPY recording_musical_artwork /mnt/extra-addons/recording_musical_artwork
COPY recording_platform /mnt/extra-addons/recording_platform
COPY recording_subgenre /mnt/extra-addons/recording_subgenre
COPY recording_tag /mnt/extra-addons/recording_tag
COPY recording_url_link /mnt/extra-addons/recording_url_link
COPY recording_version /mnt/extra-addons/recording_version
COPY show_place /mnt/extra-addons/show_place
COPY show_project /mnt/extra-addons/show_project
COPY show_project_sold_tickets /mnt/extra-addons/show_project_sold_tickets

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
