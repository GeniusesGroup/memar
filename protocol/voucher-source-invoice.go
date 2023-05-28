/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// VoucherSourceInvoice indicate the domain record data fields.
type VoucherSourceInvoice interface {
	VoucherID() VoucherUUID                 //
	InvoiceID() InvoiceUUID                 //
	InvoiceType() VoucherSourceInvoice_Type //
	Time() protocol.Time                    // save time
	RequestID() urp.UserRequestUUID         //
}

type VoucherSourceInvoice_StorageServices interface {
	Save(vsi VoucherSourceInvoice) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID VoucherUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID VoucherUUID, vo protocol.VersionOffset) (vsi VoucherSourceInvoice, nv protocol.NumberOfVersion, err protocol.Error)

	FindByInvoice(invoiceID InvoiceUUID, offset, limit uint64) (voucherIDs []VoucherUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type VoucherSourceInvoice_Type uint8

const (
	VoucherSourceInvoice_Type_Unset VoucherSourceInvoice_Type = iota
	VoucherSourceInvoice_Type_PastCompleted
	VoucherSourceInvoice_Type_HurryToBuying
	VoucherSourceInvoice_Type_BackToBuy
)
