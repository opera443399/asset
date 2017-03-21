"""www URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import ugettext_lazy as _

from assets import views as assets_views
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter


admin.site.site_header = _('Asset management')
admin.site.index_title = _('Site admin')
admin.site.site_title = _('Asset')

# ================================ API ================================
# Provide schema
schema_view = get_schema_view(title='ASSET RESTFUL API')
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'vendors', assets_views.VendorViewSet)
router.register(r'models', assets_views.DeviceTypeViewSet)
router.register(r'offerings', assets_views.InstanceTypeViewSet)
router.register(r'idcs', assets_views.IDCInfoViewSet)
router.register(r'os', assets_views.OSTypeViewSet)
router.register(r'endusers', assets_views.EndUserViewSet)
router.register(r'clusters', assets_views.ClusterViewSet)
router.register(r'bizunits', assets_views.BusinessUnitViewSet)
router.register(r'env', assets_views.RuntimeEnvironmentViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.

# ================================ URL ================================
urlpatterns = [
    #################################### index
    #
    url(r'^$', assets_views.show_index, name='index'),
    #################################### apps
    #
    url(r'^accounts/', include('accounts.urls')),
    url(r'^assets/', include('assets.urls')),
    #################################### admin
    #
    url(r'^admin/', include(admin.site.urls)),
    #################################### i18n
    #
    url(r'^i18n/', include('django.conf.urls.i18n')),
    ####################################  API
    #
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/schema/$', schema_view),
    url(r'^api/auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
