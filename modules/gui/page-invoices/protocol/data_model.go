/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	time_p "memar/time/protocol"
	invoice_p "org/modules/economics/invoice/protocol"
	pos_p "org/modules/economics/pos/protocol"
	product_p "org/modules/economics/product/protocol"
	user_p "org/modules/identity/user/protocol"
	label_p "org/modules/knowledge/label/protocol"
	estate_p "org/modules/rights/estate/protocol"
)

// /invoices?time=20,21&user=123
type Invoices_GUI_Page_Conditions interface {
	Time() (start, end time_p.Time)
	user_p.Field_UserUUID
	product_p.Field_ProductID // inner filter like in stock product
	label_p.Field_LabelsUUID
	invoice_p.Field_InvoiceID
	pos_p.Field_PosID
	label_p.Field_LabelsUUID
	Discount() // inner filters like percent discount
	estate_p.Field_EstateID

	// Pagination
}

type Invoices_GUI_Page_Services interface {
	New()

	Filter()
	Print()

	ChangeDefaultSettings() // e.g. startup default data
}

type TimeHelper interface {
	// PastTimeByNow(past Day) (start, end time_p.Time)
}
