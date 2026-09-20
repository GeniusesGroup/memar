/* For license and copyright information please see the LEGAL file in the code repository */

package ig_p

type Type uint32

const (
	Type_Unset      Type = 0
	Type_1st_Friend Type = (1 << iota)
	Type_2st_Friend
	Type_3st_Friend
	Type_4st_Friend
	Type_5st_Friend
	Type_6st_Friend
	Type_Family
	// Type_
)
