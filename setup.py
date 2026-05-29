from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="vehicle_rental_management",
    version="1.1.0",
    description="Vehicle Rental Management for ERPNext v15+",
    author="Your Company",
    author_email="dev@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
