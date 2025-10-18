from __future__ import annotations

import openpyxl
from typing import Any

from django.core.files.uploadedfile import UploadedFile

from server.apps.workers.models import Worker


ERROR = 'error'


class WorkerImportService:
    """Service for importing workers from Excel."""

    def __init__(self) -> None:
        self.created_count = 0
        self.errors: list[dict[str, Any]] = []

    def import_from_excel(self, file: UploadedFile) -> dict[str, Any]:
        """Imports workers from Excel-file."""
        try:
            workbook = openpyxl.load_workbook(file)
        except Exception:
            return {
                'created': 0,
                'errors': [{ERROR: 'Excel file cannot be read.'}],
            }

        sheet = workbook.active

        for idx, row in enumerate(
            sheet.iter_rows(min_row=2, values_only=True), start=2
        ):
            first_name, last_name, email, position = row

            if not (first_name and last_name and email):
                self.errors.append(
                    {'row': idx, ERROR: 'Required fields are missing.'},
                )
                continue

            if '@' not in email:
                self.errors.append(
                    {'row': idx, ERROR: f'Incorrect email: {email}'},
                )
                continue

            if Worker.objects.filter(email=email).exists():
                self.errors.append(
                    {'row': idx, ERROR: f'Email already exists: {email}'},
                )
                continue

            Worker.objects.create(
                first_name=first_name.strip(),
                last_name=last_name.strip(),
                email=email.strip(),
                position=position or 'other',
            )
            self.created_count += 1

        return {'created': self.created_count, 'errors': self.errors}
