/* For license and copyright information please see the LEGAL file in the code repository */

package ip

import (
	vp "org/modules/voucher/protocol"
)

// Also usually known as shopping-cart, ... in GUI part of applications

// New invoice service

// delete invoice service : This state indicates that the invoice has been deleted.
// You can only delete an invoice in the draft state and not in any other state.

// GetIDsByDateTime(time protocol.Time, offset, limit uint64) (ids [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

type Invoice_GUI_Page_Conditions interface {
	ID()

	// /invoice?status=new
	State() // show/edit/new

}

// /invoice-pay?id=123
type Invoice_GUI_Page_Services interface {
	new()
	edit() // change invoice status
	close()
	save()
	saveAndClose()

	addItemByProductID()
	editItem(rowID uint32)
	removeItem(rowID uint32)
	increaseItemNumber()
	decreaseItemNumber()

	addVoucher(vID vp.VoucherUUID)

	paid(amount int64, method uint8) // method:cash, card, internet, ...

	print()
	changePrintSettings()
}
