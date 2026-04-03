"""
Poor Man's Router - 穷鬼智能模型路由

专门聚合每日免费额度模型的智能路由
"""

from setuptools import setup

setup(
    name="poor-mans-router",
    version="1.0.0",
    description="穷鬼智能模型路由 - 专为初学者和小用量用户设计",
    author="Your Name",
    author_email="your@email.com",
    url="https://github.com/yourname/poor-mans-router",
    py_modules=["poor_mans_router"],
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)
