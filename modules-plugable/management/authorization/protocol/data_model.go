/* For license and copyright information please see the LEGAL file in the code repository */

package group_authorization

// DataModel indicate the domain record data fields.
type DataModel interface {
	GetPolicy() Policy // Visibility level
	SetPolicy() Policy
}
