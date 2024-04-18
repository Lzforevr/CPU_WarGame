#include "libkdump/libkdump.h"
#include <stdio.h>
#include <stdlib.h>

#define MAX_BUFFER_SIZE 1024

int main(int argc, char *argv[]) {
    size_t phys;
    if (argc < 2) {
        printf("Usage: %s <physical address> [<direct physical map>]\n", argv[0]);
        return 0;
    }

    phys = strtoull(argv[1], NULL, 0);

    libkdump_config_t config;
    config = libkdump_get_autoconfig();
    if (argc > 2) {
        config.physical_offset = strtoull(argv[2], NULL, 0);
    }

    libkdump_init(config);

    size_t vaddr = libkdump_phys_to_virt(phys);

    printf("\x1b[32;1m[+]\x1b[0m Physical address       : \x1b[33;1m0x%zx\x1b[0m\n", phys);
    printf("\x1b[32;1m[+]\x1b[0m Physical offset        : \x1b[33;1m0x%zx\x1b[0m\n", config.physical_offset);
    printf("\x1b[32;1m[+]\x1b[0m Reading virtual address: \x1b[33;1m0x%zx\x1b[0m\n\n", vaddr);

    // 初始化缓冲区和变量
    char buffer[MAX_BUFFER_SIZE] = {0};
    int last_value = -1;
    size_t buffer_index = 0;

    while (1) {
        int value = libkdump_read(vaddr);
        // 当读取到的值不再更新时（这里假设不变为0）结束循环
        if (value == 0 || value == last_value) {
            break;
        }
        last_value = value;

        // 添加当前值到缓冲区
        if (buffer_index < MAX_BUFFER_SIZE - 1) {
            buffer[buffer_index++] = value;
        } else {
            printf("\x1b[31;1m[!]\x1b[0m Buffer overflow, stopping read.\n");
            break;
        }

        vaddr++;
    }

    // 将缓冲区末尾置零以确保字符串正确终止
    buffer[buffer_index] = '\0';

    libkdump_cleanup();

    return 0;
}
