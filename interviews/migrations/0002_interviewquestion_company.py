from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('interviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interviewquestion',
            name='company',
            field=models.ForeignKey(
                blank=True,
                help_text='Leave blank for global questions',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='interview_questions',
                to='accounts.companyprofile',
            ),
        ),
    ]
