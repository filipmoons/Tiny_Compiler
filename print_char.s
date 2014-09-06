.section .text
.globl print_char
.type print_char, @function
print_char:
	pushl %ebp
	movl %esp, %ebp
	movl $1, %edx
	movl 1(%ebp), %ecx
	movl $1, %ebx
	movl $4, %eax
	int $0x80
	movl %ebp, %esp
	popl %ebp
	ret
