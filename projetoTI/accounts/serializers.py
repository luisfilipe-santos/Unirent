from rest_framework import serializers
from .models import *

class SenhorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Senhorio
        fields = '__all__'

    def create(self, validated_data):
        ll = super(SenhorioSerializer, self).create(validated_data)
        ll.save()
        return ll

class InquilinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquilino
        fields = '__all__'
    
    def create(self, validated_data):
        tn = super(InquilinoSerializer, self).create(validated_data)
        tn.save()
        return tn

class PropriedadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propriedade
        fields = '__all__'
    
    def crate(self,validated_data):
        pp = super(PropriedadeSerializer, self).create(validated_data)
        pp.save()
        return pp

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oferta
        fields = '__all__'

    def create(self, validated_data):
        offer = super(OfferSerializer, self).create(validated_data)
        offer.save()
        return offer

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrato
        fields = '__all__'

    def create(self, validated_data):
        ct = super(ContractSerializer, self).create(validated_data)
        ct.save()
        return ct

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields  = '__all__'

    def create(self, validated_data):
        mss = super(MessageSerializer, self).create(validated_data)
        mss.save()
        return mss

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields  = '__all__' 

    def create(self, validated_data):
        rev = super(ReviewSerializer, self).create(validated_data)
        rev.save()
        return rev

class ReviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewUser
        fields  = '__all__'

    def create(self, validated_data):
        revUser = super(ReviewUserSerializer, self).create(validated_data)
        revUser.save()
        return revUser
