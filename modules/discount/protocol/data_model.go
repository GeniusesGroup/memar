/* For license and copyright information please see the LEGAL file in the code repository */

package dp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel or product-auction to reduce invoices price automatically by some rules know also as sales, ...
type DataModel interface {
	DiscountID() DiscountUUID       //
	Type() Type                     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint32

const (
	Type_Unset Type = 0
	Type_Area  Type = (1 << iota)
	Type_Campaign
	Type_Category
	Type_Group
	Type_Invoice
	Type_Location
	// Type_Owner
	Type_POS
	Type_Product
	Type_TimeValidity
	Type_Timing
	Type_Usage    // limit to usage number
	Type_UserType // limit to user type
	Type_User     // limit to specific users
	// Type_
)

type Discount_GUI_Page_Services interface {
}
