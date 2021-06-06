from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse

from django.forms import inlineformset_factory

from django.views import View

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

from django.urls import reverse

from django.utils import timezone

from django.template import loader, RequestContext
from django.template.loader import get_template

from django.db.models import Q
from django.db.models.signals import post_save

from django.core.paginator import Paginator
from django.http import Http404
from datetime import datetime, timedelta

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics 
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.authtoken.models import Token
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema

from django.conf import settings


from django.dispatch import receiver

from io import BytesIO

from xhtml2pdf import pisa 
import csv
import xlwt

from .filters import PropriedadeFilter
from .models import *
from .forms import *
from .decorators import unauthenticated_user, allowed_users, admin_only
from .serializers import *

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
#----------------------------------API-----------------------------------------------------------------------------------------------------#   

#@receiver(post_save, sender=settings.AUTH_USER_MODEL)
#def create_auth_token(sender, instance=None, created=False, **kwargs):
#    if created:
#        Token.objects.create(user=instance)

@extend_schema(
            parameters=[
                SenhorioSerializer,
                OpenApiParameter(
                    name='id',
                    description='Senhorio user',
                    type=int
                    ),
                OpenApiParameter(
                    name='bio',
                    description='Biography of user',
                    type=str
                ),
                OpenApiParameter(
                    name='grupo',
                    description='Group of which the user belongs to',
                    type=str
                ),
                OpenApiParameter(
                    name='email',
                    description='Senhorio user email',
                    type=str
                ),
                OpenApiParameter(
                    name='name',
                    description='User name',
                    type=str
                ),
                OpenApiParameter(
                    name='idade',
                    description='Age',
                    type=int
                )
            ],
            
            
    )
class SenhorioList(generics.ListCreateAPIView):
    '''
    List all Landlords or create a new landlord
    get: Returns a list of all landlords
    post: Creates a new landlord
    '''
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

    queryset = Senhorio.objects.all()
    serializer_class = SenhorioSerializer

@extend_schema(
            parameters=[
                SenhorioSerializer,
                OpenApiParameter(
                    name='id',
                    description='User',
                    type=int
                    ),
            ],
            
            
    )
class SenhorioDetail(APIView):
    '''
    Retrieve, updata or delete an instance of senhorio
    '''

    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request, pk, format=None):
        '''
        Returns a user with given id
        '''
        try:
            senhorio = Senhorio.objects.get(pk=pk)
            serializer = SenhorioSerializer(senhorio)
            return Response(serializer.data)
        except Senhorio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  
    
    def put(self, request, pk, format=None):
        '''
        Update a landlord information
        '''
        try:
            senhorio = Senhorio.objects.get(pk=pk)
            serial = SenhorioSerializer(senhorio, data=request.data)
            if serial.is_valid():
                serial.save()
                return Response(serial.data)
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except Senhorio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk, format=None):
        '''
        Deletes a landlord
        '''
        try:
            senhorio = Senhorio.objects.get(pk=pk)
            senhorio.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Senhorio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@extend_schema(
            parameters=[
                InquilinoSerializer,
                OpenApiParameter(
                    name='id',
                    description='User',
                    type=int
                    ),
                OpenApiParameter(
                    name='bio',
                    description='Biography of user',
                    type=str
                ),
                OpenApiParameter(
                    name='grupo',
                    description='Group of which the user belongs to',
                    type=str
                ),
                OpenApiParameter(
                    name='email',
                    description='User email',
                    type=str
                ),
                OpenApiParameter(
                    name='name',
                    description='User name',
                    type=str
                ),

            ],
            
            
    )
class InquilinoList(generics.ListCreateAPIView):
    '''
    List all tenants or create a new tenant
    get: Return a list of all tenants
    post: Create a new tenant
    '''
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = Inquilino.objects.all()
    serializer_class = InquilinoSerializer

@extend_schema(
    parameters=[
            InquilinoSerializer,
            OpenApiParameter(
                name='id',
                description='An integer unique to senhorio user',
                type=int
                ),

    ],
)
class InquilinoDetail(APIView):
    '''
    Retrieve, update or delete a tenant instance
    '''
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk, format=None):
        '''
        Return a tenant
        '''
        try:
            inquilino = Inquilino.objects.get(pk=pk)
            inquilino = InquilinoSerializer(inquilino)
            return Response(inquilino.data)
        except Inquilino.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    
    def put(self, request, pk, format=None):
        '''
        Update a tenant
        '''
        try:
            inquilino = Inquilino.objects.get(pk=pk)
            serial = SenhorioSerializer(inquilino, data=request.data)
            if serial.is_valid():
                serial.save()
                return Response(serial.data)
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except Inquilino.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

    def delete(self, request, pk, format=None):
        '''
        Delete a tenant
        '''
        try:        
            inquilino = Inquilino.objects.get(pk=pk)
            inquilino.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Inquilino.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    parameters=[
        PropriedadeSerializer,
        OpenApiParameter(
            name='titulo',
            description='Property Name',
            type=str
        ),
        OpenApiParameter(
            name='preco',
            description='Property price',
            type=str
        ),
        OpenApiParameter(
            name='local',
            description='Property address/city',
            type=str
        ),
        OpenApiParameter(
            name='numero_quartos',
            description='Amount of rooms in property',
            type=int
        ),
        OpenApiParameter(
            name='numero_inquilinos',
            description='Number of tenants allowed',
            type=int
        ),
        OpenApiParameter(
            name='area',
            description='Total area of property',
            type=str
        ),
        OpenApiParameter(
            name='internet',
            description='Indicates whether it provides internet or not. True if there is internet, False otherwise',
            type=bool
        ),
        OpenApiParameter(
            name='pets',
            description='Indicates whether pets are allowed or not.',
            type=bool
        ),
        OpenApiParameter(
            name='limpeza',
            description='Provides cleaner or not.',
            type=bool
        ),
        OpenApiParameter(
            name='fumador',
            description='Whether it allows smokers inside or not',
            type=bool
        ),
        OpenApiParameter(
            name='Bio',
            description='Description of property',
            type=str
        ),
        OpenApiParameter(
            name='senhorio',
            description='Property owners',
            type=int
        ),
    ],
)
class PropriedadeList(generics.ListCreateAPIView):
    '''
    List all properties or create new ones
    get: Returns a list of all properties
    post: Creates a new property
    '''
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

    queryset = Propriedade.objects.all()
    serializer_class = PropriedadeSerializer

