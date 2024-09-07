/* For license and copyright information please see the LEGAL file in the code repository */

package tax_p

type Type uint8

const (
	Type_Unset Type = iota

	// VAT as Value-Added-Tax is bad name for a robbery!
	Type_VAT
)
