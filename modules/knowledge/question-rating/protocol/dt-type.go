/* For license and copyright information please see the LEGAL file in the code repository */

package qrp

type Type uint16

const (
	Type_Unset             Type = 0
	Type_LikertScale_Emoji Type = (1 << iota)
	Type_LikertScale_Color
	Type_LikertScale_Range // bipolar scale
	Type_Star
	Type_Number
	Type_Text
	Type_Label

	Type_ForceToFill
	Type_ForceToContinue
)
