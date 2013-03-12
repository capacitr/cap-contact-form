import os, sys
from django.conf import settings

DIRNAME = os.path.dirname(__file__)
settings.configure(DEBUG=True,
               DATABASES={
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                    }
                },
               TEMPLATE_LOADERS=('dbtemplates.loader.Loader',),
               ROOT_URLCONF='cap_contact_form.urls',
               FIXTURE_DIRS='cap_contact_form/fixtures',
               SITE_ID='1',
               INSTALLED_APPS=('django.contrib.auth',
                              'django.contrib.contenttypes',
                              'django.contrib.sessions',
                              'django.contrib.admin',
                              'django.contrib.sites',
                              'dbtemplates',
                              'cap_contact_form',))

from django.test.simple import DjangoTestSuiteRunner
test_runner = DjangoTestSuiteRunner(verbosity=1)
failures = test_runner.run_tests(['cap_contact_form', ])
if failures:
    sys.exit(failures)