/* For license and copyright information please see the LEGAL file in the code repository */

package oidp

type SideType uint8

const (
	SideType_Unset SideType = iota
	SideType_Buy
	SideType_Sell
	// OrderItemDetail_SideType_...
)
