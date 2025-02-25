from django.urls import path
from .views import get_page_assets,delete_asset,search_suppliers,get_movements_by_asset
urlpatterns = [
    path('',view=get_page_assets,name='assets'),
    path('delete/<int:id>',view=delete_asset,name="delete_asset"),
    path("search_supplier",view=search_suppliers,name="search_supplier"),
    path("movements/<int:asset_id>",view=get_movements_by_asset,name="asset_movements")
]