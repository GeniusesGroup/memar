/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// InvoiceItemTime indicate the domain record data fields.
type InvoiceItemTime interface {
	InvoiceID() [16]byte        // invoice domain
	ProductID() [16]byte        // product domain
	Type() InvoiceItemTime_Type //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type InvoiceItemTime_StorageServices interface {
	Save(iit InvoiceItemTime) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID [16]byte, vo protocol.VersionOffset) (iit InvoiceItemTime, err protocol.Error)
}

type InvoiceItemTime_Type uint8

const (
	InvoiceItemTime_Type_Unset InvoiceItemTime_Type = iota
	InvoiceItemTime_Type_Enter
	InvoiceItemTime_Type_Exit
	InvoiceItemTime_Type_ManualEnter
	InvoiceItemTime_Type_ManualExit
	InvoiceItemTime_Type_Start
	InvoiceItemTime_Type_End
)
