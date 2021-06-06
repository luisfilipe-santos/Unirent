from django.contrib import admin
from django.urls import path, include
from . import views

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('', views.home, name="home"),

    #------API------

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path(api)
    path('api/senhorio-list/', views.SenhorioList.as_view()),
    path('api/inquilino-list/', views.InquilinoList.as_view()),
    path('api/propriedade-list/', views.PropriedadeList.as_view()),
    path('api/senhorio-detail/<int:pk>', views.SenhorioDetail.as_view()),
    path('api/inquilino-detail/<int:pk>', views.InquilinoDetail.as_view()),
    path('api/propriedade-detail/<int:pk>', views.PropriedadeDetail.as_view()),
    path('api/oferta-list/',views.OfferList.as_view()),
    path('api/contract-list/',views.ContractList.as_view()),
    path('api/message-list/',views.MessageList.as_view()),
    path('api/review-list/', views.ReviewList.as_view()),
    path('api/reviewUser-list/', views.ReviewUserList.as_view()),
    path('api/oferta-detail/<int:pk>', views.OfferDetail.as_view()),
    path('api/contract-detail/<int:pk>', views.ContractDetail.as_view()),
    path('api/message-detail/<int:pk>', views.MessageDetail.as_view()),
    path('api/review-detail/<int:pk>', views.ReviewDetail.as_view()),
    path('api/reviewUser-detail/<int:pk>', views.ReviewUserDetail.as_view()),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    #-------
    path('exportinquilinos/', views.export_inquilinos, name="export-inquilinos"),
    path('exportsenhorios/', views.export_senhorios, name="export-senhorios"),
    path('exportpropriedades/', views.export_propriedades, name="export-propriedades"),

    path('importinquilinos/', views.import_inquilinos, name="import-inquilinos"),
    path('importsenhorios/', views.import_senhorios, name="import-senhorios"),
    path('importpropriedades/', views.import_propriedades, name="import-propriedades"),
    
    path('register/', views.registerPage, name="register"),
    path('registerS/', views.registerSPage, name="registerS"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('freepropriedades/', views.freeProps, name="free-propriedades"),
    path('freepropriedadesdetalhes/<str:pk>/', views.freedetalhes_propriedades, name="free-detalhes-propriedades"),

    path('senhorios/', views.userPage, name="senhorio-page"),
    path('users/', views.userPage, name="user-page"),
    path('definicoes-user/', views.accountSettings, name='definicoes-inquilino'),
    path('definicoes-senhorio/', views.accountSettingsSenhorio, name='definicoes-senhorio'),
    path('userperfil/<str:pk>/<str:group>', views.perfil_user, name='perfil-user'),
    path('ratepropriedade/<str:pk>/<str:group>', views.Rate_user, name='rate-user'),

    path('propriedades/', views.propriedades, name='propriedades'),
    path('propriedadesdetalhes/<str:pk>/', views.detalhes_propriedades, name='detalhes-propriedades'),
    path('minhaspropriedades/', views.self_propriedade, name='self-propriedades'),
    path('addpropriedades/', views.add_propriedade, name='add-propriedades'),
    path('updatepropriedades/<str:pk>/', views.update_propriedade, name='update-propriedades'),
    path('deletepropriedades/<str:pk>/', views.delete_propriedade, name='delete-propriedades'),
    path('ratepropriedade/<str:pk>/', views.Rate, name='rate-propriedades'),

    path('criaroferta/<str:pk>/<str:sk>/', views.createOferta, name='create-oferta'),
    path('ofertassenhorio/', views.oferta_senhorio, name='oferta-senhorio'),
    path('ofertasinquilino/', views.oferta_inquilino, name='oferta-inquilino'),
    path('recusaroferta/<str:pk>/', views.recusar_oferta, name='recusar-oferta'),
    path('aceitaroferta/<str:pk>/', views.aceitar_oferta, name='aceitar-oferta'),

    path('contratossenhorio/', views.contrato_senhorio, name='contrato-senhorio'),
    path('contratosinquilino/', views.contrato_inquilino, name='contrato-inquilino'),
    path('terminarcontratoinquilino/<str:pk>/', views.terminar_contrato_inquilino, name="terminar-contrato-inquilino"),
    path('terminarcontratosenhorio/<str:pk>/', views.terminar_contrato_senhorio, name="terminar-contrato-senhorio"),
    path('renovarcontrato/<str:pk>/', views.renovar_contrato, name="renovar-contrato"),
    path('recibo/<str:pk>/', views.DownloadPDF.as_view(), name="recibo"),

    path('inbox/', views.Inbox, name='inbox'),
   	path('directs/<username>', views.Directs, name='directs'),
   	path('new/', views.UserSearch, name='usersearch'),
   	path('new/<username>', views.NewConversation, name='newconversation'),
   	path('send/', views.SendDirect, name='send_direct'),
]


