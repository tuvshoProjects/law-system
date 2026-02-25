from django.db import models
from django.contrib.auth.models import User


# =============================
# 🏛 LAW MODEL
# =============================
class Law(models.Model):

    STATUS_CHOICES = [
        ("active", "Хүчинтэй"),
        ("inactive", "Хүчингүй"),
        ("draft", "Төсөл"),
    ]

    title = models.CharField(max_length=300)
    category = models.CharField(max_length=200)

    law_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Хуулийн дугаар"
    )

    approved_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Батлагдсан огноо"
    )

    effective_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Хүчин төгөлдөр болсон огноо"
    )

    issued_by = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Баталсан байгууллага"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    summary = models.TextField(
        blank=True,
        null=True,
        verbose_name="Товч тайлбар"
    )

    pdf_file = models.FileField(
        upload_to="law_pdfs/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# =============================
# 📜 LAW VERSION
# =============================
class LawVersion(models.Model):
    law = models.ForeignKey(
        Law,
        on_delete=models.CASCADE,
        related_name="versions"
    )

    version_number = models.IntegerField(default=1)
    content = models.TextField()
    effective_date = models.DateField()

    def __str__(self):
        return f"{self.law.title} - v{self.version_number}"


# =============================
# ⭐ BOOKMARK
# =============================
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    law = models.ForeignKey(Law, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "law")

    def __str__(self):
        return f"{self.user.username} - {self.law.title}"


# =============================
# 📊 ACTIVITY LOG
# =============================
class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"