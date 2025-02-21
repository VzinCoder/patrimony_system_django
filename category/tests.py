from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Category
from .forms import CategoryForm
from django.db.utils import IntegrityError
# Create your tests here.


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = {
            'name':"Name category",
            'description':"Description Category"
        }

    def test_create(self):
        category = self.category
        Category.objects.create(**category)
        category_found = Category.objects.filter(name=category.get('name')).first()
        self.assertEqual(category.get('name'),category_found.name)
        self.assertEqual(category.get('description'),category_found.description)
    
    def test_unique_name(self):
        category = self.category
        Category.objects.create(**category)
        with self.assertRaises(IntegrityError):
            Category.objects.create(**category)
    
    def test_blank_name(self):
        category = self.category
        category['name'] = ''
        category = Category(**category)
        with self.assertRaisesMessage(ValidationError,'Este campo não pode estar vazio.'):
            category.full_clean()
    
    def test_null_name(self):
        category = self.category
        category['name'] = None
        category = Category(**category)
        with self.assertRaisesMessage(ValidationError,'Este campo não pode ser nulo.'):
            category.full_clean()

class CategoryFormTest(TestCase):
    def setUp(self):
        self.category = {
            'name':"Name category",
            'description':"Description Category"
        }

    def test_create_category(self):
        form = CategoryForm(data=self.category)
        self.assertTrue(form.is_valid())
        category_created = form.save()
        self.assertEqual(self.category['name'], category_created.name)
        self.assertEqual(self.category['description'], category_created.description)
    
    def test_unique_name_create_category(self):
        Category.objects.create(**self.category) # create category
        form = CategoryForm(data=self.category)
        self.assertFalse(form.is_valid())
        self.assertIn("Já existe uma categoria com este nome. Escolha outro nome.",form.errors['name'])
        
class GetPageCategoriesView(TestCase):
    def setUp(self):
        self.category = {
            'name':"Name category",
            'description':"Description Category"
        }
        self.categories = self.popule_category(15)

    def popule_category(self,qty):
        category = self.category
        def create_category(i):
            new_category = {
                "name": f'{category['name']}-{i}',
                "description": f'{category['description']}-{i}'
            }
            return Category.objects.create(**new_category)
        return [ create_category(i) for i in range (0,qty) ]

    def test_get_page_success(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'categories.html')
        titleHTML = '<h2 class="text-4xl lg:text-6xl font-semibold text-gray-900 dark:text-white mb-10">Categoria</h2>'
        self.assertContains(response,titleHTML)
        self.assertIn('page_obj',response.context)
    
    def test_pagination(self):
        response = self.client.get(reverse('categories'))
        page_obj = response.context.get('page_obj')
        # total categoriess
        self.assertEqual(page_obj.paginator.count,len(self.categories))
        # number page
        self.assertEqual(page_obj.number,1)
        # 10 categories per page
        self.assertEqual(len(page_obj),10)
        # order desc by id
        self.categories.reverse()
        for i in range(0,len(page_obj)):
           category = self.categories[i]
           category_page = page_obj[i]
           self.assertEqual(category.id,category_page.id)
           self.assertEqual(category.name,category_page.name)
           self.assertEqual(category.description,category_page.description)

        # in html
        element_html_show_total = f'<span class="font-semibold text-gray-900 dark:text-white">{page_obj.paginator.count}</span>'
        self.assertContains(response,element_html_show_total)
        for i in self.categories:
           # categorys ins html
           self.assertContains(response,category.name)
           self.assertContains(response,category.description)
    
    def test_pagination_page_2(self):
        response = self.client.get(reverse('categories'),{'page':2})
        page_obj = response.context.get('page_obj')
        # total categories
        self.assertEqual(page_obj.paginator.count,len(self.categories))
        # number page
        self.assertEqual(page_obj.number,2)
        # 5 categories in page
        self.assertEqual(len(page_obj),5)

    def test_create_category_success(self):
        response = self.client.post(reverse('categories'),self.category)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'categories.html')
        message_success = f'Categoria {self.category.get('name')} criada com sucesso'
        self.assertContains(response,message_success)
        category_created = Category.objects.filter(name=self.category.get('name')).first()
        self.assertEqual(category_created.name,self.category.get('name'))
        self.assertEqual(category_created.description,self.category.get('description'))
