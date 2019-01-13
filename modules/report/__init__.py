# security/__init__.py
import warnings

from flask import Blueprint
from flask_restful import Api

from modules import app
from modules.extensions import admin
from modules.utilities.route_builder import build_routes

sla_report_bp = Blueprint('sla_report_bp', __name__)
sla_report_api = Api(sla_report_bp)


""" Create models for module in dB """
with app.app_context():
    import modules.report.models
    import modules.report.views

    # Register the admin views to the extension
    # Ignore warning messages from overridden fields
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', 'Fields missing from ruleset', UserWarning)

        # Report Data Views: Admin Area
        admin.add_view(
            views.TablesLoadedView(
                models.TablesLoadedModel,
                models.TablesLoadedModel.session,
                name='Report Data', category="SLA Admin"
            )
        )

    # Report Views: All
    admin.add_view(
        views.SLAReportView(
            models.SlaReportModel,
            models.SlaReportModel.session,
            name='SLA Reports', category="SLA Admin"
        )
    )
    admin.add_view(
        views.SLASummaryReportView(
            models.SummarySLAReportModel,
            models.SummarySLAReportModel.session,
            name='Summary Reports', category="SLA Admin"
        )
    )

    # Client Manager Views: Manager Area
    admin.add_view(
        views.ClientManagerView(
            models.ClientManager,
            models.ClientManager.session,
            name="Client Managers", category="User Admin"
        )
    )

    # Client Manager Views: Admin Area
    admin.add_view(
        views.ClientView(
            models.ClientModel,
            models.ClientModel.session,
            name='Add/Remove Clients', category="SLA Admin"
        )
    )

    admin.add_view(
        views.CallDataView(
            models.CallTableModel,
            models.CallTableModel.session,
            name='Raw Call Data', category="SLA Admin"
        )
    )
    admin.add_view(
        views.EventDataView(
            models.EventTableModel,
            models.EventTableModel.session,
            name='Raw Event Data', category="SLA Admin"
        )
    )


app.register_blueprint(sla_report_bp)

# Inject module routes
build_routes(app, sla_report_api, "report")
