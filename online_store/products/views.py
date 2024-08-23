from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404

from .models import Category, Product, Cart, CartItem
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    CartSerializer,
    CartItemSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для росмотра категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для просмотра товаров."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10


class CartViewSet(viewsets.ViewSet):
    """Вьюсет для управления корзиной пользователя."""

    permission_classes = [IsAuthenticated]

    @staticmethod
    def add_to_cart(serializer_class, request):
        """Создание товара в корзине."""

        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        data = {**request.data, 'cart': cart.id}
        serializer = serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        url_path='add-item'
    )
    def add_item(self, request):
        """Добавление товара в корзину."""

        return self.add_to_cart(CartItemSerializer, request)

    @action(
        detail=False,
        methods=['patch'],
        permission_classes=[IsAuthenticated],
        url_path=r'update-item/(?P<pk>\d+)'
    )
    def update_item_quantity(self, request, pk=None):
        """Изменение количества товара в корзине."""

        cart = self.get_or_create_cart(request.user)
        product = get_object_or_404(Product, id=pk)
        item = CartItem.objects.filter(cart=cart, product=product).first()

        if item:
            serializer = CartItemSerializer(
                item,
                data=request.data,
                partial=True,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'errors': 'Product not found in cart!'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['delete'],
        permission_classes=[IsAuthenticated],
        url_path=r'remove-item/(?P<pk>\d+)'
    )
    def remove_item(self, request, pk=None):
        """Удаление товара из корзины."""

        cart = self.get_or_create_cart(request.user)
        product = Product.objects.get(id=pk)
        obj = CartItem.objects.filter(
            cart=cart, product=product
        )
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Product not found in cart!'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='summary'
    )
    def summary(self, request):
        """Вывод корзины с продуктами и общей стоимостью."""

        cart = self.get_or_create_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['delete'],
        permission_classes=[IsAuthenticated],
        url_path='clear'
    )
    def clear(self, request):
        """Полная очистка корзины."""

        cart = self.get_or_create_cart(request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_or_create_cart(self, user):
        """Получить или создать корзину для данного пользователя."""

        cart, created = Cart.objects.get_or_create(user=user)
        return cart
