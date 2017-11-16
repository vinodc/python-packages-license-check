#!/usr/bin/env python
import pkg_resources
import argparse
import sys

from pip.utils import get_installed_distributions


def main():
    parser = argparse.ArgumentParser(
        description=("Read all installed packages from sys.path and list"
                     " licenses."))
    args = parser.parse_args()

    meta_files_to_check = ['PKG-INFO', 'METADATA']

    for installed_distribution in get_installed_distributions():
        project_name = installed_distribution.project_name

        licenses = []
        for metafile in meta_files_to_check:
            if not installed_distribution.has_metadata(metafile):
                continue
            for line in installed_distribution.get_metadata_lines(metafile):
                _license = None
                if 'License: ' in line:
                    _license = line.split(': ', 1)[1]
                elif 'Classifier: License :: ' in line:
                    _license = line.rsplit(' :: ', 1)[1]
                if _license:
                    _license = _license.upper().strip()
                    if _license not in licenses:
                        licenses.append(_license)

        ignore = ['GPL', 'UNKNOWN', 'GENERAL PUBLIC LICENSE']
        filtered = []
        for l in licenses:
            for i in ignore:
                if i in l:
                    break
            else:
                filtered.append(l)
        if len(filtered) > 0:
            licenses = filtered

        sys.stdout.write("{project_name}: {license}\n".format(
            project_name=project_name,
            license=' | '.join(licenses)))
        if not licenses:
            sys.stdout.write(
                "{project_name}: Found no license information.\n".format(
                project_name=installed_distribution.project_name))

if __name__ == "__main__":
    main()
