from setuptools import find_packages, setup

package_name = 'turtles'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='usuario',
    maintainer_email='jorge.sales@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'rings = turtles.rings:main',
            'rings_exercise = turtles.rings_exercise:main',
            'rings_solution = turtles.rings_solution:main',
            
        ],
    },
)
