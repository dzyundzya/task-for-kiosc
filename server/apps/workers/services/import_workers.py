from __future__ import annotations

from typing import Any

import openpyxl
from django.core.files.uploadedfile import UploadedFile

from server.apps.workers.models import Worker

ERROR = 'error'


class WorkerImportService:
    """Service for importing workers from Excel."""

    def __init__(self) -> None:
        """Initialize the service with counters and error storage."""
        self.created_count = 0
        self.errors: list[dict[str, Any]] = []

    def import_from_excel(self, excel_file: UploadedFile) -> dict[str, Any]:  # noqa: WPS210, WPS231
        """Import worker data from an uploaded Excel file."""
        try:
            workbook = openpyxl.load_workbook(excel_file)
        except Exception:
            return {
                'created': 0,
                'errors': [{ERROR: 'Excel file cannot be read.'}],
            }

        sheet = workbook.active
        existing_emails = set(Worker.objects.values_list('email', flat=True))

        workers_to_create = []

        for idx, row in enumerate(
            sheet.iter_rows(min_row=2, values_only=True), start=2
        ):
            first_name, last_name, email, position = row

            if not (first_name and last_name and email):
                self.errors.append({
                    'row': idx,
                    ERROR: 'Required fields are missing.',
                })
                continue

            if '@' not in email:
                self.errors.append({
                    'row': idx,
                    ERROR: f'Incorrect email: {email}',
                })
                continue

            if email in existing_emails:
                self.errors.append({
                    'row': idx,
                    ERROR: f'Email already exists: {email}',
                })
                continue

            workers_to_create.append(
                Worker(
                    first_name=first_name.strip(),
                    last_name=last_name.strip(),
                    email=email.strip(),
                    position=position or 'other',
                )
            )
            existing_emails.add(email)

        Worker.objects.bulk_create(workers_to_create)
        self.created_count = len(workers_to_create)

        return {'created': self.created_count, 'errors': self.errors}
