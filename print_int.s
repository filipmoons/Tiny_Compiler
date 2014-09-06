.section .text
.globl print_int
.type print_int, @function
print_int:
	pushl %ebp
	movl %esp, %ebp
	.equ value, 8
	.equ base, -4
	pushl $10 
	.equ bufsize, -8
	pushl $1 
	.equ negative, -12
	pushl $0 
	pushl $10 
	movl value(%ebp), %eax
	jge .K1 
	movl $1, negative(%ebp)
	negl %eax
.K1:
	cdq
	divl base(%ebp)
	pushl %edx
	addl $48, (%esp)
	incl bufsize(%ebp)
	cmpl $0, %eax
	jne .K1
	cmpl $0, negative(%ebp)
	je .K2
	pushl $45
	incl bufsize(%ebp)
.K2:
	movl $4, %eax 
	movl $1, %ebx 
	movl %esp, %ecx 
	movl $4, %edx
	imul bufsize(%ebp), %edx
	int $0x80
	movl %ebp, %esp
	popl %ebp
	ret
