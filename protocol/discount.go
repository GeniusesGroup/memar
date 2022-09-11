/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// Discount indicate the domain record data fields.
// Discount or product-auction to reduce invoices price automatically by some rules know also as sales, ...
type Discount interface {
	DiscountID() [16]byte       //
	Type() Discount_Type        //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type Discount_StorageServices interface {
	Save(d Discount) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID [16]byte, vo protocol.VersionOffset) (d Discount, nv protocol.NumberOfVersion, err protocol.Error)
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
