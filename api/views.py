from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .serializers import *
# Create your views here.

User = get_user_model()


class Register_User(APIView):
    permission_classes = [AllowAny, ]

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
        }

    def get(self, request):
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        print(request.user.is_authenticated)
        try:
            email = request.data["email"]
            password = request.data["password"]
            name = request.data["name"]
        except KeyError:
            pass
        print(email, password)
        if email and password:
            user = User.objects.create_user(
                email=email, password=password, name=name)
            user.save()
            token = self.get_tokens_for_user(user)
            print("save")
            return Response({"status": "success", "message": "Data SuccessFully Created", "token": token}, status=status.HTTP_200_OK)
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            user = User.objects.get(email=request.user)
            print(user.country, user.phone_number)
            print(request.data.items())
            print(request.FILES)
            try:
                if request.FILES["avatar"]:
                    user.avatar = request.FILES["avatar"]
                    user.save()
            except MultiValueDictKeyError:
                pass
            try:
                for (key, data) in request.data.items():
                    print(key, data)
                    if key == 'password':
                        user.set_password(data)
                        user.save()
                    if key == 'country':
                        user.country = data
                        user.save()
                    if key == 'phone_number':
                        user.phone_number = data
                        user.save()
            except ValueError:
                return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)
            user.refresh_from_db()
            return Response({"status": "success", "data": Custom_User_Serializer(user).data}, status=status.HTTP_200_OK)
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)


class Login_User(APIView):
    permission_classes = [AllowAny, ]

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
        }

    def get(self, request):
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            print(request.user)
            user = User.objects.get(email=request.user)
            user_serializer = Custom_User_Serializer(user).data
            return Response({"status": "success", "data": user_serializer})
        return Response({"message": "error"}, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.user.is_authenticated)
        print(request.data)
        try:
            email = request.data["email"]
            password = request.data["password"]
        except KeyError:
            pass
        print(email, password)
        if email and password:
            user = User.objects.filter(email=email)
            if user.exists():
                user = user[0]
                if check_password(password, user.password):
                    token = self.get_tokens_for_user(user)
                    print("save")
                    return Response({"status": "success", "message": "Log in succesful", "token": token}, status=status.HTTP_200_OK)
                return Response({"status": "error", "message": "Login Error"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status": "error", "message": "Login Error"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "error", "message": "Login Error"}, status=status.HTTP_400_BAD_REQUEST)


class Products_View(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        product = Product.objects.all()
        product_serializer = Product_Serializer(product, many=True).data
        return Response({"message": "success", "products": product_serializer})


class Cart_View(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = User.objects.get(email=request.user)
        cart = Cart.objects.filter(user=user)
        if cart.exists():
            cart_serializer = Cart_Serializer(cart, many=True).data
            return Response({"message": "success", "data": cart_serializer})
        return Response({"message": "success", "data": []})

    def post(self, request):
        user = User.objects.get(email=request.user)
        product_id = request.data["productID"]
        cart = Cart.objects.filter(user=user)
        product = Product.objects.filter(id=product_id)
        if cart.exists():
            for cart_item in cart:
                if cart_item.product == product[0]:
                    cart_item.product_no = cart_item.product_no + 1
                    cart_item.save()
                    updated_cart = Cart.objects.filter(user=user)
                    return Response({"message": "success", "data": Cart_Serializer(updated_cart, many=True).data}, status=status.HTTP_200_OK)
            cart = Cart.objects.create(user=user, product=product[0])
            cart.save()
            updated_cart = Cart.objects.filter(user=user)
            return Response({"message": "success", "data": Cart_Serializer(updated_cart, many=True).data}, status=status.HTTP_200_OK)
        cart = Cart.objects.create(user=user, product=product[0])
        cart.save()
        updated_cart = Cart.objects.filter(user=user)
        return Response({"message": "success", "data": Cart_Serializer(updated_cart, many=True).data}, status=status.HTTP_200_OK)
