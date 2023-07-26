/* For license and copyright information please see the LEGAL file in the code repository */

package pp

type Type uint8

const (
	Type_Unset            Type = 0
	Type_CustomProduction Type = (1 << iota)
	Type_MassProduction
)
