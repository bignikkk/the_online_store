from rest_framework import serializers

from .models import Category, Subcategory, Product, CartItem, Cart


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор субкатегорий."""

    class Meta:
        model = Subcategory
        fields = ('name', 'slug', 'image')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'image', 'subcategories')


class CategoryProductSerializer(serializers.ModelSerializer):
    """Сериализатор категории без подкатегорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug', 'image')


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор продукта."""

    subcategory = SubcategorySerializer(read_only=True)
    category = CategoryProductSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('name', 'slug', 'price', 'category', 'subcategory',
                  'image_small', 'image_medium', 'image_large')


class CartItemSerializer(serializers.ModelSerializer):
    """Сериализатор элемента корзины."""

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity', 'total_price')

    def validate(self, data):
        """Валидация на уникальность элемента."""
        request = self.context.get('request')
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        data['cart'] = cart

        product = data.get('product')
        if cart.items.filter(product=product).exists() and not self.instance:
            raise serializers.ValidationError('Этот товар уже в корзине!')

        return data


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор корзины."""

    items = CartItemSerializer(many=True)
    total_items = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total_items', 'total_cost')

    def get_total_items(self, obj):
        """Метод общего кол-ва элементов в корзине."""

        return obj.items.count()

    def get_total_cost(self, obj):
        """Метод общей стоимости элементов в корзине."""

        return sum(item.total_price for item in obj.items.all())
