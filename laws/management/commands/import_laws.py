import json
from django.core.management.base import BaseCommand
from laws.models import Law, LawVersion


class Command(BaseCommand):
    help = "Import laws from JSON file"

    def handle(self, *args, **kwargs):
        with open("laws_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            law = Law.objects.create(
                title=item["title"],
                category=item["category"],
                law_number=item.get("law_number"),
                approved_date=item.get("approved_date"),
                effective_date=item.get("effective_date"),
                issued_by=item.get("issued_by"),
                status=item.get("status"),
                summary=item.get("summary"),
            )

            for version in item.get("versions", []):
                LawVersion.objects.create(
                    law=law,
                    version_number=version["version_number"],
                    effective_date=version["effective_date"],
                    content=version["content"],
                )

        self.stdout.write(self.style.SUCCESS("✅ Laws imported successfully"))