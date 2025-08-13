#include <mutex>
#include <thread>
#include <iostream>
#include <ostream>

int main(int argc, char** argv) {
    std::mutex m;
    std::cout << "Main locking." << std::endl; 
    m.lock();
    std::cout << "Main locked." << std::endl; 
    std::thread t([&]() {
        std::cout << "Thread created." << std::endl; 
        std::lock_guard<std::mutex> l(m);
        std::cout << "Thread closing." << std::endl; 
    });
    std::this_thread::sleep_for(std::chrono::milliseconds(5000));
    m.unlock();
    std::cout << "Main unlocked." << std::endl; 
    std::cout << "Joining." << std::endl; 
    t.join();
    return 0;
}