import os
import platform
import re
import subprocess
import sys
from distutils.version import LooseVersion

from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name, source_dir=''):
        Extension.__init__(self, name, sources=[])
        self.source_dir = os.path.abspath(source_dir)


class CMakeBuild(build_ext):

    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError('CMake must be installed to build the following extensions: '
                               ', '.join(e.name for e in self.extensions))

        # self.debug = True

        cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
        if cmake_version < '3.2.0':
            raise RuntimeError("CMake >= 3.2.0 is required")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        ext_dir = os.path.join(os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name))),
                              'hole_filling_liepa')  # 'igl' -> 'hole_filling_liepa' ?

        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + ext_dir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]
        cmake_args.append('-DCMAKE_BUILD_TYPE=' + cfg)
        # cmake_args += ['-DDEBUG_TRACE=ON']

        if platform.system() == 'Windows':
            cmake_args.append(f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{cfg.upper()}={ext_dir}')
            cmake_generator = os.environ.get('CMAKE_GENERATOR', '')
            if cmake_generator != 'NMake Makefiles' and 'Ninja' not in cmake_generator:
                if sys.maxsize > 2 ** 32:
                    cmake_args += ['-A', 'x64']
                # build_args += ['--', '/m']
        else:
            build_args += ['--', '-j2']

        tmp = os.environ.get('AR', '')
        if 'arm64-apple' in tmp:
            tmp = os.environ.get('CMAKE_ARGS', '')
            if tmp:
                cmake_args += tmp.split(' ')

            tmp = os.environ.get('CC', '')
            print('C compiler', tmp)
            if tmp:
                cmake_args.append(f'-DCMAKE_C_COMPILER={tmp}')

            tmp = os.environ.get('CXX', '')
            print('CXX compiler', tmp)
            if tmp:
                cmake_args.append(f'-DCMAKE_CXX_COMPILER={tmp}')
        else:
            tmp = os.getenv('CC_FOR_BUILD', '')
            if tmp:
                print('Setting c compiler to', tmp)
                cmake_args.append(f'-DCMAKE_C_COMPILER={tmp}')

            tmp = os.getenv('CXX_FOR_BUILD', '')
            if tmp:
                print('Setting cxx compiler to', tmp)
                cmake_args.append(f'-DCMAKE_CXX_COMPILER={tmp}')

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''), self.distribution.get_version())

        tmp = os.getenv('target_platform', '')
        if tmp:
            print('target platfrom', tmp)
            if 'arm' in tmp:
                cmake_args.append('-DCMAKE_OSX_ARCHITECTURES=arm64')

        # print(cmake_args)
        # tmp = os.getenv('CMAKE_ARGS', '')

        # if tmp:
        #     tmp = tmp.split(' ')
        #     print('tmp', tmp)
        #     cmake_args += tmp

        # cmake_args += ['-DCMAKE_OSX_ARCHITECTURES' , 'arm64']
        # print(cmake_args)

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.source_dir] + cmake_args, cwd=self.build_temp, env=env)

        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)

        print()


setup(
    name='hole-filling-liepa',
    version='0.0.1',
    author='Ruslan Guseinov',
    description='Hole filling algorithm by P. Liepa',
    url='https://github.com/russelmann/hole-filling-liepa',
    ext_modules=[CMakeExtension('core', '../cpp')],
    install_requires=['numpy'],
    cmdclass=dict(build_ext=CMakeBuild),
    packages=find_packages(),
    # include_package_data=True,
    # package_data={'': ['*.pyd', '*.so']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    test_suite="test"
)
