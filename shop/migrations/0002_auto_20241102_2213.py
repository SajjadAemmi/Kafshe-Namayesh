from django.db import migrations


def create_shoes(apps, schema_editor):
    Shoe = apps.get_model('shop', 'Shoe')

    shoes_data = [
        {
            "name": "کفش ۱",
            "details": "کد۲۳۰\n. تولید تبریز\n. ۱۰۰٪طبی\n. جنس رویه چرم طبیعی\n. جنس آستر و کفی چرم بزی\n.زیره پی یو و مقاوم\n. کفی طبی",
            "price": 1250.00,
        },
        {
            "name": "کفش ۲",
            "details": "مردانه کلاسیک\n.آستر و کفی و رویه تمام چرم ترکمان درجه یک\n.برند دکتر اشمیت\n.زیره لاستیک",
            "price": 1980.00,
        },
        {
            "name": "کفش ۳",
            "details": "مردانه پرفکت دکتر شول\n.تولید تهران و برند کوروش\n.آستر و کفی چرم بزی\n.رویه چرم گاوی\n.زیره تی پی یو و استحکام بالا",
            "price": 1280.00,
        },
    ]

    for shoe_data in shoes_data:
        Shoe.objects.create(**shoe_data)


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_shoes),
    ]
