#include <filesystem>
#include <iostream>
#include <string>
#include <sys/stat.h>
#include <md5.h>
#include <fstream>
#include <vector>

namespace fs = std::filesystem;

std::string calculateMD5Hash(const std::string& filename) {
    std::ifstream file(filename, std::ifstream::binary | std::ifstream::ate);
    std::string hash;

    if (file.is_open()) {
        size_t fileSize = file.tellg();
        file.seekg(0, std::ifstream::beg);

        std::vector<char> buffer(fileSize);

        file.read(buffer.data(), fileSize);
        file.close();

        unsigned char result[MD5_DIGEST_LENGTH];
        _MD5_H_((unsigned char*)buffer.data(), fileSize, result);

        for (int i = 0; i < MD5_DIGEST_LENGTH; i++) {
            std::stringstream stream;
            stream << std::hex << (int)result[i];
            hash += stream.str();
        }
    }
    return hash;
}

int main()
{
    // Paste the desired path!!!
    std::string path
        = "/home/folder/";

    struct stat sb;

    for (const auto& entry : fs::directory_iterator(path)) {

        std::filesystem::path outfilename = entry.path();
        std::string outfilename_str = outfilename.string();
        const char* path = outfilename_str.c_str();

        if (stat(path, &sb) == 0 && !(sb.st_mode & S_IFDIR)) {
            std::string hash = calculateMD5Hash(outfilename_str); 
            std::cout << path << " " << hash << std::endl;
        }
    }
}
