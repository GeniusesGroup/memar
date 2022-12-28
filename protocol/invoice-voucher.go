/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// InvoiceVoucher indicate the domain record data fields.
// This domain will let users redeem their vouchers and track vouchers rules.
type InvoiceVoucher interface {
	InvoiceID() InvoiceUUID           //
	VoucherID() [16]byte              // voucher domain
	Discounted() protocol.MoneyAmount //
	Time() protocol.Time              // save time
	RequestID() UserRequestUUID       // user-request domain
}

type InvoiceVoucher_StorageServices interface {
	Save(iv InvoiceVoucher) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID [16]byte, vo protocol.VersionOffset) (iv InvoiceVoucher, nv protocol.NumberOfVersion, err protocol.Error)

	FindByVoucherID(voucherID [16]byte, offset, limit uint64) (invoiceIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}
