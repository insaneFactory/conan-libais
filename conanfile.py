from conans import ConanFile, CMake, tools


class LibaisConan(ConanFile):
    name = "libais"
    version = "0.15"
    license = "Beerware"
    author = "Manuel Freiholz"
    url = "https://github.com/insaneFactory/conan-libais"
    description = ""
    topics = ("ais", "nmea")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True
    }
    build_requires = "cmake_installer/3.12.1@conan/stable"
    generators = "cmake"

    def configure(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.run("git clone https://github.com/schwehr/libais.git")
        self.run("cd libais && git fetch --all --tags --prune && git checkout tags/v" + self.version)

        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("libais/CMakeLists.txt", "project (libais)",
                              '''project (libais)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="libais")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*ais.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["ais"]

