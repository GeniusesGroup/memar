/* For license and copyright information please see the LEGAL file in the code repository */

package org

type SideType uint8

const (
	SideType_Unset SideType = iota
	SideType_First
	SideType_Second
	SideType_Third
	SideType_Witness
	SideType_Arbitrator
	SideType_Expert
)
