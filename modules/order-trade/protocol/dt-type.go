/* For license and copyright information please see the LEGAL file in the code repository */

package otp

type Type uint8

const (
	Type_Unset Type = iota
	// stop-loss orders guarantee execution
	Type_StopLoss
	// stop-limit orders guarantee price
	Type_StopLimit
)
