# (C) Copyright 2021- United States Government as represented by the Administrator of the
# National Aeronautics and Space Administration. All Rights Reserved.
#
# This software is licensed under the terms of the Apache License Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.


# --------------------------------------------------------------------------------------------------


import os
import sys


# --------------------------------------------------------------------------------------------------


def run_os_system_command(command):

    return_code = os.system(command)

    # Check the return code
    if return_code != 0:
        raise Exception(f'Command {command} failed')


# --------------------------------------------------------------------------------------------------


class PackageInstaller():


    # ----------------------------------------------------------------------------------------------


    def __init__(self, package, package_local_name, root, update, clean, verbose, editable):

        # Split package by '/' to get the package name
        self.package_org = package.split('/')[0]
        self.package_name = package.split('/')[1]
        self.package_local_name = package_local_name

        # Root directory that will contain src, core, module files
        self.verbose = verbose
        self.editable = editable

        # Absolute root
        self.root = os.path.abspath(root)

        # Paths where things will go
        self.path_src = os.path.join(root, 'src', self.package_name, self.package_local_name)
        self.path_core = os.path.join(root, 'core', self.package_name, self.package_local_name)
        self.path_mod = os.path.join(root, 'modulefiles', 'core', self.package_name,
                                      f'{self.package_local_name}.lua')

        # Clean option to remove any existing package with this name
        # ----------------------------------------------------------
        if clean:
            print(f'Cleaning up package {self.package_name}/{self.package_local_name}')
            for path in [self.path_src, self.path_core, self.path_mod]:
                if os.path.isdir(path):
                    if self.verbose:
                        print(f'Removing {path}')
                    run_os_system_command(f'rm -rf {path}')
            exit(0)

        # If update make sure that the package is already cloned and lua file exists
        # --------------------------------------------------------------------------
        if update:
            if not os.path.isdir(self.path_src):
                raise Exception(f'Package {self.package_name} not cloned. Cannot update.')
            if not os.path.isfile(self.path_mod):
                raise Exception(f'Package {self.package_name} lua file not present. Cannot update.')


    # ----------------------------------------------------------------------------------------------


    def clone(self, branch):

        # Check if package is already cloned and if so do not clone again
        if os.path.isdir(self.path_src):
            print(f'Package {self.package_name} is already cloned. Continuing')
            return

        # Remote location of package (could be relaxed to non GitHub later)
        package_remote_location = f'https://github.com/{self.package_org}/{self.package_name}.git'

        # Set branch
        branch_command = ''
        if branch is not None:
            branch_command = f' --branch {branch}'

        # Clone command
        clone_command = f'git clone {branch_command} {package_remote_location} {self.path_src}'

        # Print message if verbose
        if self.verbose:
            print(f'Cloning package with: {clone_command}')

        # Perform git clone of package
        run_os_system_command(clone_command)

        # Check if clone was successful
        if not os.path.isdir(self.path_src):
            raise Exception(f'Package {self.package_name} was not cloned successfully')


    # ----------------------------------------------------------------------------------------------


    def pip_install(self):

        # Always perform a clean install
        if os.path.isdir(self.path_core):
            run_os_system_command(f'rm -rf {self.path_core}')

        # Pip options
        pip_options = ''
        if self.editable:
            pip_options = '-e'

        # Check for a requirements.txt file in the package directory
        requirements_file = os.path.join(self.path_src, 'requirements.txt')
        if os.path.isfile(requirements_file):
            pip_options = pip_options + f' -r {requirements_file}'

        print ('pip_options =', pip_options)
        exit()

        # Perform pip install
        install_command = f'pip install --prefix={self.path_core} --no-cache-dir {pip_options} ' + \
                          f'{self.path_src}'

            
        
        # Print message if verbose
        if self.verbose:
            print(f'Installing package with: {install_command}')

        # Perform git clone of package
        run_os_system_command(install_command)


    # ----------------------------------------------------------------------------------------------


    def create_module_file(self):

        # Ensure directory exists
        if not os.path.isdir(os.path.dirname(self.path_mod)):
            os.makedirs(os.path.dirname(self.path_mod))

        # Get Python major/minor
        python_maj_min = ".".join(sys.version.split(".")[:2])

        # Set contents of module file
        module_file_contents = \
        f'help([[\n' + \
        f']])\n' + \
        f'\n' + \
        f'local pkgName    = myModuleName()\n' + \
        f'local pkgVersion = myModuleVersion()\n' + \
        f'local pkgNameVer = myModuleFullName()\n' + \
        f'\n' + \
        f'conflict(pkgName)\n' + \
        f'\n' + \
        f'local opt = "{self.root}"\n' + \
        f'local python_dir = "python{python_maj_min}"\n' + \
        f'\n' + \
        f'local base = pathJoin(opt,"core",pkgNameVer)\n' + \
        f'\n' + \
        f'prepend_path("PATH", pathJoin(base,"bin"))\n' + \
        f'prepend_path("PYTHONPATH", pathJoin(base,"lib",python_dir,"site-packages"))\n' + \
        f'\n' + \
        f'whatis("Name: {self.package_name}")\n' + \
        f'whatis("Version: {self.package_local_name}")\n' + \
        f'whatis("Category: Software")\n'

        # Write module_file_contents to file
        if self.verbose:
            print(f'Writing module file to {self.path_mod}')

        with open(self.path_mod, 'w') as module_file:
            module_file.write(module_file_contents)

        # Print information about how to load the module
        print(f'Package {self.package_name} installed successfully.')
        print(f'You can load the package with:\n')
        print(f'    module use {self.root}/modulefiles/core')
        print(f'    module load {self.package_name}/{self.package_local_name}')
        print(f'\n')


    # ----------------------------------------------------------------------------------------------
