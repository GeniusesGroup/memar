/* For license and copyright information please see the LEGAL file in the code repository */

package emp

// Type is education unit type
type Type uint8

const (
	Type_Unset Type = iota
	Type_OrganizationStaff
	Type_SelfStatement
	Type_UsersVote
	Type_AI
)
