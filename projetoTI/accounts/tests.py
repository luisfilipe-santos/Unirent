from django.test import TestCase
from accounts.models import *
from django.contrib.auth.models import User

# Create your tests here.

#-------------------------------TEST MODELS----------------------------------------------

class SenhorioTestCase():
    
    def setUp(self):
        Senhorio.objects.create(user=User, name='Pedro', idade='34', email='teste@teste.com', bio='testeDjango para senhorios')
        Senhorio.obkects.create(user=User, name='Afonso', idade='21', email='testeAfonso@testeAfonso.com', bio='testAfonso senhorio')
        Senhorio.objects.create(user=User,name='Beatriz', idade='25', email='testeBeatriz@testeBeatriz.com',bio='testeBeatroz senhoria')
    
    def testLandlordName(self):
        landlord = Senhorio.objects.get(id=1)
        field_label = Senhorio._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

class PropriedadeTestCase():
    
    def setUp(self):
        Propriedade.objects.create(senhorio=Senhorio, titulo='Exemp1', preco='99999', preco_semestral='49999', preco_mensal='499', local='Lisboa', numero_quartos='3', numero_inquilinos='3', area='150')
        Propriedade.objects.create(senhorio=Senhorio, titulo='Exemp2', preco='111111', preco_semestral='19999', preco_mensal='500', local='Porto', numero_quartos='6', numero_inquilinos='5', area='200')
        Propriedade.objects.create(senhorio=Senhorio, titulo='Exemp1', preco='160000', preco_semestral='85262', preco_mensal='3000', local='Leiria', numero_quartos='8', area='500')

    def testPropertyTitle(self):
        prop = Propriedade.objects.get(id=1)
        field_label = Propriedade._meta.get_field('titulo').verbose_name
        self.assertEqual(field_label, 'titulo')

class InquilinoTestCase():

    def setUp(self):
        Inquilino.objects.create(user=User, name='Joao', propriedade=Propriedade, email='testJoao@testJoao.com', idade='43', genero='Masculino')
        Inquilino.objects.create(user=User, name='Henrique', propriedade=Propriedade, email='testHenry@testHenry.com', idade='32', genero='Masculino')
        Inquilino.objects.create(user=User, name='Ines', propriedade=Propriedade, email='testInes@testInes.com', idade='28', genero='Feminino')
    
    def testTenantName(self):
        tenant = Inquilino.objects.get(id=1)
        field_label = Inquilino._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

class OfertaTestCase():
    
    def setUp(self):
        Oferta.objects.create(inquilino=Inquilino, senhorio=Senhorio, propriedade=Propriedade, status='Em espera', periodo='Mensal')
        Oferta.objects.create(inquilino=Inquilino, senhorio=Senhorio, propriedade=Propriedade, status='Rejeitada', periodo='Semestral')
        Oferta.objects.create(inquilino=Inquilino, senhorio=Senhorio, propriedade=Propriedade, status='Em espera', periodo='Anual')

    def test_property_owner(self):
        pw = Oferta.objects.get(id=1)
        field_label = Oferta._meta.get_field('senhorio').verbose_name
        self.assertEqual(field_label, 'senhorio')        
        

class ContratoTestCase():
    
    def setUp(self):
        Contrato.objects.create(inquilino=Inquilino, senhorio=Senhorio, propriedade=Propriedade, periodo='Mensal')
        Contrato.objects.create(inquilino=Inquilino, senhorio=Senhorio, propriedade=Propriedade, periodo='Semestral')
        Contrato.objects.create(inquilino=Inquilino, senhorio=Senhorio, propriedade=Propriedade, status='Em espera', periodo='Anual')

    def test_contract_property(self):
        prop = Contrato.objects.get(id=1)
        field_label = Contrato._meta.get_field('propriedade').verbose_name
        self.assertEqual(field_label, 'propriedade')

class MessageTestCase():
    
    def setUp(self):
        Message.objects.create(user=User, sender=User, recipient=User, body='teste teste')
        Message.objects.create(user=User, sender=User, recipient=User, body='teste 2 teste 2')
        #Message.objects.create()
        #Message.objects.create()
    
    def test_message_content(self):
        message = Message.objects.get(id=2)
        field_label = Message._meta.get_field('body').verbose_name
        self.assertEqual(field_label, 'body')

class ReviewTestCase():
    
    def setUp(self):
        Review.object.create(propriedade=Propriedade, user=User, text='yes yes', rate='7')
        Review.object.create(propriedade=Propriedade, user=User, text='whoo', rate='10')
      
    def test_review_user(self):
        rev = Review.objects.get(id=1)
        field_label = Review._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

class ReviewUserTestCase():
    
    def setUp(self):
        ReviewUser.object.create(avaliadoI=Inquilino, avaliadoS=Senhorio, user=User, text='10/10 good', rate='10')
        #ReviewUser.object.create()
        #ReviewUser.object.create()

    def test_reviewUser_text(self):
        revUser = ReviewUser.objects.get(id=1)
        field_label = ReviewUser._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

#-------------------------------------TEST VIEWS----------------------------------------------------

class ViewTest(TestCase):

    def test_login(self):
        pass
    
    def test_login_incorrect(self):
        pass

    def test_home(self):
        pass

    def test_register_inquilino_page(self):
        pass

    def test_register_senhorio_page(self):
        pass

    def test_logout(self):
        pass

    def test_account_setting_page(self):
        pass

    def test_account_setting_senhorio(self):
        pass

    def test_user_page(self):
        pass

    def test_perfil_user(self):
        pass

##PROPERTIES VIEWS

    def test_propriedades(self):
        pass

    def test_freeProps_page(self):
        pass

    def test_propDetails_page(self):
        pass

    def test_freePropDetails_page(self):
        pass

    def test_ownProps_page(self):
        pass

    def test_addProps(self):
        pass

    def test_propsUpdates(self):
        pass

    def test_deleteProps(self):
        pass

## OFFER VIEWS

    def test_createOffer(self):
        pass

    def test_offerLandlord(self):
        pass

    def test_offerTenant(self):
        pass

    def test_acceptOffer(self):
        pass

    def test_denyOffer(self):
        pass

    def test_wrong_offer(self):
        pass

## CONTRACT VIEWS

    def test_landlordContract(self):
        pass

    def test_endTenantContract(self):
        pass

    def test_endLandlordContract(self):
        pass

    def test_renew_contract(self):
        pass

## MESSAGES VIEWS

    def test_inbox(self):
        pass

    def test_user_search(self):
        pass

    def test_directs(self):
        pass

    def test_newConvo(self):
        pass

    def test_sendDirect(self):
        pass

    def test_checkDirects(self):
        pass

## RATES VIEWS

    def test_rate(self):
        pass

    def test_userRate(self):
        pass

#-------------------------------------TEST API------------------------------------------------------



#------------------------------------TEST FORMS-----------------------------------------------------

class CreateUserFormTest(TestCase):

    pass

class InquilinoFormTest(TestCase):
    pass

class SenhorioFormTest(TestCase):
    pass

class PropriedadeFormTest(TestCase):
    pass

class UpdatePropriedadeFormTest(TestCase):
    pass

class OfertaInquilinoFormTest(TestCase):
    pass

class ContratoFormTest(TestCase):
    pass

class RenovarContratoFormTest(TestCase):
    pass

class RateFormTest(TestCase):
    pass

class RateUserFormTest(TestCase):
    pass