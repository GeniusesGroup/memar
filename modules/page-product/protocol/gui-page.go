/* For license and copyright information please see the LEGAL file in the code repository */

package upp

import (
	pp "org/modules/product/protocol"
)

// /product?new
// /product?pid=ppppp
// /product/new

// /product/admin/new
// /product/admin?edit

// /product/new
// /product?edit&pid=pppppppppp

type GUI_Page_UsedDomains interface {
	// Product
	// Staff
	// Content
	// User
	// Group
	// Quiddity
}

type GUI_Page_HyperLinks interface {
}

type GUI_Page_Conditions interface {
	ProductID() pp.ProductUUID //

	Editable() bool
}

type GUI_Page_Service interface {
	ChangeViewLayout()
	// Block()
	Report()

	SetNotifyType(nt Notify_Type)
}

type Notify_Type uint8

const (
	Notify_Type_Unset Notify_Type = iota
	Notify_Type_Casual
	Notify_Type_All
	Notify_Type_Mute
)
