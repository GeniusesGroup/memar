/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"memar/protocol"
)

// /invoices?time=20,21&user=123
type Invoices_GUI_Page_Conditions interface {
	Time() (start, end protocol.Time)
	UserID()
	Product() // inner filter like in stock product
	Category()
	InvoiceID()
	PosID()
	Status()
	Discount() // inner filters like percent discount
	Estate()

	// Pagination
}

type Invoices_GUI_Page_Services interface {
	New()

	Filter()
	Print()

	ChangeDefaultSettings() // e.g. startup default data
}

type TimeHelper interface {
	// PastTimeByNow(past Day) (start, end protocol.Time)
}
