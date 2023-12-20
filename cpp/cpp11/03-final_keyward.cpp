// g++ -std=c++11  03-final_keyward.cpp


// 基本语法
struct A {
    virtual void func1() final { }
    virtual void func2() = 0;
};

struct B final { };

struct C final : public A {
    // void func1() override { } // error
    void func2() final override { }
    //void func2() override final { }
};

// error
//struct D : public B { };
//struct E : public C { };

#include <iostream>
#include <string>

class AudioPlayInterface {
protected:
    AudioPlayInterface(std::string format) : _mFormat { format } { }

public:
    virtual void play() final {
        std::cout << "AudioPlayInterface: start -> " << _mFormat  << std::endl;
        _init();
        _config();
        _startPlay();
        _deinit();
        std::cout << "AudioPlayInterface: end..." << std::endl << std::endl;
    }
protected:
    virtual void _init() = 0;
    virtual void _config() = 0;
    virtual void _startPlay() = 0;
    virtual void _deinit() = 0;

protected:
    std::string _mFormat;
    // other data
};

class WAVPlay final : public AudioPlayInterface {

public:
    WAVPlay() : AudioPlayInterface("WAV") {
        // ...
    }

protected:
    void _init() override {
        std::cout << "WAVPlay: _init" << std::endl;
    }

    void _config() override {
        std::cout << "WAVPlay: _config" << std::endl;
    }

    void _startPlay() override {
        std::cout << "WAVPlay: _startPlay" << std::endl;
    }

    void _deinit() override {
        std::cout << "WAVPlay: _deinit" << std::endl;
    }


};

class MP3Play final : public AudioPlayInterface {

public:
    MP3Play() : AudioPlayInterface("MP3") {
        // ...
    }

protected:
    void _init() override {
        std::cout << "MP3Play: _init" << std::endl;
    }

    void _config() override {
        std::cout << "MP3Play: _config" << std::endl;
    }

    void _startPlay() override {
        std::cout << "MP3Play: _startPlay" << std::endl;
    }

    void _deinit() override {
        std::cout << "MP3Play: _deinit" << std::endl;
    }
};

int main() {

    AudioPlayInterface *wav = new WAVPlay();
    AudioPlayInterface *mp3 = new MP3Play();

    wav->play();
    mp3->play();

    delete wav;
    delete mp3;

    return 0;
}