/* For license and copyright information please see the LEGAL file in the code repository */

package bsrp

type Type uint8

const (
	Type_Unset Type = iota
	Type_withdrawal
	Type_Deposit
	Type_Suggester
)
