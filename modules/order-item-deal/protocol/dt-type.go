/* For license and copyright information please see the LEGAL file in the code repository */

package oidp

type Type uint8

const (
	OrderAmount_Type_Unset   Type = iota
	OrderAmount_Type_Regular      // order-price rules
	OrderAmount_Type_Trade        // order-trade rules
	// Whole order must be filled for matching deal or order must cancelled on timeout
	// If this flag absent, allow matching engine to deal part of order.
	// https://en.wikipedia.org/wiki/Immediate_or_cancel
	// https://en.wikipedia.org/wiki/All_or_none
	// https://en.wikipedia.org/wiki/Fill_or_kill
	OrderAmount_Type_MustFill
)
