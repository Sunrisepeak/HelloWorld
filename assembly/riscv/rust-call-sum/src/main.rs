#![no_std]  // 禁用标准库
#![no_main] // 关闭main为程序入口函数

extern crate tinysyscall;

use core::{arch::global_asm};

global_asm!(include_str!("sum.s"));

fn method1() {
    let mut result: usize;

    unsafe { // call sum
        core::arch::asm!(
            "li a0, 4",
            "jal ra, sum",
            out("a0") result,
        );
    }

    for i in 0..result {
        tinysyscall::file::write(
            tinysyscall::file::STDOUT,
            &[
                48 + i as u8,
                '\n' as u8
            ]
        );
    }

}

fn method2() {
    let n = 4usize;
    let result: usize;

    unsafe {
        core::arch::asm!(
            "jal sum", // call sum
            inlateout("a0") n => result,
        );
    }

    for i in 0..result {
        tinysyscall::file::write(
            tinysyscall::file::STDOUT,
            &[
                48 + i as u8,
                '\n' as u8
            ]
        );
    }

}

#[no_mangle]
extern fn _start() {
    tinysyscall::hello();

    method2();
    tinysyscall::file::write(1, "\n".as_bytes());
    method1();

    tinysyscall::process::exit(0);
}