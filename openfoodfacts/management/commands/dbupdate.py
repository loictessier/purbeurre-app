from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from openfoodfacts.models import Category, Product

import re
import requests
import json
from os import path

NUTRITION_GRADES = ["A", "B", "C", "D", "E"]


class Command(BaseCommand):
    help = 'Update the database'

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()

        directory = path.dirname(__file__)
        config_file = path.join(directory, "dbupdate.config.json")
        with open(config_file) as json_data:
            categories = json.load(json_data)['categories']
        if len(categories) > 0:
            self.get_categories_from_file(categories)
        else:
            self.get_categories()
        self.get_products()

    def get_categories_from_file(self, categories):
        for cat in categories:
            if self._is_category_valid(cat):
                category = Category(
                    name=cat['name'],
                    off_identifier=re.sub(r'.*:', '', cat['id']))
                category.save()

    # get categories - insert them in database
    def get_categories(self):
        resp = requests.get("https://fr.openfoodfacts.org/categories.json")
        data = resp.json()
        for category_dict in data['tags']:
            if self._is_category_valid(category_dict):
                category = Category(
                    name=category_dict['name'],
                    off_identifier=re.sub(r'.*:', '', category_dict['id']))
                category.save()

    def _is_category_valid(self, category_dict):
        # only retrieve category with name not having ':' in it
        if (":" not in category_dict['name'] and
                len(category_dict['name']) < 150):
            return True

    # get some products - insert them in database
    def get_products(self):
        # get most populars products
        payload = {
            "search_simple": "1",
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": "",
            "tagtype_1": "nutrition_grades",
            "tag_contains_1": "contains",
            "tag_1": "",
            "sort_by": "unique_scans_n",
            "page_size": "400",
            "json": "1"
        }
        for category in Category.objects.all():
            for grade in NUTRITION_GRADES:
                payload['tag_0'] = category.name
                payload['tag_1'] = grade
                resp = requests.get("https://fr.openfoodfacts.org/cgi/search.pl", params=payload)
                resp = resp.json()
                for p in resp['products']:
                    cpt = 0
                    # insert products retrieved
                    # TODO validation sur nom, url_img (regex url valide ou requests.get et code 200), img_nutrinfo_url
                    try:
                        product = Product(
                            name=p['product_name_fr'],
                            nutriscore=p['nutrition_grades'],
                            img_nutrinfo_url=p['image_nutrition_url'],
                            img_url=p['image_url'],
                            off_url=p['url'],
                            popularity=p['unique_scans_n'],
                            category=category)
                        product.save()
                        cpt += 1
                        if cpt >= 50:
                            break
                    except KeyError:
                        print("Invalid product - missing informations : ", self.get_product_summary(p))
                    except IntegrityError:
                        print("Key already exists", p.get('product_name_fr'))

    def get_product_summary(self, produit):
        return "Produit = { name : " + produit.get('product_name_fr', "empty") \
            + ", nutriscore : " + produit.get('nutrition_grades', "empty") \
            + ", img_nutrinfo_url :" + produit.get('image_nutrition_url', "empty") \
            + ", img_url :" + produit.get('image_url', "empty") \
            + ", off_url :" + produit.get('url', "empty") \
            + ", popularity :" + str(produit.get('unique_scans_n', "empty")) + " }"
