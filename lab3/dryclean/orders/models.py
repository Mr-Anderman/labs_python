from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User


class Branch(models.Model):
    """Филиал химчистки."""
    name = models.CharField('Название', max_length=100)
    address = models.CharField('Адрес', max_length=200)

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    def __str__(self):
        return self.name


class Client(models.Model):
    last_name = models.CharField('Фамилия', max_length=50)
    first_name = models.CharField('Имя', max_length=50)
    patronymic = models.CharField('Отчество', max_length=50, blank=True)
    address = models.CharField('Адрес', max_length=200)
    phone = models.CharField('Телефон', max_length=20)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return '%s %s %s' % (self.last_name, self.first_name, self.patronymic)

    def visits(self):
        return self.contract_set.count()

    def is_regular(self):
        return self.visits() >= 3
    is_regular.boolean = True
    is_regular.short_description = 'Постоянный'


class Service(models.Model):
    TYPES = [
        ('dry', 'Химчистка'),
        ('stain', 'Выведение пятен'),
        ('aqua', 'Аквачистка'),
        ('leather', 'Кожа и мех'),
    ]
    name = models.CharField('Название', max_length=100)
    type = models.CharField('Тип', max_length=10, choices=TYPES)
    base_price = models.DecimalField('Базовая цена, руб.', max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Вид услуги'
        verbose_name_plural = 'Виды услуг'

    def __str__(self):
        return '%s (%s руб.)' % (self.name, self.base_price)


class Contract(models.Model):
    number = models.CharField('Номер договора', max_length=20, unique=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 verbose_name='Приёмщик')                    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Филиал')
    comment = models.TextField('Описание работ', blank=True)
    date_received = models.DateField('Дата приёма', auto_now_add=True)

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'
        ordering = ['-id']

    def __str__(self):
        return '№%s: %s' % (self.number, self.client)

    def has_discount(self):
        previous = Contract.objects.filter(client=self.client, id__lt=self.id).count()
        return previous >= 2
    has_discount.boolean = True
    has_discount.short_description = 'Скидка 3 %'

    def total(self):
        return sum(item.price() for item in self.item_set.all())
    total.short_description = 'Сумма, руб.'

    def get_excerpt(self):
        return self.comment[:140] + "..." if len(self.comment) > 140 else self.comment
    get_excerpt.short_description = 'Описание'


class Item(models.Model):
    COMPLEXITY = [
        ('1.0', 'Обычная'),
        ('1.2', 'Повышенная (+20 %)'),
        ('1.5', 'Высокая (+50 %)'),
    ]
    URGENT_RATE = Decimal('1.5')    # надбавка за срочность +50 %
    DISCOUNT = Decimal('0.97')      # скидка постоянного клиента 3 %

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name='Договор')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, verbose_name='Услуга')
    description = models.CharField('Вещь', max_length=200)
    complexity = models.CharField('Сложность', max_length=3, choices=COMPLEXITY, default='1.0')
    urgent = models.BooleanField('Срочно', default=False)
    date_returned = models.DateField('Дата возврата', null=True, blank=True)

    class Meta:
        verbose_name = 'Вещь'
        verbose_name_plural = 'Вещи'

    def __str__(self):
        return self.description

    def price(self):
        value = self.service.base_price * Decimal(self.complexity)
        if self.urgent:
            value *= self.URGENT_RATE
        if self.contract.has_discount():
            value *= self.DISCOUNT
        return value.quantize(Decimal('0.01'))
    price.short_description = 'Цена, руб.'
