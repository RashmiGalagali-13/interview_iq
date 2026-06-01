from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(
                choices=[('jobseeker', 'Job Seeker'), ('company', 'Company'), ('admin', 'Admin')],
                default='jobseeker',
                max_length=20,
            ),
        ),
    ]
