# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyPlaid(PythonPackage):
    """FIXME: Put a proper description of your package here."""
    homepage = "https://github.com/PLAID-lib/plaid"
    pypi = "pyplaid/pyplaid-0.1.15.tar.gz"

    maintainers("williampiat3", "casenave", "bstaber")


    license("MIT", checked_by="casenave")

    version("0.1.15", sha256="e596ee155804da31793af0ee8f0e93c5fe629e246cbdca87dcae741a1e1f1205")

    with default_args(type="build"):
        depends_on("py-setuptools@:76.1.0")
        depends_on("py-setuptools-scm")


    # FIXME: Add additional dependencies if required.
    with default_args(type=("build","run")):
        depends_on("python@:3.13")
        depends_on("py-pyyaml")
        depends_on("py-pycgns")
        depends_on("py-zarr")
        depends_on("py-scikit-learn")
        depends_on("py-datasets")
        depends_on("py-numpy")
        depends_on("py-matplotlib")
        depends_on("py-pydantic")

