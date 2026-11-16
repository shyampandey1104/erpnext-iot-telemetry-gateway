# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "simulator"
app_title = "Erpnext Iot Telemetry Gateway"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Iot Telemetry Gateway for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/simulator/css/simulator.bundle.css"
app_include_js = "/assets/simulator/js/simulator.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "simulator.engine.on_document_submit",
        "on_cancel": "simulator.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "simulator.engine.daily_scheduled_sync"
    ]
}
