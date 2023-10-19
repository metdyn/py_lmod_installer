# (C) Copyright 2021- United States Government as represented by the Administrator of the
# National Aeronautics and Space Administration. All Rights Reserved.
#
# This software is licensed under the terms of the Apache License Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.


# --------------------------------------------------------------------------------------------------


import argparse

from py_lmod_installer.package_installer import PackageInstaller


# --------------------------------------------------------------------------------------------------


package_help = 'Package to install, e.g. GEOS-ESM/swell or JCSDA-internal/eva'
package_local_name_help = 'Name of the package referred to locally. Once installed you will do ' \
                          'module load <package_name>/<package_local_name>'
branch_help = 'Specific branch to checkout of the package'
root_help = 'Root directory for source, install and modules files'
clean_help = 'Clean up any previous installation of the package '
verbose_help = 'Verbose output'


# --------------------------------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Python installer package")

    # Define the 'package' argument with choices.
    parser.add_argument('package', help=package_help)

    # Define the local name for the package argument with choices.
    parser.add_argument('package_local_name', help=package_local_name_help)

    # Define the '-b' or '--branch' option with a default value.
    parser.add_argument('-b', '--branch', default=None, help=branch_help)

    # Define the '-r' or '--root' option with a default value.
    parser.add_argument('-r', '--root', default='./', help=root_help)

    # Define the '-c' or '--clean' option as a flag.
    parser.add_argument('-c', '--clean', action='store_true', help=clean_help)

    # Define the '-v' or '--verbose' option as a flag.
    parser.add_argument('-v', '--verbose', action='store_true', help=verbose_help)

    args = parser.parse_args()

    # Access the arguments and options
    package = args.package
    package_local_name = args.package_local_name
    branch = args.branch
    root = args.root
    clean = args.clean
    verbose = args.verbose

    # Create the package installer object
    package_installer = PackageInstaller(package, package_local_name, root, clean, verbose)

    # Clone the repo
    package_installer.clone(branch)

    # Install package
    package_installer.pip_install()

    # Create module file
    package_installer.create_module_file()


# --------------------------------------------------------------------------------------------------
