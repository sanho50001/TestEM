from django.test import TestCase
from .models import Item, Category, ExchangeProposal, UserProfile
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse

class ExchangeAcceptanceTests(TestCase):
    def setUp(self):
        User = get_user_model()

        # Создаем категорию, чтобы избежать IntegrityError
        self.category = Category.objects.create(name='Тестовая категория')

        # Создаем пользователей
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password123')
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123'
        )

        self.profile1 = UserProfile.objects.get_or_create(user=self.user1)
        self.profile2 = UserProfile.objects.get_or_create(user=self.user2)

        # Создаем товары с указанием категории
        self.item1 = Item.objects.create(
            title='Книга',
            description='Хорошая книга',
            category=self.category,  # <-- используем созданную выше
            condition='like_new',
            owner=self.user1
        )
        self.item2 = Item.objects.create(
            title='Футболка',
            description='Чистая футболка',
            category=self.category,  # <-- используем созданную выше
            condition='new',
            owner=self.user2
        )

        self.proposal = ExchangeProposal.objects.create(
            sender=self.user1,
            receiver=self.user2,
            offered_item=self.item1,
            desired_item=self.item2,
            status='pending'
        )

    def _add_messages_support(self, request):
        """Добавляет поддержку messages в тестовый запрос"""
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

    def test_accept_exchange(self):
        self.proposal.status = 'accepted'
        self.proposal.save()

        self.assertEqual(self.proposal.status, 'accepted')

        # Готовим тестовый запрос
        request = HttpRequest()
        request.user = self.user2
        self._add_messages_support(request)  # <-- добавляем поддержку сообщений

        # Вызываем функцию завершения обмена
        from .views import complete_exchange
        response = complete_exchange(request, self.proposal.pk)

        self.assertEqual(response.status_code, 302)

        # Проверяем, действительно ли предметы поменялись владельцами
        self.assertTrue(self.user2.items.filter(pk=self.item1.pk).exists())
        self.assertTrue(self.user1.items.filter(pk=self.item2.pk).exists())
        
        # Проверяем редирект
        self.assertEqual(response.url, reverse('item_detail', kwargs={'pk': self.proposal.receiver.id}))