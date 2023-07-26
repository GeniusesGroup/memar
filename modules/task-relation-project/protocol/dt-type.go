/* For license and copyright information please see the LEGAL file in the code repository */

package trpp

type Type uint32

const (
	Type_Unset Type = 0

	Type_Blocking Type = (1 << iota) // stuck
	Type_Move                        // move from other project

	Type_Parent
	Type_
)
