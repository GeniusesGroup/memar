/* For license and copyright information please see the LEGAL file in the code repository */

package isp

type Type uint8

const (
	Type_Seller Type = iota
	Type_Customer
	Type_Agent
	Type_Franchise
)
