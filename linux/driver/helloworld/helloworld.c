#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>

static int __init helloworld_init(void) {
    printk("helloworld_init\n");
    return 0;
}

static void __exit helloworld_exit(void) {
    printk("helloworld_exit\n");
}

module_init(helloworld_init);
module_exit(helloworld_exit);

MODULE_AUTHOR("Your Name");
MODULE_DESCRIPTION("More: https://github.com/Sunrisepeak/HelloWorld");
MODULE_LICENSE("GPL");