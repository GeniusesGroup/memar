/* For license and copyright information please see the LEGAL file in the code repository */

package qop

type Type uint16

const (
	Type_Unset    Type = 0
	Type_DropList Type = (1 << iota)
)
