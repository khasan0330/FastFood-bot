# Generated by Django 4.2.1 on 2023-06-05 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Сумма продуктов')),
                ('total_products', models.IntegerField(null=True, verbose_name='Количество продуктов')),
            ],
            options={
                'verbose_name': 'Корзинка',
                'verbose_name_plural': 'Корзинки',
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=150, unique=True, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=150, verbose_name='Имя пользователя')),
                ('user_telegram', models.BigIntegerField(unique=True, verbose_name='Телеграм ID')),
                ('user_phone', models.CharField(blank=True, max_length=150, null=True, verbose_name='Контактный номер')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=150, unique=True, verbose_name='Наименования')),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость')),
                ('product_info', models.TextField(default='Описания продукта...', verbose_name='Описания')),
                ('product_image', models.ImageField(upload_to='photos/', verbose_name='Изображения')),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_admin.categories', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Finally_carts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=150)),
                ('product_quantity', models.IntegerField()),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_admin.carts')),
            ],
            options={
                'verbose_name': 'Касса',
                'verbose_name_plural': 'Кассы',
            },
        ),
        migrations.AddField(
            model_name='carts',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_admin.users', verbose_name='Пользователь'),
        ),
        migrations.AddConstraint(
            model_name='finally_carts',
            constraint=models.UniqueConstraint(fields=('cart_id', 'product_name'), name='unique_cart_product'),
        ),
    ]
