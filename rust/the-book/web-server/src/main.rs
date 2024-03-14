use std::{
    fs,
    io::{prelude::*, BufReader},
    net::{TcpListener, TcpStream},
    thread,
    time::Duration,
};

use webserver;

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    println!("webserver: 127.0.0.1:7878");

    let thread_pool = webserver::ThreadPool::new(3);

    for stream in listener.incoming().take(2) {
        let stream = stream.unwrap();

        thread_pool.execute(|| handle_connection(stream));
    }
}

fn handle_connection(mut stream: TcpStream) {

    println!("handle_connection start");

    let buf_reader = BufReader::new(&mut stream);

    let request_line = buf_reader.lines().next().unwrap().unwrap();

    let (status_line, filename) = match &request_line[..] {
        "GET / HTTP/1.1" => ("HTTP/1.1 200 OK", "hello.html"),
        "GET /sleep HTTP/1.1" => {
            thread::sleep(Duration::from_secs(5));
            ("HTTP/1.1 200 OK", "hello.html")
        }
        _ => ("HTTP/1.1 404 NOT FOUND", "404.html"),
    };

    let contents = fs::read_to_string(filename).unwrap();
    let length = contents.len();

    let response =
        format!("{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}");


    println!("response -> ");

    stream.write_all(response.as_bytes()).unwrap();
    stream.flush().unwrap();

    println!("handle_connection end");
}


/*

webserver: 127.0.0.1:7878
worker 0 start
worker 2 start
worker 1 start

Worker 0: task start...
handle_connection start
    Worker 2: task start...
    handle_connection start
response ->
handle_connection end
Worker 0: task end

        Worker 1: task start...
        handle_connection start
    response ->
    handle_connection end
    Worker 2: task end

// block query
// buf_reader.lines().next().unwrap().unwrap();
// TODO: request issue
Worker 2: task start...
handle_connection start
Worker 0: task start...
handle_connection start
response -> 
handle_connection end
  ~5min
Worker 2: task end
thread '<unnamed>' panicked at src/main.rs:31:50:
called `Option::unwrap()` on a `None` value
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace

webserver: 127.0.0.1:7878
worker 0 start
worker 1 start
worker 2 start
Worker 0: task start...
handle_connection start
Shutting down worker 0
Worker 1: task start...
Worker 2 disconnected; shutting down.
handle_connection start
response -> 
handle_connection end
Worker 0: task end
Worker 0 disconnected; shutting down.
Shutting down worker 1


thread '<unnamed>' panicked at src/main.rs:31:50:
called `Option::unwrap()` on a `None` value
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
thread 'main' panicked at src/lib.rs:96:31:
called `Result::unwrap()` on an `Err` value: Any { .. }

// when listener.incoming().take(2)
webserver: 127.0.0.1:7878
worker 1 start
worker 0 start
worker 2 start
Worker 1: task start...
handle_connection start
Shutting down worker 0
Worker 0: task start...
handle_connection start
Worker 2 disconnected; shutting down.
response -> 
handle_connection end
Worker 1: task end
Worker 1 disconnected; shutting down.
response -> 
handle_connection end
Worker 0: task end
Worker 0 disconnected; shutting down.
Shutting down worker 1
Shutting down worker 2

*/