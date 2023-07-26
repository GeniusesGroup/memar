/* For license and copyright information please see the LEGAL file in the code repository */

package rrup

type Type uint8

const (
	Type_Unset Type = iota
	Type_RegisteredBy
	Type_Issuer
	Type_DelegateRole // Owner
)
