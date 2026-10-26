// For license and copyright information please see the LEGAL file in the code repository

// func activeCoreID() uint64
TEXT ·activeCoreID(SB),7,$0
	MOVQ $0xB,AX
	XORQ CX,CX
	CPUID
	MOVQ DX,ret+0(FP)
	RET
