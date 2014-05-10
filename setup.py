from setuptools import setup, find_packages

required = [line for line in open('requirements/base.txt').read().split("\n")]

setup(
    name='django-flatcontent',
    version=__import__('flatcontent').__version__,
    description='Django FlatContent is intended as a flatpages-like app but for smaller chunks of content that can be edited in the Django admin.',
    long_description=open('README.rst').read(),
    author='Oregon Center for Applied Science',
    author_email='support@orcasinc.com',
    url='http://github.com/orcasgit/django-flatcontent',
    install_requires=["setuptools"] + required,
    download_url='http://github.com/orcasgit/django-flatcontent/downloads',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False, # because we're including media that Django needs
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