@extend_schema(
    parameters=[
        PropriedadeSerializer,
        OpenApiParameter(
            name='titulo',
            description='Property Name',
            type=str
        ),
        OpenApiParameter(
            name='preco',
            description='Property price',
            type=str
        ),
        OpenApiParameter(
            name='local',
            description='Property address/city',
            type=str
        ),
        OpenApiParameter(
            name='numero_quartos',
            description='Amount of rooms in property',
            type=int
        ),
        OpenApiParameter(
            name='numero_inquilinos',
            description='Number of tenants allowed',
            type=int
        ),
        OpenApiParameter(
            name='area',
            description='Total area of property',
            type=str
        ),
        OpenApiParameter(
            name='internet',
            description='Indicates whether it provides internet or not. True if there is internet, False otherwise',
            type=bool
        ),
        OpenApiParameter(
            name='pets',
            description='Indicates whether pets are allowed or not.',
            type=bool
        ),
        OpenApiParameter(
            name='limpeza',
            description='Provides cleaner or not.',
            type=bool
        ),
        OpenApiParameter(
            name='fumador',
            description='Whether it allows smokers inside or not',
            type=bool
        ),
        OpenApiParameter(
            name='Bio',
            description='Description of property',
            type=str
        ),
        OpenApiParameter(
            name='senhorio',
            description='Property owners',
            type=int
        ),
    ]
)
class PropriedadeDetail(APIView):
    '''
    Retrieve, update or delete a property instance
    '''
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk, format=None):
        '''
        Return a property
        '''
        try:
            prop = PropriedadeDetail.objects.get(pk=pk)
            prop = PropriedadeSerializer(prop)
            return Response(prop.data)
        except Propriedade.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

    def put(self, request, pk, format=None):
        '''
        Update a property
        '''
        try:
            prop = PropriedadeDetail.objects.get(pk=pk)
            serial = PropriedadeSerializer(prop, data=request.data)
            if serial.is_valid():
                serial.save()
                return Response(serial.data)
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except Propriedade.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

    def delete(self, request, pk, format=None):
        '''
        Delete a property
        '''
        try:
            prop = PropriedadeDetail.objects.get(pk=pk)
            prop.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Propriedade.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    parameters=[
        OfferSerializer,
        OpenApiParameter(
            name='inquilino',
            description='Potential tenant',
            type=int
        ),
        OpenApiParameter(
                name='senhorio',
                description='Property owner',
                type=int
        ),
        OpenApiParameter(
                name='propriedade',
                description='Property',
                type=int
        ),
        OpenApiParameter(
                name='data_created',
                description='Date the offer was made',

        ),
        OpenApiParameter(
                name='status',
                description='Indicates whether the offer is on waiting for an answer, was rejected or accepted',
                type=str
        ),
        OpenApiParameter(
                name='periodo',
                description='Indicates the period of time of the offer',
                type=str
        ),
        OpenApiParameter(
                name='quantidade',
                description='Cost of said offer',
                type=int
        )
    ],
    
)
class OfferList(generics.ListCreateAPIView):
    '''
    List all offers or create a new one
    get: Returns a list of all available offers
    post: Creates a new offer
    '''
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = Oferta.objects.all()
    serializer_class = OfferSerializer

