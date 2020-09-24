import setuptools

setuptools.setup(
    name="eol_jump_to",
    version="0.0.1",
    author="matiassalinas",
    author_email="matsalinas@uchile.cl",
    description="jump_to function version EOL",
    long_description="Redirect student to specific block if has access. Otherwise redirect to course index",
    url="https://eol.uchile.cl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "lms.djangoapp": [
            "eol_jump_to = eol_jump_to.apps:EolJumpToConfig",
        ]
    },
)
