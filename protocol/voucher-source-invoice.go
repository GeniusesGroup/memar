/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// VoucherSourceInvoice indicate the domain record data fields.
type VoucherSourceInvoice interface {
	VoucherID() [16]byte                    // voucher domain
	InvoiceID() [16]byte                    // invoice domain
	InvoiceType() VoucherSourceInvoice_Type //
	Time() protocol.Time                    // save time
	RequestID() UserRequestUUID             // user-request domain
}

type VoucherSourceInvoice_StorageServices interface {
	Save(vsi VoucherSourceInvoice) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID [16]byte, vo protocol.VersionOffset) (vsi VoucherSourceInvoice, nv protocol.NumberOfVersion, err protocol.Error)

	FindByInvoice(invoiceID [16]byte, offset, limit uint64) (voucherIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

type VoucherSourceInvoice_Type uint8

const (
	VoucherSourceInvoice_Type_Unset VoucherSourceInvoice_Type = iota
	VoucherSourceInvoice_Type_PastCompleted
	VoucherSourceInvoice_Type_HurryToBuying
	VoucherSourceInvoice_Type_BackToBuy
)
