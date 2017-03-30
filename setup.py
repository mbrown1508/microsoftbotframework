from setuptools import setup


setup(name='microsoftbotframework',
      version='0.1.10',
      description='A wrapper for the microsoft bot framework API',
      classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.5',
            'Topic :: Communications :: Chat',
      ],
      keywords='microsoft bot framework flask celery',
      url='https://github.com/Grungnie/microsoftbotframework',
      author='Matthew Brown',
      author_email='mbrown1508@outlook.com',
      license='MIT',
      packages=['microsoftbotframework'],
      install_requires=[
            "Flask",
            "celery",
            "requests",
            "redis",
            "pyyaml",
            "cryptography",
      ],
      dependency_links=[
            'https://github.com/jpadilla/pyjwt/archive/master.zip#egg=PyJWT',
      ],
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      )
