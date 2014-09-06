.section .text
.globl read_char
.type read_char, @function
read_char:
	pushl %ebp
	movl %esp, %ebp
	subl $1, %esp
	movl $3, %eax
	movl $0, %ebx
	movl -1(%ebp), %ecx
	movl $1, %edx
	int $0x80
	movl %eax,-1(%ebp)
	movl %ebp, %esp
	popl %ebp
	ret 