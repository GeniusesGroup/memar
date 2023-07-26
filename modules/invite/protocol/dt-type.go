/* For license and copyright information please see the LEGAL file in the code repository */

package ip

type Type uint32

const (
	Type_Unset Type = 0
	Type_      Type = (1 << iota)
	Type_WaitList
)
