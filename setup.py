import os
import sys
from setuptools import setup


def read(f):
    try:
        with open(f, 'r') as h:
            return h.read()
    except IOError:
        return ''


install_reqs = [
    l for l in read('requirements.txt').splitlines() if not l.startswith('#')
]

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'django_auth_spnego'))

setup(
    name='django-auth-spnego2',
    version='5.03',
    url='https://github.com/alfonsrv/django-auth-spnego',
    description='Django Authentication Backend for Single Sign-On via Kerberos SPNEGO',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    packages=['django_auth_spnego'],
    package_data={'django_auth_spnego': ['./*', 'templates/*']},
    author='Brandon Ewing, alfonsrv',
    author_email='alfonsrv@protonmail.com',
    include_package_data=True,
    install_requires=install_reqs,
    license='Apache 2.0',
    python_requires='>=3.6',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.1',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