class OfferDetail(APIView):
    '''
    Retrieve, update or delete an offer instance
    '''
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]    
    permission_classes = [permissions.IsAdminUser]
   
    def get(self, request, pk, format=None):
        '''
        Return an existing offer
        ''' 
        try:
            offer = OfferDetail.objects.get(pk=pk)
            offer = OfferSerializer(offer)
            return Response(offer.data)
        except Oferta.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        '''
        Update an offer
        '''
        try:
            offer = OfferDetail.objects.get(pk=pk)
            serial = OfferSerializer(offer, data=request.data)
            if serial.is_valid():
                serial.save()
                return Response(serial.data)
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except Oferta.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

    def delete(self, request, pk, format=None):
        '''
        Delete an offer
        '''
        try:
            offer = OfferDetail.objects.get(pk=pk)
            offer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Oferta.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    parameters=[
        ContractSerializer,
        OpenApiParameter(
                name='inquilino',
                description='Tenant/s',
                type=int
        ),
        OpenApiParameter(
                name='senhorio',
                description='Property owner',
                type=int
        ),
        OpenApiParameter(
                name='propriedade',
                description='Property',
                type=int
        ),
        OpenApiParameter(
                name='data_created',
                description='Date the contract was made',

        ),
        OpenApiParameter(
                name='duracao',
                description='Time until which the contract is valid',
                type=str
        ),
        OpenApiParameter(
                name='periodo',
                description='Indicates the period of time of the contract',
                type=str
        ),
        OpenApiParameter(
                name='quantidade',
                description='Cost of said property agreed on contract',
                type=int
        ),
        OpenApiParameter(
            name='expirou',
            description='Indicates whether the contract has expired or not',
            type=bool
        ),
    ],
    
)
class ContractList(generics.ListCreateAPIView):
    '''
    List all contracts or create a new one
    get: Returns a list of all contracts
    post: Creates a new contract
    '''
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = Contrato.objects.all()
    serializer_class = ContractSerializer

class ContractDetail(APIView):
    '''
    Retrieve, update or delete a contract instance
    '''
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]

    def get(self, request, pk, format=None):
        '''
        Returns a contract
        '''
        try:
            contract = ContractDetail.objects.get(pk=pk)
            contract = ContractSerializer(contract)
            return Response(contract.data)
        except Contrato.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk, format=None):
        '''
        Update a contract content
        '''
        try:
            contract = ContractDetail.objects.get(pk=pk)
            serial = ContractSerializer(contract, data=request.data)
            if serial.is_valid():
                serial.save()
                return Response(serial.data)
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except Contrato.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk, format=None):
        '''
        Delete a contract
        '''
        try:
            contract = ContractDetail.objects.get(pk=pk)
            contract.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Contrato.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    parameters=[
        MessageSerializer,
        OpenApiParameter(
            name='user',
            description='User',
            type=int
        ),
        OpenApiParameter(
            name='sender',
            description='Message sender',
            type=int
        ),
        OpenApiParameter(
            name='recipient',
            description='Message receiver',
            type=int
        ),
        OpenApiParameter(
            name='body',
            description='Content of message',
            type=str
        ),
        OpenApiParameter(
            name='date',
            description='Date on which message was sent',
            type=str
        ),
        OpenApiParameter(
            name='is_read',
            description='Indicates if the message has been read',
            type=bool
        )
    ],
)
class MessageList(generics.ListCreateAPIView):
    '''
    List all messages or create a new one
    get: Returns a list of all messages
    post: Creates a new message
    '''
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

@extend_schema(
    parameters=[
        MessageSerializer,
        OpenApiParameter(
            name='user',
            description='Primary key of self',
            type=int
        ),
        OpenApiParameter(
            name='sender',
            description='Primary key of message sender',
            type=int
        ),
        OpenApiParameter(
            name='recipient',
            description='Primary key of message receiver',
            type=int
        ),
    ],
)
class MessageDetail(APIView):
    '''
    Retrieve or delete a message instance
    '''
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]


    def get(self, request, pk, format=None):
        '''
        Retuns a message
        '''
        try:
            message = Message.objects.get(pk=pk)
            message = MessageSerializer(message)
            return Response(message.data)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk, format=None):
        try:
            message = Message.objects.get(pk=pk)
            serial = MessageSerializer(message, data=request.data)
            if serial.is_valid():
                serial.save()
                return Response(serial.data)
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

    def delete(self, request, pk, format=None):
        '''
        Deletes a message
        '''
        try:
            message = Message.objects.get(pk=pk)
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    parameters=[
        ReviewSerializer,
        OpenApiParameter(
            name='propriedade',
            description='Property',
            type=int
        ),
        OpenApiParameter(
            name='user',
            description='User',
            type=int
        ),
        OpenApiParameter(
            name='text',
            description='Review content',
            type=str
        ),
        OpenApiParameter(
            name='date',
            description='Review date',
            type=str
        ),
        OpenApiParameter(
            name='rate',
            description='Rate of review from 0 to 10',
            type=int
        ),
        OpenApiParameter(
            name='likes',
            description='Amount of likes the property received',
            type=int
        ),
        OpenApiParameter(
            name='unlikes',
            description='Amount of dislikes the property received',
            type=int
        )
    ],
)
class ReviewList(generics.ListCreateAPIView):
    '''
    List all reviews or create a new one
    get: Returns a list of all reviews
    post: Creates a new review
    '''
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetail(APIView):
    '''
    Retrieve, update/edit or delete a review instance
    '''
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk, format=None):
        '''
        Returns a review
        '''
        try:
            rev = Review.objects.get(pk=pk)
            rev = ReviewSerializer(rev)
            return Response(rev.data)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        '''
        Updates a review
        '''
        try:
            rev = self.get_object(pk)
            serial = ReviewSerializer(rev, data=request.data)
            if serial.is_valid():
                serial.save()
                return Response(serial.data)
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk, format=None):
        '''
        Deletes a review
        '''
        try:
            rev = self.get_object(pk)
            rev.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    parameters=[
        ReviewUserSerializer,
        OpenApiParameter(
            name='avaliadoI',
            description='Tenant',
            type=int
        ),
        OpenApiParameter(
            name='avaliadoS',
            description='Landlord',
            type=int
        ),
        OpenApiParameter(
            name='user',
            description='User',
            type=int
        ),
        OpenApiParameter(
            name='text',
            description='Content of review made',
            type=str
        ),
        OpenApiParameter(
            name='date',
            description='Date of review',
            type=str
        ),
        OpenApiParameter(
            name='rate',
            description='Rating of review, from 0 to 10',
            type=int
        ),
        OpenApiParameter(
            name='likes',
            description='Amount of likes given to user',
            type=int
        ),
        OpenApiParameter(
            name='unlikes',
            description='Amount of dislikes given to user',
            type=int
        )
    ],
)
class ReviewUserList(generics.ListCreateAPIView):
    '''
    List the user reviews or create one
    get: Return a list all the user reviews
    post: Create a new user review
    '''
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = ReviewUser.objects.all()
    serializer_class = ReviewUserSerializer

