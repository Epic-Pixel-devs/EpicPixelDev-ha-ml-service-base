# -*- coding: utf-8 -*-

from pip._internal.operations import freeze

if __name__ == '__main__':
    packages = []
    with open('unrequirements.txt', 'r') as file:
        ignores = file.readlines()
        pkgs = freeze.freeze()

        for pkg in pkgs:
            if pkg not in ignores:
                packages.append(f'{pkg}\n')
    file.close()

    with open('requirements.txt', 'w') as file:
        file.writelines(packages, )

    file.close()
