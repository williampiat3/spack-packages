# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Xkblas(CMakePackage):
    """
    XKBlas is a BLAS library for multi-GPUs servers similar to CUBLASXt but with
    higher performances especially when matrix dimensions becomes smaller.
    """

    homepage = "https://gitlab.inria.fr/xkblas"
    url = "https://github.com/williampiat3/xkblas/archive/refs/tags/v0.6.0.tar.gz"

    maintainers("williampiat3")

    license("CeCILL-C", checked_by="Thierry Gautier")
    version("0.6.1",sha256="e038315be4b5d71f25bf2f8bb10f6a7629f06af985a45c09fcfb0f8948565212")
    version("0.6.0", sha256="1e3d6a9f7a09f15cc76d46583843a69e769b68252791dc13460548c4b54212bf")

    variant("mkl", default=False, description="Build with MKL support")
    variant("openblas", default=True, description="Build with OpenBLAS support")
    variant("cuda", default=True, description="Build with CUDA support")
    variant("rocm", default=False, description="Build with ROCm support")
    ## Only for grace hopper GPUs
    variant("unified", default=False, description="Build with unified memory support")
    variant("pkgconfig", default=False, description="Add pkgconfigs")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("hwloc")
    depends_on("intel-oneapi-mkl threads=openmp mpi_family=openmpi +cluster", when="+mkl")
    depends_on("openblas", when="+openblas")
    ## Tested with CUDA 8,9, 11, 12.0.0 and 13.0.1 without success
    ## Only CUDA 12.9.1 works with xkblas 0.6.0 within my limited testing.
    depends_on("cuda@12.9.1", when="+cuda")
    depends_on("rocm", when="+rocm")

    conflicts(
        "+mkl",
        when="+openblas",
        msg="MKL and OpenBLAS support cannot be enabled at the same time.",
    )
    conflicts(
        "+cuda", when="+rocm", msg="CUDA and ROCm support cannot be enabled at the same time."
    )

    def cmake_args(self):
        args = [
            self.define_from_variant("KAAPI_USE_CUDA_RT", "cuda"),
            self.define_from_variant("KAAPI_USE_HIP", "rocm"),
            self.define_from_variant("KAAPI_USE_MKL", "mkl"),
            self.define_from_variant("KAAPI_USE_OPENBLAS", "openblas"),
            self.define_from_variant("ENABLE_KAAPI_UNIFIED", "unified"),
        ]
        if self.spec.satisfies("+openblas"):
            args.append(
                self.define(
                    "BLAS_LIBRARIES", join_path(self.spec["openblas"].prefix.lib, "libopenblas.so")
                )
            )
            args.append(self.define("BLAS_INCLUDE_DIRS", self.spec["openblas"].prefix.include))
        args.append(self.define("KAAPI_BUILD_TESTING", True))
        return args

    @run_after("install", when="+pkgconfig")
    def create_pkgconfig(self):
        """Create unofficial pkgconfig files for xkblas libraries"""
        libdir = join_path(self.prefix, "lib")
        pkg_path = join_path(libdir, "pkgconfig")
        mkdirp(pkg_path)

        with open(join_path(pkg_path, "xkblas.pc"), "w") as f:
            f.write(
                "\n".join(
                    [
                        f"prefix={self.prefix}",
                        "exec_prefix=${prefix}",
                        "includedir=${prefix}/include",
                        "libdir=${exec_prefix}/lib",
                        "",
                        "Name: xkblas",
                        "Description: XKBlas is a BLAS library for multi-GPUs servers",
                        f"Version: {self.version}",
                        "Cflags: -I${includedir}",
                        "Libs: -L${libdir} -lkaapi -lxkblas",
                    ]
                )
            )
