/* ftell example : getting size of a file */
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <iostream>


/**

https://cs.android.com/android/kernel/superproject/+/common-android-mainline:prebuilts/ndk-r23/sources/third_party/googletest/src/gtest-port.cc;l=1081?q=CapturedStream


*/

using namespace std; // only for test


size_t GetFileSize(FILE* file) {
  fseek(file, 0, SEEK_END);
  cout << "GetFileSize " << endl; // print to stdout
  return static_cast<size_t>(ftell(file));
}

std::string ReadEntireFile(FILE* file) {
  const size_t file_size = GetFileSize(file);

  cout << "file size: "  << file_size << endl;

  char* const buffer = new char[file_size];

  size_t bytes_last_read = 0;  // # of bytes read in the last fread()
  size_t bytes_read = 0;       // # of bytes read so far

  fseek(file, 0, SEEK_SET);

  // Keeps reading the file until we cannot read further or the
  // pre-determined file size is reached.
  do {
    bytes_last_read = fread(buffer+bytes_read, 1, file_size-bytes_read, file);
    bytes_read += bytes_last_read;
  } while (bytes_last_read > 0 && bytes_read < file_size);

  const std::string content(buffer, bytes_read);
  delete[] buffer;

  return content;
}

class CapturedStream {
 public:
  // The ctor redirects the stream to a temporary file.
  explicit CapturedStream(int fd) : fd_(fd), uncaptured_fd_(dup(fd)) {
    char name_template[] = "/tmp/captured_stream.XXXXXX";
    const int captured_fd = mkstemp(name_template);
    filename_ = name_template;
    fflush(nullptr);
    dup2(captured_fd, fd_);
    close(captured_fd);
  }

  ~CapturedStream() {
    cout << "tmp file is " << filename_.c_str() << endl;
    //remove(filename_.c_str());
  }

  std::string GetCapturedString() {

    if (uncaptured_fd_ != -1) {
      // Restores the original stream.
      fflush(nullptr);
      dup2(uncaptured_fd_, fd_);
      close(uncaptured_fd_);
      uncaptured_fd_ = -1;
    }

    FILE* const file = fopen(filename_.c_str(), "r");
    if (file == nullptr) {
      cout << "Failed to open tmp file " << filename_
                        << " for capturing stream.";
    }
    const std::string content = ReadEntireFile(file);
    fclose(file);
    return content;
  }

 private:
  const int fd_;  // A stream to capture.
  int uncaptured_fd_;
  // Name of the temporary file holding the stderr output.
  ::std::string filename_;

};




int main() {
	cout << "start CapturedStream test" << endl; // to stdout
	auto stream = new CapturedStream(STDOUT_FILENO); // bind stdout_no to  tmp file
   	
	cout << "save to tmp file" << endl; // print to tmp file
	
	cout << stream->GetCapturedString() << endl; // restore stdout strem and read tmp file print to stdout
	cout << "release stream" << endl;
	delete stream;
	return 0;
}
