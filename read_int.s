.section .text
.globl read_int
.type read_int, @function
read_char:
	pushl %ebp
	movl %esp, %ebp
	subl $5, %esp
	movl $3, %eax
	movl $0, %ebx
	movl -5(%ebp), %ecx
	movl $5, %edx
	int $0x80
	incl [%ebp-4]
	movl %eax,-5(%ebp)
	movl %ebp, %esp
	popl %ebp
	ret 