/* For license and copyright information please see the LEGAL file in the code repository */

package qru

type Type uint8

const (
	Type_Unset Type = iota

	// Just owner MUST edit the related record in any domain
	// Others CAN fork or update if owner allow.
	Type_Owner

	//TODO:: other??
)