class ReviewUserDetail(APIView):
    '''
    Retrieve, update/edit or delete a user review instance
    '''
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk, format=None):
        '''
        Return a user review
        '''
        try:
            revUser = ReviewUser.objects.get(pk=pk)
            revUser = ReviewUserSerializer(revUser)
            return Response(revUser.data)
        except ReviewUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
    def put(self, request, pk, format=None):
        '''
        Update a user review
        '''
        try:
            revUser = ReviewUser.objects.get(pk=pk)
            serial = ReviewUserSerializer(revUser, data=request.data)
            if serial.is_valid():
                serial.save()
                return Response(serial.data)
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except ReviewUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk, format=None):
        '''
        Delete a user review
        '''
        try:
            revUser = ReviewUser.objects.get(pk=pk)
            revUser.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReviewUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

#-----------------------------------ADMIN---------------------------------------------------------------------------------------------------#

def export_inquilinos(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="inquilinos.xls"'

    wb = xlwt.Workbook(encoding='urf-8')
    ws = wb.add_sheet('Inquilinos')
    row_num = 0
    font_style=xlwt.XFStyle()
    font_style.font.bold = True

    colums = ['id','Nome','Género','Idade','Email']
    
    for col_num in range(len(colums)):
        ws.write(row_num, col_num, colums[col_num], font_style)

    font_style=xlwt.XFStyle()

    rows=Inquilino.objects.all().values_list('id','name','genero','idade','email')
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response


def import_inquilinos(request):
    #response = HttpResponse(content_type='application/ms-excel')
    #response['Content-Disposition'] = 'attachment'
    
    if request.method == 'POST':
        f = request.FILES['myfile']
        if f.name.endswith('xls'):
                         # Start parsing excel spreadsheet upload
            wb = excelrd.open_workbook(filename=f.name,file_contents=f.read())
            table = wb.sheets()[0]
            rows = table.nrows
            #try:
                    #with transaction.atomic (): # database transaction transaction control
            for i in range(0,rows):
                            #rowValues = table.row_values(i)
                            #user = table.row_values(i)[0]
                            #group = Group.objects.get(name='inquilino')
                            #user.groups.add(group)
                            inquilino = Inquilino.objects.get(id=table.row_values(i)[0])
                            inquilino.name = table.row_values(i)[1]
                            inquilino.genero = table.row_values(i)[2]
                            inquilino.idade = table.row_values(i)[3]
                            inquilino.email = table.row_values(i)[4]
                            inquilino.save()
                            #inquilino.update(name=table.row_values(i)[1],
                            #                         genero=table.row_values(i)[2],
                            #                         idade=table.row_values(i)[3],
                            #                         email=table.row_values(i)[4],
                            #                        )
            #except:
             #           logger.error ( 'parse excel file or data insertion error')
            #return HttpResponse('importação com successo')
            return redirect('/admin')
        else:
            logger.error ( 'upload file type error!')
            return HttpResponse('Importação falhada')



def export_senhorios(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="senhorios.xls"'

    wb = xlwt.Workbook(encoding='urf-8')
    ws = wb.add_sheet('Senhorios')
    row_num = 0
    font_style=xlwt.XFStyle()
    font_style.font.bold = True

    colums = ['id','Nome','Idade','Email']
    
    for col_num in range(len(colums)):
        ws.write(row_num, col_num, colums[col_num], font_style)

    font_style=xlwt.XFStyle()

    rows=Senhorio.objects.all().values_list('id','name','idade','email')
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response


def import_senhorios(request):
     if request.method == 'POST':
        f = request.FILES['myfile2']
        if f.name.endswith('xls'):
                         # Start parsing excel spreadsheet upload
            wb = excelrd.open_workbook(filename=f.name,file_contents=f.read())
            table = wb.sheets()[0]
            rows = table.nrows
            #try:
            for i in range(0,rows):
                            senhorio = Senhorio.objects.get(id=table.row_values(i)[0])
                            senhorio.name = table.row_values(i)[1]
                            senhorio.idade = table.row_values(i)[2]
                            senhorio.email = table.row_values(i)[3]
                            senhorio.save()
                            #rowValues = table.row_values(i)
                            #group = Group.objects.get(name='senhorio')
                            #user.groups.add(group)
                            #Senhorio.objects.create(name=rowValues[0],idade=rowValues[1],email=rowValues[2])
            #except:
                      #  logger.error ( 'parse excel file or data insertion error')
            #return HttpResponse('importação com successo')
            return redirect('/admin')
        else:
            logger.error ( 'upload file type error!')
            return HttpResponse('Importação falhada')

def export_propriedades(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="propriedades.xls"'

    wb = xlwt.Workbook(encoding='urf-8')
    ws = wb.add_sheet('Propriedades')
    row_num = 0
    font_style=xlwt.XFStyle()
    font_style.font.bold = True

    colums = ['id','Titulo','Senhorio','Local',
    'Preço Mensal','Preço Semestral','Preço Anual',
    'Número de quartos','Número de inquilinos','Area',
    'Orientaçao Solar','Internet','Pets','Limpeza','Fumador',
    'Faixa etária permitida', 'Género permitido']
    
    for col_num in range(len(colums)):
        ws.write(row_num, col_num, colums[col_num], font_style)

    font_style=xlwt.XFStyle()

    rows=Propriedade.objects.all().values_list('id','titulo','senhorio','local','preco','preco_semestral','preco_anual',
        'numero_quartos','numero_inquilinos','area','orientacao_solar',
        'internet','pets','limpeza','fumador','faixa_etaria','genero')
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response


def import_propriedades(request):
     if request.method == 'POST':
        f = request.FILES['myfile3']
        if f.name.endswith('xls'):
                         # Start parsing excel spreadsheet upload
            wb = excelrd.open_workbook(filename=f.name,file_contents=f.read())
            table = wb.sheets()[0]
            rows = table.nrows
            #try:
            for i in range(0,rows):
                            #rowValues = table.row_values(i)
                            prop = Propriedade.objects.get(id=table.row_values(i)[0])
                            prop.titulo=table.row_values(i)[1]
                            senhor = Senhorio.objects.get(id=table.row_values(i)[2])
                            prop.senhorio=senhor
                            prop.local=table.row_values(i)[3]
                            prop.preco=table.row_values(i)[4]
                            prop.preco_semestral=table.row_values(i)[5]
                            prop.preco_anual=table.row_values(i)[6]
                            prop.numero_quartos=table.row_values(i)[7]
                            prop.numero_inquilinos=table.row_values(i)[8]
                            prop.area=table.row_values(i)[9]
                            prop.orientacao_solar=table.row_values(i)[10]
                            prop.internet=table.row_values(i)[11]
                            prop.pets=table.row_values(i)[12]
                            prop.limpeza=table.row_values(i)[13]
                            prop.fumador=table.row_values(i)[14]
                            prop.faixa_etaria=table.row_values(i)[15]
                            prop.genero=table.row_values(i)[16]
                            prop.save()
            #except:
                        #logger.error ( 'parse excel file or data insertion error')
            #return HttpResponse('importação com successo')
            return redirect('/admin')
        else:
            logger.error ( 'upload file type error!')
            return HttpResponse('Importação falhada')

#--------------------------------------------------------------------------------------------------------------------------------------#

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            group = Group.objects.get(name='inquilino')
            user.groups.add(group)
            Inquilino.objects.create(
                user=user,
                email=email,
                name=username,
            )

            messages.success(request, username + ' criado com successo!')

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def registerSPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            group = Group.objects.get(name='senhorio')
            user.groups.add(group)
            Senhorio.objects.create(
                user=user,
                email=email,
                name=username,
            )

            messages.success(request, username + ' criado com successo!')

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/registerS.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username ou passowrd incorretos')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

#-----------------------------------------------------USERS INTERFACE------------------------------------------------------------------------#

@login_required(login_url='login')
@admin_only
def home(request):
    return render(request, 'accounts/dashboard.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['inquilino'])
def accountSettings(request):
    inquilino = request.user.inquilino
    form = InquilinoForm(instance=inquilino)

    if request.method == 'POST':
        form = InquilinoForm(request.POST, request.FILES, instance=inquilino)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['senhorio'])
def accountSettingsSenhorio(request):
    senhorio = request.user.senhorio
    form = SenhorioForm(instance=senhorio)

    if request.method == 'POST':
        form = InquilinoForm(request.POST, request.FILES, instance=senhorio)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'accounts/account_settings_senhorio.html', context)


@login_required(login_url='login')
@allowed_users(['inquilino', 'senhorio'])
def userPage(request):
    l = []
    for g in request.user.groups.all():
        l.append(g.name)
    
    if 'inquilino' in l:
        inquilino = request.user.inquilino
        reviews = ReviewUser.objects.filter(avaliadoI = inquilino)
        return render(request, 'accounts/user.html', {'reviews':reviews})
    if 'senhorio' in l:
        senhorio = request.user.senhorio
        reviews = ReviewUser.objects.filter(avaliadoS = senhorio)
        return render(request, 'accounts/senhorio.html', {'reviews':reviews})
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
@allowed_users(['inquilino', 'senhorio'])
def perfil_user(request, pk, group):
    if group == 'senhorio':
        perfil = Senhorio.objects.get(id=pk)
        reviews = ReviewUser.objects.filter(avaliadoS=perfil)
        if perfil.user == request.user:
            return redirect('home')

        return render(request, 'accounts/perfil_user_senhorio.html', {'perfil':perfil, 'reviews':reviews})

    
    if group == 'inquilino':
        perfil = Inquilino.objects.get(id=pk)
        reviews = ReviewUser.objects.filter(avaliadoI=perfil)  
        if perfil.user == request.user:
            return redirect('home')
        return render(request, 'accounts/perfil_user_inquilino.html', {'perfil':perfil, 'reviews':reviews})

    return redirect('home')


#---------------------------PROPRIEDADES-----------------------------------------------------------------------------------------------------------#


@login_required(login_url='login')
def propriedades(request):
    propriedades = Propriedade.objects.all()

    myFilter = PropriedadeFilter(request.GET, queryset=propriedades)
    propriedades = myFilter.qs

    return render(request, 'accounts/propriedades.html', {'propriedades':propriedades, 'myFilter':myFilter})

@unauthenticated_user
def freeProps(request):
    propriedades = Propriedade.objects.all()
    myFilter = PropriedadeFilter(request.GET, queryset=propriedades)
    propriedades = myFilter.qs

    return render(request, 'accounts/free_propriedades.html', {'propriedades':propriedades, 'myFilter':myFilter})

@login_required(login_url='login')
def detalhes_propriedades(request, pk):
    detalhes_propriedades = Propriedade.objects.get(id=pk)
    reviews = Review.objects.filter(propriedade=detalhes_propriedades)
    
    contratos = Contrato.objects.filter(propriedade=detalhes_propriedades)
    shortest = timezone.now() + timedelta(days=10000)
    for i in contratos:
        if i.duracao < shortest:
            shortest = i.duracao

    return render(request, 'accounts/propriedades_detalhes.html', {'propriedades':detalhes_propriedades , 'reviews':reviews, 'shortest':shortest})

@unauthenticated_user
def freedetalhes_propriedades(request, pk):
    detalhes_propriedades = Propriedade.objects.get(id=pk)
    reviews = Review.objects.filter(propriedade=detalhes_propriedades)
    
    contratos = Contrato.objects.filter(propriedade=detalhes_propriedades)
    shortest = timezone.now() + timedelta(days=10000)
    for i in contratos:
        if i.duracao < shortest:
            shortest = i.duracao

    return render(request, 'accounts/free_propriedades_detalhes.html', {'propriedades':detalhes_propriedades , 'reviews':reviews, 'shortest':shortest})

@login_required(login_url='login')
@allowed_users(['senhorio'])
def self_propriedade(request):
    self_propriedades = Propriedade.objects.all()
    return render(request, 'accounts/minhas_propriedades.html', {'propriedades':self_propriedades})


@login_required(login_url='login')
@allowed_users(['senhorio'])
def add_propriedade(request):
    senhorio = request.user.senhorio
    
    form = PropriedadeForm()
    if request.method == 'POST':
        form = PropriedadeForm(request.POST)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.senhorio = senhorio
            prop.save()
            return redirect('self-propriedades')

    context = {'form':form}
    return render(request, 'accounts/add_propriedade.html', context)

@login_required(login_url='login')
@allowed_users(['senhorio'])
def update_propriedade(request, pk):
    propriedade = Propriedade.objects.get(id=pk)
    
    form = UpdatePropriedadeForm(instance=propriedade)   
    if request.method == 'POST':
        form = UpdatePropriedadeForm(request.POST, request.FILES, instance=propriedade)
        if form.is_valid():
            form.save()
            return redirect('self-propriedades')

    context = {'form':form}
    return render(request, 'accounts/edit_propriedade.html', context)


@login_required(login_url='login')
@allowed_users(['senhorio'])
def delete_propriedade(request, pk):
    propriedade = Propriedade.objects.get(id=pk)
    if request.method == "POST":
        propriedade.delete()
        return redirect('self-propriedades')

    context = {'item':propriedade}
    return render(request, 'accounts/delete.html', context)


#------------------------------------OFERTAS--------------------------------------------------------------------

@login_required(login_url='login')
@allowed_users(['inquilino'])
def createOferta(request, pk, sk):
    propriedade = Propriedade.objects.get(id=pk)
    senhorio = Senhorio.objects.get(name=sk)
    inquilino = request.user.inquilino
    
    form = OfertaInquilinoForm()
    if request.method == 'POST':
        form = OfertaInquilinoForm(request.POST)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.inquilino = inquilino
            oferta.propriedade = propriedade
            oferta.senhorio = senhorio
            oferta.save()

            return redirect('propriedades')

    context = {'form':form , 'propriedade':propriedade}
    return render(request, 'accounts/oferta.html', context)


@login_required(login_url='login')
@allowed_users(['senhorio'])
def oferta_senhorio(request):
    ofertas = Oferta.objects.all()
    return render(request, 'accounts/ofertas_senhorio.html', {'ofertas':ofertas})

@login_required(login_url='login')
@allowed_users(['inquilino'])
def oferta_inquilino(request):
    ofertas = Oferta.objects.all()
    return render(request, 'accounts/ofertas_inquilino.html', {'ofertas':ofertas})

@login_required(login_url='login')
@allowed_users(['senhorio'])
def aceitar_oferta(request, pk):
    oferta = Oferta.objects.get(id=pk)
    propriedade = Propriedade.objects.get(id=oferta.propriedade.id)
    
    form = ContratoForm()
    if request.method == "POST":
        form = ContratoForm(request.POST)
        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.inquilino = oferta.inquilino
            contrato.senhorio = oferta.senhorio
            contrato.propriedade = oferta.propriedade
            contrato.periodo = oferta.periodo
            contrato.quantidade = oferta.quantidade
            if contrato.periodo == "Mensal":
                quant = oferta.quantidade * 30
                contrato.duracao = datetime.now()+timedelta(days=quant)
            if contrato.periodo == "Semestral":
                quant = oferta.quantidade * 182
                contrato.duracao = datetime.now()+timedelta(days=quant)
            if contrato.periodo == "Anual":
                quant = oferta.quantidade * 365
                contrato.duracao = datetime.now()+timedelta(days=quant)
            contrato.save()
        
            propriedade.numero_inquilinos += 1
            propriedade.numero_quartos -= 1
            if propriedade.numero_quartos == 0:
                propriedade.disponivel = False

            propriedade.save()
            oferta.delete()
            return redirect('contrato-senhorio')
    
    context = {'form':form , 'item':oferta}
    return render(request, 'accounts/aceitaroferta.html', context)


@login_required(login_url='login')
@allowed_users(['senhorio'])
def recusar_oferta(request, pk):
    oferta = Oferta.objects.get(id=pk)
    if request.method == "POST":
        oferta.delete()
        return redirect('oferta-senhorio')

    context = {'item':oferta}
    return render(request, 'accounts/recusaroferta.html', context)


#--------------------------------CONTRATOS------------------------------------------------------------



@login_required(login_url='login')
@allowed_users(['senhorio'])
def contrato_senhorio(request):
    contratos = Contrato.objects.all()

    senhorio = request.user.senhorio
    count = Contrato.objects.filter(senhorio = senhorio).count()
    if count > 0:
        contratosS = Contrato.objects.filter(senhorio = senhorio)
        for i in contratosS:
            if i.periodo == "Mensal":
                if timezone.now() > i.duracao:
                    i.expirou=True
            elif i.periodo == "Semestral":
                if timezone.now() > i.duracao:
                    i.expirou=True
            elif i.periodo == "Anual":
                if timezone.now() > i.duracao:
                    i.expirou=True

    return render(request, 'accounts/contratos_senhorio.html', {'contratos':contratos})

@login_required(login_url='login')
@allowed_users(['inquilino'])
def contrato_inquilino(request):
    contratos = Contrato.objects.all()

    inquilino = request.user.inquilino
    count = Contrato.objects.filter(inquilino = inquilino).count()
    if count > 0:
        contratosI = Contrato.objects.filter(inquilino = inquilino)
        for i in contratosI:
            if i.periodo == "Mensal":
                if timezone.now() > i.duracao:
                    i.expirou=True
            elif i.periodo == "Semestral":
                if timezone.now() > i.duracao:
                    i.expirou=True
            elif i.periodo == "Anual":
                if timezone.now() > i.duracao:
                    i.expirou=True
                    

    return render(request, 'accounts/contratos_inquilino.html', {'contratos':contratos})

@login_required(login_url='login')
@allowed_users(['inquilino'])
def terminar_contrato_inquilino(request, pk):
    contrato = Contrato.objects.get(id=pk)
    propriedade = contrato.propriedade

    if request.method == "POST":
        contrato.delete()
        propriedade.numero_inquilinos += -1
        propriedade.numero_quartos += 1
        if propriedade.numero_quartos > 0:
            propriedade.disponivel = True

        propriedade.save()
        return redirect('contrato-inquilino')

    context = {'item':contrato}
    return render(request, 'accounts/terminarcontratoi.html', context)

@login_required(login_url='login')
@allowed_users(['senhorio'])
def terminar_contrato_senhorio(request, pk):
    contrato = Contrato.objects.get(id=pk)
    propriedade = contrato.propriedade
    if request.method == "POST":
        contrato.delete()
        propriedade.numero_inquilinos += -1
        propriedade.numero_quartos += 1
        if propriedade.numero_quartos > 0:
            propriedade.disponivel = True
        propriedade.save()
        return redirect('contrato-senhorio')

    context = {'item':contrato}
    return render(request, 'accounts/terminarcontratos.html', context)

@login_required(login_url='login')
@allowed_users(['inquilino'])
def renovar_contrato(request, pk):
    contrato = Contrato.objects.get(id=pk)

    form = RenovarContratoForm(instance=contrato)
    if request.method == "POST":
        form = RenovarContratoForm(request.POST, instance=contrato)
        if form.is_valid():
            contrato = form.save(commit=False)
            if contrato.periodo == "Mensal":
                quant = contrato.quantidade * 30
                contrato.duracao += timedelta(days=quant)
            if contrato.periodo == "Semestral":
                quant = contrato.quantidade * 182
                contrato.duracao += timedelta(days=quant)
            if contrato.periodo == "Anual":
                quant = contrato.quantidade * 365
                contrato.duracao += timedelta(days=quant)
            contrato.expirou = False
            contrato.save()
            
            return redirect('contrato-inquilino')

    context = {'form':form , 'item':contrato}
    return render(request, 'accounts/renovarcontrato.html', context)

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


#Opens up page as PDF
class ViewPDF(View):
	def get(self, request, *args, **kwargs):

		pdf = render_to_pdf('accounts/recibo_template.html', data)
		return HttpResponse(pdf, content_type='application/pdf')


#Automaticly downloads to PDF file
class DownloadPDF(View):
    def get(self, request, pk, *args, **kwargs):
        contrato = Contrato.objects.get(id=pk)
        
        if contrato.periodo == "Mensal":
            preco = contrato.propriedade.preco
            periodo = "Mensalidades"
        elif contrato.periodo == "Semestral":
            preco = contrato.propriedade.preco_semestral
            periodo = "Semestralidades"
        else:
            preco = contrato.propriedade.preco_anual
            periodo = "Anualidades"
        
        total = int(preco)*int(contrato.quantidade)

        data = {"titulo": contrato.propriedade.titulo, 
        "local": contrato.propriedade.local, 
        "senhorio": contrato.senhorio.name, 
        "inquilino": contrato.inquilino.name, 
        "periodo": periodo, 
        "quantidade": contrato.quantidade, 
        "preco": preco, 
        "total": total,
        "fim": contrato.duracao,
        }
        
        pdf = render_to_pdf('accounts/recibo_template.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Fatura-Recibo %s.pdf" %(str(contrato.propriedade.titulo)+ " " +str(contrato.inquilino.name))
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response


#------------------------------------MENSAGENS------------------------------------------------------


@login_required(login_url='login')
def Inbox(request):
	messages = Message.get_messages(user=request.user)
	active_direct = None
	directs = None

	if messages:
		message = messages[0]
		active_direct = message['user'].username
		directs = Message.objects.filter(user=request.user, recipient=message['user'])
		directs.update(is_read=True)
		for message in messages:
			if message['user'].username == active_direct:
				message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_direct': active_direct,
		}

	template = loader.get_template('accounts/direct.html')

	return HttpResponse(template.render(context, request))

@login_required(login_url='login')
def UserSearch(request):
	query = request.GET.get("q")
	context = {}
	
	if query:
		users = User.objects.filter(Q(username__icontains=query))

		#Pagination
		paginator = Paginator(users, 6)
		page_number = request.GET.get('page')
		users_paginator = paginator.get_page(page_number)

		context = {
				'users': users_paginator,
			}
	
	template = loader.get_template('accounts/search_user.html')
	
	return HttpResponse(template.render(context, request))

@login_required(login_url='login')
def Directs(request, username):
	user = request.user
	messages = Message.get_messages(user=user)
	active_direct = username
	directs = Message.objects.filter(user=user, recipient__username=username)
	directs.update(is_read=True)
	for message in messages:
		if message['user'].username == username:
			message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_direct':active_direct,
	}

	template = loader.get_template('accounts/direct.html')

	return HttpResponse(template.render(context, request))


@login_required(login_url='login')
def NewConversation(request, username):
	from_user = request.user
	body = ''
	try:
		to_user = User.objects.get(username=username)
	except Exception as e:
		return redirect('usersearch')
	if from_user != to_user:
		Message.send_message(from_user, to_user, body)
	return redirect('inbox')

@login_required(login_url='login')
def SendDirect(request):
	from_user = request.user
	to_user_username = request.POST.get('to_user')
	body = request.POST.get('body')
	
	if request.method == 'POST':
		to_user = User.objects.get(username=to_user_username)
		Message.send_message(from_user, to_user, body)
		return redirect('inbox')
	else:
		HttpResponseBadRequest()

def checkDirects(request):
	directs_count = 0
	if request.user.is_authenticated:
		directs_count = Message.objects.filter(user=request.user, is_read=False).count()

	return {'directs_count':directs_count}



#--------------------------------REVIEWS---------------------------------------------------

def Rate(request, pk):
    propriedade = Propriedade.objects.get(id=pk)
    user = request.user

    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = user
            rate.propriedade = propriedade
            rate.save()
            return HttpResponseRedirect(reverse('detalhes-propriedades', args=[pk]))
    else:
        form = RateForm()

    template = loader.get_template('accounts/rate.html')
    
    context = {
        'form': form,
        'propriedade': propriedade,
    }
    return HttpResponse(template.render(context ,request))


def Rate_user(request, pk, group):
    if group == 'inquilino':
        avaliado = Inquilino.objects.get(id=pk)
    else: 
        avaliado = Senhorio.objects.get(id=pk)

    user = request.user

    if request.method == 'POST':
        form = RateUserForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = user
            if group == 'inquilino':
                rate.avaliadoI = avaliado
            else:
                rate.avaliadoS = avaliado
            rate.save()
            return HttpResponseRedirect(reverse('perfil-user', args=[pk, group]))
    else:
        form = RateForm()

    template = loader.get_template('accounts/rate_user.html')
    
    context = {
        'form': form,
        'avaliado': avaliado,
    }
    return HttpResponse(template.render(context ,request))