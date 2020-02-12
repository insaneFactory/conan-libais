from conans import ConanFile, CMake, tools


class LibaisConan(ConanFile):
    name = "libais"
    version = "0.0"
    license = "Beerware"
    author = "Manuel Freiholz (https://mfreiholz.de)"
    url = "https://github.com/insaneFactory/conan-libais"
    description = "Library to parse AIS responder messages."
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
    build_requires = (
        "cmake_installer/3.15.5@conan/stable"
    )
    generators = "cmake"
    exports_sources = "CMakeLists.txt"

    def configure(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.run("git clone https://github.com/schwehr/libais.git")
        #self.run("cd libais && git fetch --all --tags --prune && git checkout tags/v" + self.version)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="libais/src/libais")
        self.copy("*ais.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["ais"]

