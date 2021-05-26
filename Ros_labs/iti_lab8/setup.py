from setuptools import setup

package_name = 'iti_lab8'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ahmed',
    maintainer_email='ahmed_salah1996@yahoo.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ["pub=iti_lab8.node1:main",  "sub =iti_lab8.node2:main"
        ],
    },
)