{
    "name": "Seasons Bakery",
    "version": "0.1",
    "summary": "A simple bakery management module for handling seasonal products.",
    "category": "Seasons Bakery",
    "depends": ["base", "mail", "hr"],
    "data": [

        "security/ir.model.access.csv",
        "views/seasons_branch_views.xml",
        "views/branch_region_views.xml",
        "views/branch_township_views.xml",
        "views/employee_views.xml",
        "views/seasons_bakery_menus.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
