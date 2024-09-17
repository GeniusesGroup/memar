/* For license and copyright information please see the LEGAL file in the code repository */

package dp

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
