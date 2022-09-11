/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// FinancialTransactionOrder indicate the domain record data fields.
type FinancialTransactionOrder interface {
	FinancialTransactionOrderID() [16]byte //
	UserID() protocol.UserID               // user domain
	ReferenceID() [16]byte                 // Other Platform transaction ID e.g. bank
	PlatformID() [4]byte                   // Detect to||from Currency
	Amount() float64                       //
	SuggestPrice() float64                 //
	Time() protocol.Time                   // save time
	RequestID() UserRequestUUID            // user-request domain
}
