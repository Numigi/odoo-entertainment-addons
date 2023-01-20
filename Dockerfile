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
COPY crm_musical_relation /mnt/extra-addons/crm_musical_relation
COPY crm_production_title /mnt/extra-addons/crm_production_title
COPY musical_artwork /mnt/extra-addons/musical_artwork
COPY musical_catalog /mnt/extra-addons/musical_catalog
COPY partner_organization_membership /mnt/extra-addons/partner_organization_membership
COPY product_musical_relation /mnt/extra-addons/product_musical_relation
COPY recording /mnt/extra-addons/recording
COPY recording_analytic /mnt/extra-addons/recording_analytic
COPY recording_artist /mnt/extra-addons/recording_artist
COPY recording_contributor /mnt/extra-addons/recording_contributor
COPY recording_credential_format /mnt/extra-addons/recording_credential_format
COPY recording_external_revenue /mnt/extra-addons/recording_external_revenue
COPY recording_external_revenue_account /mnt/extra-addons/recording_external_revenue_account
COPY recording_genre /mnt/extra-addons/recording_genre
COPY recording_lang /mnt/extra-addons/recording_lang
COPY recording_lyrics /mnt/extra-addons/recording_lyrics
COPY recording_musical_artwork /mnt/extra-addons/recording_musical_artwork
COPY recording_platform /mnt/extra-addons/recording_platform
COPY recording_status /mnt/extra-addons/recording_status
COPY recording_subgenre /mnt/extra-addons/recording_subgenre
COPY recording_tag /mnt/extra-addons/recording_tag
COPY recording_url_link /mnt/extra-addons/recording_url_link
COPY recording_version /mnt/extra-addons/recording_version
COPY show_appearance_type /mnt/extra-addons/show_appearance_type
COPY show_place /mnt/extra-addons/show_place
COPY show_project /mnt/extra-addons/show_project
COPY show_project_access /mnt/extra-addons/show_project_access
COPY show_project_artwork /mnt/extra-addons/show_project_artwork
COPY show_project_custom_view /mnt/extra-addons/show_project_custom_view
COPY show_project_perdiem /mnt/extra-addons/show_project_perdiem
COPY show_project_fee /mnt/extra-addons/show_project_fee
COPY show_project_list /mnt/extra-addons/show_project_list
COPY show_project_promotion /mnt/extra-addons/show_project_promotion
COPY show_project_role /mnt/extra-addons/show_project_role
COPY show_project_sale /mnt/extra-addons/show_project_sale
COPY show_project_sold_tickets /mnt/extra-addons/show_project_sold_tickets
COPY show_sale /mnt/extra-addons/show_sale

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
