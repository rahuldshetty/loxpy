from setuptools import setup

setup(
    name="loxpy",
    version="1.0",
    description="Another interpreter designed in Python",
    author="Rahul D Shetty",
    author_email="35rahuldshetty@gmail.com",
    scripts=[],
    entry_points={"console_scripts": ["loxpy = __main__:main"]},
)
