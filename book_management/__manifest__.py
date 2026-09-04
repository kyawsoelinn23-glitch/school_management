{
    "name": "Book Management",
    "version": "1.0",
    "summary": "Manage books in the library",
    "description": "This module allows you to manage books in the library, including adding, editing, and deleting book records.",
    "author": "Your Name",
    "category": "Library",
    "depends": ["base", "contacts",],
    "data": [
        "security/library_security.xml",
        "security/ir.model.access.csv",

        "sequences/library_borrow_sequence.xml",
        "sequences/library_book_sequence.xml",
        "sequences/library_member_sequence.xml",

        "report/library_borrow_report.xml",
        "report/library_borrow_receipt_template.xml",

        "views/res_partner_views.xml",
        "views/library_author_views.xml",
        "views/library_book_category_views.xml",
        "views/library_borrow_views.xml",
        "views/library_book_views.xml",
    ],

    "installable": True,
    "application": True,
    "license": "LGPL-3"
}