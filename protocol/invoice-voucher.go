/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// InvoiceVoucher indicate the domain record data fields.
// This domain will let users redeem their vouchers and track vouchers rules.
type InvoiceVoucher interface {
	InvoiceID() InvoiceUUID           //
	VoucherID() VoucherUUID           //
	Discounted() protocol.MoneyAmount //
	Time() protocol.Time              // save time
	RequestID() urp.UserRequestUUID   //
}

type InvoiceVoucher_StorageServices interface {
	Save(dm InvoiceVoucher) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID InvoiceUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID InvoiceUUID, vo protocol.VersionOffset) (dm InvoiceVoucher, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_InvoiceIDs_BY_VoucherID(voucherID VoucherUUID, offset, limit uint64) (invoiceIDs []InvoiceUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}
