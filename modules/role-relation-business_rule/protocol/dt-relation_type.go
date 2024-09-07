/* For license and copyright information please see the LEGAL file in the code repository */

package rrbr_p

type Field_RelationType interface {
	RelationType() Type
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_ApplicationAccessControl
)
