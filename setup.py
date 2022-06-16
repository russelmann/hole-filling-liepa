from skbuild import setup

setup(
    name='hole-filling-liepa',
    version='0.0.3',
    author='Ruslan Guseinov',
    description='Hole filling algorithm by P. Liepa',
    url='https://github.com/russelmann/hole-filling-liepa',
    python_requires=">=3.8",
    #ext_modules=[CMakeExtension('hole_filling_liepa', 'cpp')],
    install_requires=['numpy'],
    #cmdclass=dict(build_ext=CMakeBuild),
    #packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    package_dir={'': 'cpp'},
    cmake_source_dir='cpp',
    py_modules=[],
    test_suite='test',
)
