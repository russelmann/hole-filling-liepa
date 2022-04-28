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
    debug: bool = False

    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError('CMake must be installed to build the following extensions: '
                               ', '.join(e.name for e in self.extensions))
        cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
        if cmake_version < '3.2.0':
            raise RuntimeError("CMake >= 3.2.0 is required")
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        ext_dir = os.path.join(os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name))),
                               'hole_filling_liepa')  # 'igl' -> 'hole_filling_liepa' ?
        cfg = 'Debug' if self.debug else 'Release'

        cmake_args = [f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={ext_dir}',
                      f'-DPYTHON_EXECUTABLE={sys.executable}',
                      f'-DCMAKE_BUILD_TYPE={cfg}']
        # cmake_args += ['-DDEBUG_TRACE=ON']
        build_args = ['--config', cfg]

        if platform.system() == 'Windows':
            cmake_args.append(f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{cfg.upper()}={ext_dir}')
            cmake_generator = os.environ.get('CMAKE_GENERATOR', '')
            if cmake_generator != 'NMake Makefiles' and 'Ninja' not in cmake_generator:
                if sys.maxsize > 2 ** 32:
                    cmake_args += ['-A', 'x64']
                # build_args += ['--', '/m']
        else:
            build_args += ['--', '-j2']

        env_ar = os.environ.get('AR', '')
        if 'arm64-apple' in env_ar:
            if env_ar := os.environ.get('CMAKE_ARGS', ''):
                cmake_args += env_ar.split(' ')

            env_ar = os.environ.get('CC', '')
            print('C compiler', env_ar)
            if env_ar:
                cmake_args.append(f'-DCMAKE_C_COMPILER={env_ar}')

            env_ar = os.environ.get('CXX', '')
            print('CXX compiler', env_ar)
            if env_ar:
                cmake_args.append(f'-DCMAKE_CXX_COMPILER={env_ar}')
        else:
            if env_ar := os.getenv('CC_FOR_BUILD', ''):
                print('Setting c compiler to', env_ar)
                cmake_args.append(f'-DCMAKE_C_COMPILER={env_ar}')

            if env_ar := os.getenv('CXX_FOR_BUILD', ''):
                print('Setting cxx compiler to', env_ar)
                cmake_args.append(f'-DCMAKE_CXX_COMPILER={env_ar}')

        env = os.environ.copy()
        env['CXXFLAGS'] = env.get('CXXFLAGS', '') + f' -DVERSION_INFO=\\"{self.distribution.get_version()}\\"'

        env_platform = os.getenv('target_platform', '')
        if env_platform:
            print('target platfrom', env_platform)
            if 'arm' in env_platform:
                cmake_args.append('-DCMAKE_OSX_ARCHITECTURES=arm64')

        # print(cmake_args)
        # if env_cmake_args := os.getenv('CMAKE_ARGS', ''):
        #     env_cmake_args = env_cmake_args.split(' ')
        #     print('env CMAKE_ARGS', env_cmake_args)
        #     cmake_args += env_cmake_args
        # cmake_args += ['-DCMAKE_OSX_ARCHITECTURES', 'arm64']
        # print(cmake_args)

        os.makedirs(self.build_temp, exist_ok=True)
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
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    test_suite="test"
)
