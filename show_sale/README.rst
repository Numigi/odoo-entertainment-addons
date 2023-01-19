Show Sale
=========

This module adds sales orders of type ``Show``.

.. contents:: Table of Contents

Configuration
-------------
In the form view of a sale order type, I find a new checkbox ``Show``.

.. image:: static/description/sale_order_type.png

When this box is checked, on the sale order, a new tab ``Show`` is displayed.

Overview
--------
I create a new sale order and select the type ``Show``.

.. image:: static/description/sale_order_new.png

A new ``Show`` tab is displayed.

.. image:: static/description/sale_order_show_tab.png

This tab allows to fill important information in the preparation of a show.

I select a project in the field ``Show``, then I save.

.. image:: static/description/sale_order_show_selected.png

In the form view of the selected show project, I notice a new smart button.

.. image:: static/description/project_smart_button.png

When I click on the button, the list of related sale orders is displayed.

.. image:: static/description/project_smart_button_sale_orders.png

When it is no uncancelled sale order related to project with type ``Show``, I notice a new button ``Create Sale``.

.. image:: static/description/create_so_button.png

If it is no sale order type with the field ``Show`` checked and I click on ``Create Sale`` button, an error message appears.

.. image:: static/description/so_type_not_found_popup.png

Once I create a sale order from the project,
I notice that the fields of this so ``Customer``, ``Analytic Account``, ``Show`` and ``Type`` are filled automatically.

Project form view:

.. image:: static/description/project_fields.png

Sale form view:

.. image:: static/description/so_fields.png

After saving the so, I go to the sale menu to create a new sale order and I select the previous project in the field ``Show``,
then a popup appears when I save.

.. image:: static/description/popup_so_form.png


Tickets
-------
Inside the ``Tickets`` section, there are two fields ``Ticket Prices`` and ``Service Fees``.

.. image:: static/description/ticket_section.png

Both fields allow to select a ``Customer Segment`` and a price.

Members of the group ``Sales / Manager`` can edit customer segments.
The list of segments can be found under the menu ``Sales / Configuration / Customer Segments``.

.. image:: static/description/customer_segment_menu.png

Organisation
------------
Inside the ``Organisation`` section, the fields ``Show Location`` and ``Location Capacity`` are readonly.

.. image:: static/description/sale_order_organisation.png

Those fields reflect the value selected on the project.

.. image:: static/description/project_show_place.png

Variable Remuneration
---------------------
Inside the ``Show`` tab an optional section ``Variable Remuneration`` allows
to define a contractual profit sharing between the selling company and the client.

.. image:: static/description/variable_remuneration.png

The sharing of profts can be either based on:

* A fixed expense amount
* The real cost engaged for the show

.. image:: static/description/variable_remuneration_type.png

In case of a sharing based on fixed expenses, a field allows to enter the fixed expense amount.

.. image:: static/description/variable_remuneration_fixed_amount.png

In case of a sharing based on real costs, a field allows to enter the forecasted cost for the show.

.. image:: static/description/variable_remuneration_forcasted_amount.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
