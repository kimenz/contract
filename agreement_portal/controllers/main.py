# Copyright 2020-2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class PortalAgreement(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "agreement_count" in counters:
            agreement_count = 0
            agreement_model = request.env["agreement"]
            partner_id = request.env.user.partner_id
            if partner_id.parent_id:
                partner_id = partner_id.parent_id
            if agreement_model.check_access_rights("read", raise_exception=False):
                agreement_count = partner_id.agreements_count
            values["agreement_count"] = agreement_count
        return values

    def _agreement_get_page_view_values(self, agreement, access_token, **kwargs):
        fsm_equipment_model = request.env["fsm.equipment"]
        equipment_ids = fsm_equipment_model.search(
            [("agreement_id", "=", agreement.id)]
        )
        values = {
            "page_name": "Agreements",
            "agreement": agreement,
            "equipment_ids": equipment_ids,
        }
        return self._get_page_view_values(
            agreement, access_token, values, "my_agreements_history", False, **kwargs
        )

    def _get_filter_domain(self, kw):
        return []

    @http.route(
        ["/my/agreements", "/my/agreements/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_agreements(
        self, page=1, date_begin=None, date_end=None, sortby=None, **kw
    ):
        values = self._prepare_portal_layout_values()
        agreement_obj = request.env["agreement"]
        # Avoid error if the user does not have access.
        if not agreement_obj.check_access_rights("read", raise_exception=False):
            return request.redirect("/my")
        domain = self._get_filter_domain(kw)
        searchbar_sortings = {
            # "date": {"label": _("Date"), "order": "recurring_next_date desc"},
            "name": {"label": _("Name"), "order": "name desc"},
            "code": {"label": _("Reference"), "order": "code desc"},
        }
        # default sort by order
        if not sortby:
            sortby = "name"
        order = searchbar_sortings[sortby]["order"]
        # count for pager
        partner_id = request.env.user.partner_id
        if partner_id.parent_id:
            domain.append(["partner_id", "=", partner_id.parent_id.id])
            agreement_count = agreement_obj.sudo().search_count(domain)
        else:
            agreement_count = agreement_obj.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/agreements",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
            },
            total=agreement_count,
            page=page,
            step=self._items_per_page,
        )
        # content according to pager and archive selected
        if partner_id.parent_id:
            agreements = agreement_obj.sudo().search(
                domain, order=order, limit=self._items_per_page, offset=pager["offset"]
            )
        else:
            agreements = agreement_obj.search(
                domain, order=order, limit=self._items_per_page, offset=pager["offset"]
            )
        request.session["my_agreements_history"] = agreements.ids[:100]
        values.update(
            {
                "date": date_begin,
                "agreements": agreements,
                "page_name": "Agreements",
                "pager": pager,
                "default_url": "/my/agreements",
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
            }
        )
        return request.render("agreement_portal.portal_my_agreements", values)

    @http.route(
        ["/my/agreements/<int:agreement_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_agreement_detail(self, agreement_id, access_token=None, **kw):
        try:
            agreement_sudo = self._document_check_access(
                "agreement", agreement_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")
        values = self._agreement_get_page_view_values(
            agreement_sudo, access_token, **kw
        )
        return request.render("agreement_portal.portal_agreement_page", values)
