from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max 
from datetime import datetime, timedelta

# Create your models here.

class Senhorio(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    grupo = models.CharField(max_length=255, default='senhorio', null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    idade =  models.PositiveIntegerField(null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    profile_pic = models.ImageField(default='profile1.png',null=True, blank=True)
    data_created = models.DateTimeField(auto_now_add=True, null=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Propriedade(models.Model):
    orientacao_solar = (
        ('Norte', 'Norte'),
        ('Sul', 'Sul'),
        ('Este', 'Este'),
        ('Oeste', 'Oeste'),
    )

    faixa_etaria = (
        ('18-24', '18-24'),
        ('25-29', '25-29'),
        ('30+', '30+'),
        ('Qualquer','Qualquer')
    )

    genero = (
        ('Masculino','Masculino'),
        ('Feminino','Feminino'),
        ('Qualquer','Qualquer'),
    )

    senhorio = models.ForeignKey(Senhorio, null=True, on_delete=models.CASCADE, blank=True)
    disponivel = models.BooleanField(default=True)
    titulo = models.CharField(max_length=255, null=True, blank=True)
    data_created = models.DateTimeField(auto_now_add=True)
    preco = models.DecimalField(decimal_places=0, max_digits=65, null=True)
    preco_semestral = models.DecimalField(decimal_places=0, max_digits=65, null=True, blank=True)
    preco_anual = models.DecimalField(decimal_places=0, max_digits=65, null=True, blank=True)
    local = models.TextField(null=True, blank=True)
    numero_quartos = models.PositiveIntegerField(null=True, blank=True)
    numero_inquilinos = models.PositiveIntegerField(null=True, blank=True, default=0)
    area = models.CharField(max_length=255, null=True, blank=True)
    orientacao_solar = models.CharField(max_length=255, choices=orientacao_solar, null=True, blank=True)
    internet = models.BooleanField(null=True)
    pets = models.BooleanField(null=True)
    limpeza = models.BooleanField(null=True)
    fumador = models.BooleanField(null=True)
    faixa_etaria = models.CharField(max_length=255, choices=faixa_etaria, null=True, blank=True)
    genero = models.CharField(max_length=255, choices=genero, null=True, blank=True)
    profile_pic = models.ImageField(default='prop1.jpg',null=True, blank=True)
    Bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.titulo

class Inquilino(models.Model):
    genero = (
        ('Masculino','Masculino'),
        ('Feminino','Feminino'),
    )

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, blank=True)
    grupo = models.CharField(max_length=255, default='inquilino', null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    propriedade = models.ForeignKey(Propriedade, null=True, on_delete=models.CASCADE, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    idade =  models.PositiveIntegerField(null=True, blank=True)
    genero = models.CharField(max_length=255, choices=genero, null=True, blank=True)
    profile_pic = models.ImageField(default='profile1.png',null=True, blank=True)
    data_created = models.DateTimeField(auto_now_add=True, null=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.__str__()

class Oferta(models.Model):
    STATUS = (
        ('Em espera', 'Em espera'),
        ('Rejeitada', 'Rejeitada'),
        ('Aceitada', 'Aceitada'),
    )
    PERIODO = (
        ('Mensal', 'Mensal'),
        ('Semestral', 'Semestral'),
        ('Anual', 'Anual'),
    )
    inquilino = models.ForeignKey(Inquilino, null=True, on_delete=models.CASCADE)
    senhorio = models.ForeignKey(Senhorio, null=True, on_delete=models.CASCADE)
    propriedade = models.ForeignKey(Propriedade, null=True, on_delete=models.CASCADE)
    data_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=STATUS, default='Em espera')
    periodo = models.CharField(max_length=255, choices=PERIODO, default='Mensal')
    quantidade = models.PositiveIntegerField()

class Contrato(models.Model):
    PERIODO = (
        ('Mensal', 'Mensal'),
        ('Semestral', 'Semestral'),
        ('Anual', 'Anual'),
    )
    inquilino = models.ForeignKey(Inquilino, null=True, on_delete=models.CASCADE)
    senhorio = models.ForeignKey(Senhorio, null=True, on_delete=models.CASCADE)
    propriedade = models.ForeignKey(Propriedade, null=True, on_delete=models.CASCADE)
    data_created = models.DateTimeField(auto_now_add=True)
    #fim_contrato_mes = models.DateTimeField(default=datetime.now()+timedelta(days=30))
    #fim_contrato_semestre = models.DateTimeField(default=datetime.now()+timedelta(days=182))
    #fim_contrato_ano = models.DateTimeField(default=datetime.now()+timedelta(days=365))
    duracao = models.DateTimeField(null=True)
    periodo = models.CharField(max_length=255, choices=PERIODO)
    quantidade = models.PositiveIntegerField(null=True)
    expirou = models.BooleanField(default=False)

class Message(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
	recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
	body = models.TextField(max_length=1000, blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)
	is_read = models.BooleanField(default=False)

	def send_message(from_user, to_user, body):
		sender_message = Message(
			user=from_user,
			sender=from_user,
			recipient=to_user,
			body=body,
			is_read=True)
		sender_message.save()

		recipient_message = Message(
			user=to_user,
			sender=from_user,
			body=body,
			recipient=from_user,)
		recipient_message.save()
		return sender_message

	def get_messages(user):
		messages = Message.objects.filter(user=user).values('recipient').annotate(last=Max('date')).order_by('-last')
		users = []
		for message in messages:
			users.append({
				'user': User.objects.get(pk=message['recipient']),
				'last': message['last'],
				'unread': Message.objects.filter(user=user, recipient__pk=message['recipient'], is_read=False).count()
				})
		return users

RATE_CHOICES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
]

class Review(models.Model):
    propriedade = models.ForeignKey(Propriedade, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
    likes = models.PositiveIntegerField(default=0)
    unlikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '%s - %s' % (self.propriedade.titulo, self.user)


class ReviewUser(models.Model):
    avaliadoI = models.ForeignKey(Inquilino, on_delete=models.CASCADE, null=True, blank=True)
    avaliadoS = models.ForeignKey(Senhorio, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
    likes = models.PositiveIntegerField(default=0)
    unlikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '%s' % (self.user)