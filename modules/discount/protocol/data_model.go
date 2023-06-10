/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type DiscountUUID = protocol.UUID

// Discount indicate the domain record data fields.
// Discount or product-auction to reduce invoices price automatically by some rules know also as sales, ...
type Discount interface {
	DiscountID() DiscountUUID       //
	Type() Discount_Type            //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type Discount_StorageServices interface {
	Save(dm Discount) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID DiscountUUID, vo protocol.VersionOffset) (dm Discount, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_DiscountIDs_BY_Type(t Discount_Type, offset, limit uint64) (discountIDs []DiscountUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type Discount_Type uint32

const (
	Discount_Type_Unset Discount_Type = 0
	Discount_Type_Area  Discount_Type = (1 << iota)
	Discount_Type_Campaign
	Discount_Type_Category
	Discount_Type_Group
	Discount_Type_Invoice
	Discount_Type_Location
	// Discount_Type_Owner
	Discount_Type_POS
	Discount_Type_Product
	Discount_Type_TimeValidity
	Discount_Type_Timing
	Discount_Type_Usage    // limit to usage number
	Discount_Type_UserType // limit to user type
	Discount_Type_User     // limit to specific users
	// Discount_Type_
)

type Discount_GUI_Page_Services interface {
}
