# Generated by Django 3.0.14 on 2021-06-18 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("address", "0003_auto_20200830_1851"),
    ]

    operations = [
        migrations.CreateModel(
            name="District",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=63)),
            ],
            options={
                "verbose_name_plural": "Districts",
                "ordering": ("state", "name"),
            },
        ),
        migrations.CreateModel(
            name="Sublocality",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=63)),
            ],
            options={
                "verbose_name_plural": "Sublocalities",
                "ordering": ("locality", "name"),
            },
        ),
        migrations.AlterModelOptions(
            name="state",
            options={"ordering": ("country", "name"), "verbose_name_plural": "States"},
        ),
        migrations.AlterUniqueTogether(
            name="locality",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="state",
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name="locality",
            constraint=models.UniqueConstraint(
                fields=("name", "postal_code", "state"), name="locality"
            ),
        ),
        migrations.AddConstraint(
            model_name="state",
            constraint=models.UniqueConstraint(
                fields=("name", "country"), name="state"
            ),
        ),
        migrations.AddField(
            model_name="sublocality",
            name="locality",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="address.Locality"
            ),
        ),
        migrations.AddField(
            model_name="district",
            name="state",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="districts",
                to="address.State",
            ),
        ),
        migrations.AddField(
            model_name="address",
            name="sublocality",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="addresses",
                to="address.Sublocality",
            ),
        ),
        migrations.AddField(
            model_name="locality",
            name="district",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="localities",
                to="address.District",
            ),
        ),
        migrations.AddConstraint(
            model_name="sublocality",
            constraint=models.UniqueConstraint(
                fields=("locality", "name"), name="sublocality"
            ),
        ),
        migrations.AddConstraint(
            model_name="district",
            constraint=models.UniqueConstraint(
                fields=("state", "name"), name="district"
            ),
        ),
    ]
