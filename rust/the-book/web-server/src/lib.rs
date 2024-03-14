use std::thread;
use std::sync::mpsc;
use std::sync::{Arc, Mutex};

/*
enum Status {
    Running,
    Stoped,
}
*/

pub struct Worker {
    id: usize,
    //status: Arc<Mutex<Status>>,
    // use Option for take thread and release
    thread: Option<thread::JoinHandle<()>>,
}

type Task = Box<dyn FnOnce() + Send>;

impl Worker {
    pub fn new(id: usize, rx: Arc<Mutex<mpsc::Receiver<Task>>>) -> Worker {
        
        //if let status = Arc::new(Mutex::new(Status::Running));

        let thread = thread::spawn(move || {
            println!("worker {} start", id);
            //let mut status = Status::Running;
            //while status == Status::Running

            loop {
                // return Option<> == None when sender droped
                // block rx - api
                let task_result = rx.lock().unwrap().recv();

                if let Ok(task) = task_result {
                    println!("Worker {id}: task start...");
                    task();
                    println!("Worker {id}: task end");
                } else {
                    println!("Worker {id} disconnected; shutting down.");
                    // rx: Arc<...> auto release
                    break;
                }

            }
        });

        Worker {
            id: id,
            //status: status,
            thread: Some(thread),
        }
    }
}

pub struct ThreadPool {
    workers: Vec<Worker>,
    // use Option for take sender(moved) and release
    sender: Option<mpsc::Sender<Task>>,
}

impl ThreadPool {
    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let mut workers = Vec::with_capacity(size);
        let (sender, rx) = mpsc::channel();
        let receiver = Arc::new(Mutex::new(rx));
        for i in 0..size {
            workers.push(Worker::new(i, Arc::clone(&receiver)));
        }

        ThreadPool{ workers, sender: Some(sender) }
    }

    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        self.sender.as_ref().unwrap().send(Box::new(f)).unwrap();
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {

        // disconnect channel, and release
        // Arc<rx> auto release
        drop(self.sender.take());

        for worker in &mut self.workers {
            println!("Shutting down worker {}", worker.id);

            if let Some(thread)  = worker.thread.take() {
                thread.join().unwrap();
            }
        }
    }
}